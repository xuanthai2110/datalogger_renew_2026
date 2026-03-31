from fastapi import APIRouter, Depends, HTTPException, Body
from backend.models.user import UserCreate, UserResponse
from backend.services.local_auth_utils import hash_password
from backend.services.user_service import UserService
from backend.api.auth_api import get_current_user_id, get_user_service
from typing import List
import logging

router = APIRouter(prefix="/api/users", tags=["users"])
logger = logging.getLogger(__name__)

@router.post("", response_model=UserResponse)
def post_user(user: UserCreate = Body(..., example={
    "username": "admin",
    "password": "strongpassword123",
    "email": "admin@solardatalogger.local",
    "fullname": "Administrator",
    "phone": "0987654321",
    "role": "admin"
}), user_svc: UserService = Depends(get_user_service)):
    """Tạo user mới."""
    try:
        # Check if username exists
        if user_svc.get_user_by_name(user.username):
            raise HTTPException(status_code=400, detail="Username already exists")
        
        hashed = hash_password(user.password)
        user.password = hashed
        user_id = user_svc.create_user(user)
        # Refetch to get created_at
        user_dict = user_svc.get_user_by_name(user.username)
        # Filter out hashed_password
        return UserResponse(
            id=user_dict["id"],
            username=user_dict["username"],
            email=user_dict["email"],
            fullname=user_dict["fullname"],
            phone=user_dict["phone"],
            role=user_dict["role"],
            created_at=user_dict["created_at"]
        )
    except Exception as e:
        logger.error(f"create_user error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=List[UserResponse])
def get_users(user_svc: UserService = Depends(get_user_service), current_user = Depends(get_current_user_id)):
    """Lấy danh sách user (yêu cầu login)."""
    # Note: Not implemented in MetadataDB yet, returning empty or fallback logic
    return []
