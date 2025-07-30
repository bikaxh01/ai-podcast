from fastapi import (
    FastAPI,
    Depends,
    Request,
    HTTPException,
    Form,
    File,
    UploadFile,
)
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from svix.webhooks import Webhook
from sqlmodel import Session, select
import uuid
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from clerk_backend_api import Clerk, AuthenticateRequestOptions

from Db.db import connect_Db, engine, User, Podcast, Podcast_status
from dotenv import load_dotenv
import os


from utils.utils import upload_file, push_redis

load_dotenv()
app = FastAPI()
CLIENT_URL = os.getenv("CLIENT_URL")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[CLIENT_URL],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)


@app.on_event("startup")
def on_startup():
    connect_Db()


def get_session():
    with Session(engine) as session:
        yield session


clerk_sdk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))


async def validate_user(request: Request):
    try:

        request_state = clerk_sdk.authenticate_request(
            request,
            AuthenticateRequestOptions(
                authorized_parties=["http://localhost:3000", CLIENT_URL],
                jwt_key=os.getenv("CLERK_JWT_KEY"),
            ),
        )
        if not request_state.is_signed_in:
            raise HTTPException(status_code=403, detail="Unauthorized")

        user_id = request_state.payload.get("sub")

        request.state.user_id = user_id

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unauthorized")


@app.get("/")
def read_root(session: Session = Depends(get_session)):
    # user = User(email="Bikash@gmmail.com", first_name="Bikash")
    # session.add(user)
    # session.commit()
    # session.refresh(user)

    return {
        "status": "ok 🔥🔥",
    }


@app.get("/internal/get-podcast/{podcast_id}")
def get_project_by_id(podcast_id: str, session: Session = Depends(get_session)):
    try:
        podcast_uuid = uuid.UUID(podcast_id)
    except ValueError:
        return JSONResponse(status_code=400, content={"message": "Invalid UUID format"})
    podcast_data = session.get(Podcast, podcast_uuid)
    if not podcast_data:
        return JSONResponse(status_code=404, content={"message": "No podcast found"})
    podcast_data.id = str(podcast_data.id)
    podcast_data.created_at = str(podcast_data.created_at)
    return JSONResponse(
        status_code=200,
        content={"message": "podcast found", "data": podcast_data.model_dump()},
    )


@app.get("/get-podcasts", dependencies=[Depends(validate_user)])
async def get_podcast(request: Request, session: Session = Depends(get_session)):
    try:
        user_id = request.state.user_id

        statement = (
            select(Podcast)
            .where(
                (Podcast.status != Podcast_status.FAILED) & (Podcast.user_id == user_id)
            )
            .order_by(Podcast.created_at.desc())
        )

        result = session.exec(statement).all()

        podcasts_data = []
        for p in result:
            data = p.model_dump()
            data["id"] = str(data["id"])
            data["created_at"] = str(data["created_at"])
            data["user_id"] = str(data["user_id"])
            podcasts_data.append(data)
        return JSONResponse(
            status_code=200,
            content={"message": "podcasts found", "data": podcasts_data},
        )
    except Exception as e:
        print(f"ERROR {e}")
        return JSONResponse(
            status_code=500, content={"message": "something went wrong", "data": []}
        )


@app.post("/create-podcast", dependencies=[Depends(validate_user)])
async def create_project(
    request: Request,
    prompt: Annotated[str, Form()],
    file: Annotated[UploadFile, File()] = None,
    session: Session = Depends(get_session),
):
    try:
        user_id = request.state.user_id
        podcast_id = uuid.uuid4()

        podcast = Podcast(id=podcast_id, user_id=user_id, prompt=prompt)

        # upload doc
        if file != None:
            file_url = await upload_file(file, podcast_id)
            podcast.file_url = file_url

        session.add(podcast)
        session.commit()
        session.refresh(podcast)
        # add to redis
        push_redis(str(podcast_id))

        podcast.created_at = str(podcast.created_at)
        podcast.id = str(podcast.id)
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Generating podcast...😁",
                "data": podcast.model_dump(),
            },
        )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "something went wrong",
                "data": str(e),
            },
        )


@app.post("/clerk-webhook")
async def save_user(request: Request, session: Session = Depends(get_session)):
    try:

        headers = request.headers
        body = await request.body()

        webhook_secret = os.getenv("CLERK_WEBHOOK_SECRET")
        wh = Webhook(webhook_secret)

        payload = wh.verify(body, headers)["data"]

        email = payload.get("email_addresses")[0].get("email_address")
        user_id = payload.get("id")
        first_name = payload.get("first_name")
        image_url = payload.get("image_url")

        user = User(
            id=user_id,
            email=email,
            first_name=first_name,
            avatar_url=image_url,
        )
        session.add(user)
        session.commit()  # Commit user first so user_id exists

        podcast_id = uuid.uuid4()
        podcast = Podcast(
            id=podcast_id,
            user_id=user_id,
            prompt="initial",
            audio_url="https://res.cloudinary.com/bikash01/video/upload/v1753377384/EchoMind/7b12f25c-7737-40a9-8d80-6c13e78e55a1/7b12f25c-7737-40a9-8d80-6c13e78e55a1_final.wav",
            status=Podcast_status.COMPLETED,
            title="Understanding Web3: The Next Generation of the Internet",
            description="An insightful discussion on the evolution of the internet, from Web1 to the emerging Web3, exploring its core principles, technologies, and real-world examples."
        )
        session.add(podcast)
        session.commit()

        return JSONResponse(
            status_code=201, content={"status": "true", "message": "Created"}
        )
    except Exception as e:
        print("Error: ", e)
        return JSONResponse(
            status_code=501,
            content={"status": "false", "message": "something went wrong"},
        )


class Update_podcast(BaseModel):

    title: str | None = None
    description: str | None = None
    status: Podcast_status
    audio_url: str | None = None


@app.put("/internal/update-podcast/{podcast_id}")
def update_podcast(
    podcast_id: str,
    podcast_data: Update_podcast,
    session: Session = Depends(get_session),
):
    try:
        print("ID", podcast_id)
        podcast_id = uuid.UUID(podcast_id)
        podcast = session.get(Podcast, podcast_id)

        if not podcast:
            print(
                "NOT found 🟢🟢🟢",
            )
            return JSONResponse(
                status_code=404,
                content={"status": False, "message": "invalid podcast id"},
            )
        final_podcast = podcast_data.model_dump(exclude_unset=True)
        podcast.sqlmodel_update(final_podcast)
        session.add(podcast)
        session.commit()
        session.refresh(podcast)
        podcast.id = str(podcast.id)
        podcast.created_at = str(podcast.created_at)
        return JSONResponse(
            status_code=200,
            content={
                "status": True,
                "message": "Updated successfully",
                "data": podcast.model_dump(),
            },
        )
    except Exception as e:
        print("Error: ", e)
        return JSONResponse(
            status_code=501,
            content={"status": False, "message": "something went wrong"},
        )
