from typing import List, Optional
from core._repositories.abstract.user import UserRepository
from core._models.user import User
from db.mongo import get_mongodb
from bson import ObjectId
from pymongo import ReturnDocument
from fastapi import HTTPException,status



class UserMongoRepository(UserRepository):
    def __init__(self) -> None:
        self.db = get_mongodb()

    async def find(self, query) -> List[User]:
        return list(self.db.user.find(query))

    async def find_one(self,query: dict) -> User:
        return self.db.user.find_one(query)
    
    async def get_all(self) -> List[User]:
        return self.db.user.find()
    
    async def get_by_id(self, id: str) -> User | None:
        return self.db.user.find_one({"_id": ObjectId(id)})
    
    async def create(self,user: User) -> User | None:
        new_user = self.db.user.insert_one(user.model_dump(by_alias=True, exclude=["uuid"]))
        created_user = self.db.user.find_one(
            {"_id": new_user.inserted_id}
        )
        return created_user
    
    async def update(self, id: int | str, item: User) -> None:
        return await self.db.user.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": item},
            return_document=ReturnDocument.AFTER,
        )
    
    async def delete(self, id: str ) -> User | None:
        deleted_user = self.db.user.find_one(
            {"_id": ObjectId(id)}
        ) 
        self.db.user.delete_one({"_id": ObjectId(id)})
        return deleted_user
    
    async def get_by_email(self, email: str) -> User:
        return self.db.user.find_one({"email": email})