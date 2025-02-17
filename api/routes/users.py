from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user_model import (
    UserCreateRequest, UserUpdateRequest, UserRequest, UserResponse
)
from services.user_service import UserService, get_user_service
from infra.database import get_session, get_database, Database

router = APIRouter(prefix="/users")

@router.get("/test-session-dependency/")
async def test_session_dependency(session: AsyncSession = Depends(get_session)):
    return {"message": "Session dependency injected successfully!"}

@router.get("/", response_model=list[UserResponse])
async def list_users(skip: int = 0, limit: int = 10,
                        db: Database = Depends(get_database),
                        session: AsyncSession = Depends(get_session), # corrected dependency to get_session and param name
                        service: UserService = Depends(get_user_service)):
    users = await service.list_users_service(session, skip, limit) # corrected param name to session
    return users


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(user_data: UserCreateRequest,
                        db: Database = Depends(get_database),                        
                        session: AsyncSession = Depends(get_session), # kept correct dependency and param name
                        service: UserService = Depends(get_user_service)):
    return await service.create_user_service(session, user_data) # corrected param name to session


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session), # kept correct dependency and param name
                        service: UserService = Depends(get_user_service)):
    user = await service.get_user_service(session, user_id) # corrected param name to session
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_data: UserUpdateRequest,
                        session: AsyncSession = Depends(get_session), # kept correct dependency and param name
                        service: UserService = Depends(get_user_service)):
    user = await service.update_user_service(session, user_id, user_data) # corrected param name to session
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session), # kept correct dependency and param name
                        service: UserService = Depends(get_user_service)):
    if not await service.delete_user_service(session, user_id): # corrected param name to session
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}