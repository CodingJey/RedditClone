from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user_model import (
    UserCreateRequest, UserUpdateRequest, UserRequest, UserResponse
)
from dependency_chains.get_user_service import get_user_service
from services.user_service import UserService

router = APIRouter()

@router.get("/users", response_model=list[UserResponse])
async def list_users(skip: int = 0, limit: int = 10, service: UserService = Depends(get_user_service)):
    users = await service.list_users_service(db, skip, limit)
    return users


@router.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user_data: UserCreateRequest, service: UserService = Depends(get_user_service)):
    return await service.create_user_service(db, user_data)


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    user = await service.get_user_service(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_data: UserUpdateRequest, service: UserService = Depends(get_user_service)):
    user = await service.update_user_service(db, user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    if not await service.delete_user_service(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}
