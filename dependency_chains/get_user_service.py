from fastapi import Depends
from repositories.base_repository import BaseRepository
from repositories.user_repository import UserRepository
from dependency_chains.session_handler import get_repository
from services.user_service import UserService

def get_user_service(
    user_repo: UserRepository = Depends(get_repository(UserRepository))
) -> UserService:
    return UserService(user_repo)