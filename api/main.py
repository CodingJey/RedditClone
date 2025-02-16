from fastapi import APIRouter
from api.routes import users, posts, thread

api_router = APIRouter()

api_router.include_router(users.router)
# api_router.include_router(posts.router)
# api_router.include_router(thread.router)


#
# def get_token(authorization: str = Header(...)):
#     if not authorization.startswith("Bearer "):
#         raise HTTPException(status_code=401, detail="Invalid authorization header")
#     return authorization[len("Bearer "):]
#
# @router.post("/login", response_model=LoginResponse)
# async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
#     token = await login_service(db, login_data.email, login_data.password)
#     if not token:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     return {"token": token}
#
# @router.post("/logout")
# async def logout(token: str = Depends(get_token), db: AsyncSession = Depends(get_db)):
#     await logout_service(db, token)
#     return Response(status_code=204)




