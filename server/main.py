from fastapi import FastAPI, Depends, Body
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from clerk_backend_api import CreateUserRequestBody
from typing import Any
from Db.db import connect_Db, engine, User

app = FastAPI()


@app.on_event("startup")
def on_startup():
    connect_Db()


def get_session():
    with Session(engine) as session:
        yield session


@app.get("/")
def read_root(session: Session = Depends(get_session)):
    # user = User(email="Bikash@gmmail.com", first_name="Bikash")
    # session.add(user)
    # session.commit()
    # session.refresh(user)
    return {"status": "ok 🔥🔥"}


@app.post("/clerk-webhook")
def save_user(body: dict = Body(...), session: Session = Depends(get_session)):
    try:
        req_payload = body.get("data")
        email = req_payload.get("email_addresses")[0].get("email_address")
        user_id = req_payload.get("id")
        first_name = req_payload.get("first_name")
        image_url = req_payload.get("image_url")
       
        user = User(
            id=user_id, email=email, first_name=first_name, avatar_url=image_url
        )
        session.add(user)
        session.commit()
        return JSONResponse(
            status_code=201, content={"status": "true", "message": "Created"}
        )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=501, content={"status": "false", "message": "something went wrong"}
        )
