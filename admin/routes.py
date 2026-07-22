from fastapi import APIRouter, HTTPException, Body
from admin.schemas import BlockUserSchema, UserSchema, MessageSchema
from common.repository.users import get_all_users, get_user_by_id, set_user_blocked
from common.repository.messages import get_user_messages

router = APIRouter()

@router.get("/users", response_model=list[UserSchema])
async def read_all_users():
    users = await get_all_users()
    return users

@router.get("/users/{user_id}", response_model=UserSchema)
async def read_user(user_id: int):
    user = await get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users/{user_id}/messages", response_model=list[MessageSchema])
async def read_user_messages(user_id: int):
    messages = await get_user_messages(user_id)
    if messages is None:
        raise HTTPException(status_code=404, detail="User not found")
    return messages

@router.patch("/users/{user_id}/block", response_model=BlockUserSchema)
async def block_user(user_id: int, blocked: bool = Body(embed=True)):
    user = await set_user_blocked(user_id, blocked)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return BlockUserSchema(id=user_id, is_blocked=blocked)



@router.get("/")
def read_root():
    return {"Hello": "World"}