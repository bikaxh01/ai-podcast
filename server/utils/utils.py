import cloudinary.uploader
from fastapi import (
    File,
    UploadFile,
)
import redis
from typing import Annotated
from dotenv import load_dotenv
import os
import cloudinary

load_dotenv()


CLOUD_NAME = os.getenv("CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

cloudinary.config(
    secure_url=True,
    cloud_name=CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
)


redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), decode_responses=True
)


async def upload_file(file: Annotated[UploadFile, File()], podcast_id: str):
    upload_dir = "./doc"
    os.makedirs(upload_dir, exist_ok=True)

    content = await file.read()
    file_path = os.path.join(upload_dir, f"{podcast_id}_{file.filename}")
    with open(file_path, "wb") as f:
        f.write(content)


    res = cloudinary.uploader.upload(
        file_path,
        public_id=f"{podcast_id}",
        folder=f"EchoMind/{podcast_id}",
    )
    os.remove(file_path)
    return res["secure_url"]



def push_redis (podcast_id: str):
    redis_client.lpush("podcast",podcast_id)
    
    