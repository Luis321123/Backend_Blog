from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument
from typing import Optional
from app.schemas.post import PostCreate, PostInDb
from uuid import uuid4
from datetime import datetime


class PostController:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["bebidas"]

    async def create(self, post_data: PostCreate) -> PostInDb:
        post_dic = post_data.model_dump(exclude_none=True)
        post_dic.update({
            "uuid": str(uuid4()),
            "time_get": datetime.utcnow(),
            "deleted_at": None
        })
        
        result = self.collection.insert_one(post_dic)
        new_post = self.collection.find_one({"_id": result.inserted_id})
        
        if not new_post:
            raise HTTPException(500, detail="No se pudo crear la bebida")
        
        # Convertimos el ObjectId a string para Pydantic
        new_post["_id"] = str(new_post["_id"])
        return PostInDb(**new_post)