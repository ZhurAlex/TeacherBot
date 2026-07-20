from fastapi import APIRouter
from admin.schemas import UserSchema, MessageSchema
from common.repository import get_all_users

router = APIRouter()

# @router.get("/users", response_model=list[UserSchema])
@router.get("/users")
async def read_all_users():
    users = await get_all_users()
    return users

@router.get("/")
def read_root():
    return {"Hello": "World"}