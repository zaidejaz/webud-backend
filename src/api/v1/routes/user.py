from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status, Body
from pydantic import BaseModel
from sqlmodel import Session

from src.crud.user import get_user_by_id, update_user
from src.database import get_session
from src.models.users import User
from src.schemas.auth import UserOut
from src.utils.auth import get_current_active_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[UserOut])
async def get_users(
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    skip: int = 0,
    limit: int = 100
):
    """
    Get a list of users (requires authentication)
    
    - **skip**: Number of users to skip for pagination
    - **limit**: Maximum number of users to return
    
    Returns:
        List of user objects with their profile information
    """
    # In a real application, you might want to restrict this to admin users
    from sqlmodel import select
    users = session.exec(select(User).offset(skip).limit(limit)).all()
    return users

@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user_id: int,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    Get a specific user by ID (requires authentication)
    
    - **user_id**: The ID of the user to retrieve
    
    Returns:
        User object with profile information
    """
    user = get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

class UserUpdate(BaseModel):
    name: str | None = None
    profile_picture: str | None = None

@router.put("/{user_id}", response_model=UserOut)
async def update_user_profile(
    user_id: int,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    user_data: UserUpdate = Body(..., description="User data to update")
):
    """
    Update a user profile (requires authentication)
    
    - **user_id**: The ID of the user to update
    - **user_data**: User data to update
      - name: New name for the user (optional)
      - profile_picture: New profile picture URL (optional)
    
    Returns:
        Updated user object with profile information
    """
    # Check if user is updating their own profile
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )
        
    # Convert Pydantic model to dict, excluding unset values
    user_data_dict = user_data.model_dump(exclude_unset=True)
    
    updated_user = update_user(user_id, user_data_dict, session)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user

