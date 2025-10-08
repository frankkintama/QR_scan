from fastapi import APIRouter, Depends, HTTPException, status
from beanie import PydanticObjectId
from typing import List

from app.models import User, UserRead, UserUpdate
from app.core.auth import fastapi_users  # your FastAPIUsers instance

router = APIRouter(prefix="/admin", tags=["admin"])

# ---- Dependencies ----
current_user = fastapi_users.current_user(active=True)

async def admin_required(user: User = Depends(current_user)):
    if not (user.role == "admin" or user.is_superuser):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only!"
        )
    return user

async def staff_or_admin_required(user: User = Depends(current_user)):
    if not (user.role in ["staff", "admin"] or user.is_superuser):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff or Admin only!"
        )
    return user
# ---- ROUTES ----

@router.get("/dashboard")
async def admin_dashboard(user: User = Depends(admin_required)):
    """Simple dashboard check"""
    return {"message": f"Welcome Admin {user.username}!"}


@router.get("/users", response_model=List[UserRead])
async def get_all_users(_: User = Depends(staff_or_admin_required)):
    """List all users"""
    users = await User.find_all().to_list()
    return users


@router.get("/users/{user_id}", response_model=UserRead)
async def get_user_by_id(user_id: PydanticObjectId, _: User = Depends(admin_required)):
    """Get a user by ID"""
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/users/{user_id}", response_model=UserRead)
async def update_user(user_id: PydanticObjectId, data: UserUpdate, _: User = Depends(admin_required)):
    """Update a user (e.g., change role, name, etc.)"""
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = data.dict(exclude_unset=True)
    await user.set(update_data)
    return user


@router.delete("/users/{user_id}")
async def delete_user(user_id: PydanticObjectId, _: User = Depends(admin_required)):
    """Delete a user by ID"""
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await user.delete()
    return {"message": f"User {user.email} deleted successfully."}
