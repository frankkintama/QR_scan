from fastapi import APIRouter, Depends, HTTPException
from app.models import User, UserRead, UserUpdate
from app.core.auth import fastapi_users  # import your FastAPIUsers instance

router = APIRouter(prefix="/users", tags=["users"])

# Get the current active user
current_user = fastapi_users.current_user(active=True)


@router.patch("/me", response_model=UserRead)
async def update_current_user(
    user_update: UserUpdate,
    user: User = Depends(current_user)
):
    """Update the current user's information"""
    update_dict = user_update.dict(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(user, field, value)
    await user.save()
    return user


@router.delete("/me")
async def delete_current_user(user: User = Depends(current_user)):
    """Delete the currently logged-in user"""
    target = await User.get(user.id)
    if not target:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản")
    
    await target.delete()
    return {"message": "User deleted successfully"}
