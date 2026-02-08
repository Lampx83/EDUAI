<<<<<<< HEAD
from fastapi import APIRouter, HTTPException, status, Depends

from eduai.api.schemas.auth import LoginRequest, TokenResponse
from eduai.core.auth import verify_token
=======
from fastapi import APIRouter, HTTPException, status

from eduai.api.schemas.auth import LoginRequest, TokenResponse
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
from eduai.services.auth_service import authenticate

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    token = authenticate(data.username, data.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    return {"access_token": token}
<<<<<<< HEAD


@router.get("/me")
def me(payload: dict = Depends(verify_token)):
    """Trả về thông tin user hiện tại từ token (dùng để lọc lịch sử theo từng tài khoản)."""
    return {"username": payload["sub"]}
=======
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
