from fastapi import (
    FastAPI,
    Depends,
    Body,
    Request,
    HTTPException,
    Form,
    File,
    UploadFile,
)
from fastapi.responses import JSONResponse
from svix.webhooks import Webhook
from sqlmodel import Session, select
import uuid
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from clerk_backend_api import authenticate_request, Clerk, AuthenticateRequestOptions
from typing import Any
from Db.db import connect_Db, engine, User, Podcast
from dotenv import load_dotenv
import os
from models.model import Podcast_model

load_dotenv()
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
                authorized_parties=["http://localhost:3000"],
                jwt_key=os.getenv("CLERK_JWT_KEY"),
            ),
        )

        if not request_state.is_signed_in:
            raise HTTPException(status_code=403, detail="Unauthorized")

        user_id = request_state.payload.get("sub")

        request.state.user_id = user_id

    except Exception as e:

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
    return JSONResponse(
        status_code=200, content={"message": "podcast found", "data": podcast_data}
    )


@app.post("/create-podcast", dependencies=[Depends(validate_user)])
async def create_project(
    request: Request,
    file: Annotated[UploadFile, File()],
    prompt: Annotated[str, Form()],
    session: Session = Depends(get_session),
):
    user_id = request.state.user_id
    print("User Id:", user_id)
    print("User Id:", prompt)
    content =  file.read()
    
    # upload doc
    # generate title and description

    # add to redis
    # add to bd
    # session.add(podcast)
    return JSONResponse(status_code=200, content={"message": " podcast found"})


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
            id=user_id, email=email, first_name=first_name, avatar_url=image_url
        )
        session.add(user)
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
