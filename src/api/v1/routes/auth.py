from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from src.crud.user import create_user, get_user_by_email, update_user
from src.database import get_session
from src.models.users import User
from src.schemas.auth import (
    RegisterIn, 
    RegisterOut, 
    Token, 
    UserOut, 
    ChangePassword, 
    PasswordResetRequest,
    PasswordReset
)
from src.utils.auth import (
    authenticate_user, 
    create_access_token, 
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    verify_password,
    get_password_hash
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=RegisterOut, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: RegisterIn, 
    session: Annotated[Session, Depends(get_session)]
):
    """
    Register a new user
    
    - **name**: Full name of the user
    - **email**: User's email address (must be unique)
    - **password**: User's password
    """
    # Check if email already exists
    db_user = get_user_by_email(user_data.email, session)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
        
    # Create new user
    user = create_user(user_data, session)
    
    return user

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_session)]
):
    """
    OAuth2 compatible token login, get an access token for future requests
    
    - **username**: Enter your email address in this field (FastAPI OAuth2 uses 'username' field)
    - **password**: Your password
    
    Returns:
        Access token for authentication
    """
    # The username field in OAuth2PasswordRequestForm will contain the email
    email = form_data.username
    password = form_data.password
    
    user = authenticate_user(email, password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    Get current user information
    
    Returns information about the currently authenticated user.
    """
    return current_user

@router.post("/logout")
async def logout():
    """
    Logout the current user
    
    Note: With JWT tokens, the typical approach is to handle logout on the client side
    by removing the token from local storage. This endpoint is provided for API
    completeness and could be extended with a token blacklist system in the future.
    
    Returns:
        A message confirming successful logout
    """
    return {"message": "Successfully logged out"}

@router.post("/change-password")
async def change_password(
    password_data: ChangePassword,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """
    Change the user's password (requires authentication)
    
    - **current_password**: The user's current password for verification
    - **new_password**: The new password to set
    
    Returns:
        A message confirming the password change
    """
    # Verify current password
    if not verify_password(password_data.current_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Update password
    user_data = {"password": password_data.new_password}
    update_user(current_user.id, user_data, session)
    
    return {"message": "Password changed successfully"}

@router.post("/password-reset/request")
async def request_password_reset(
    reset_request: PasswordResetRequest,
    session: Annotated[Session, Depends(get_session)]
):
    """
    Request a password reset
    
    - **email**: The email address of the account to reset password for
    
    In a real application, this would:
    1. Generate a reset token
    2. Store it in the database with an expiration time
    3. Send an email with the reset link
    
    Returns:
        A message indicating that a reset link will be sent if the email exists
    """
    user = get_user_by_email(reset_request.email, session)
    if not user:
        # Don't reveal that the email doesn't exist
        return {"message": "If your email is registered, you will receive a password reset link"}
    
    # In a real application, generate token, save it, and send email
    # For this example, we'll just return a success message
    return {"message": "If your email is registered, you will receive a password reset link"}

@router.post("/password-reset/confirm")
async def confirm_password_reset(
    reset_data: PasswordReset,
    session: Annotated[Session, Depends(get_session)]
):
    """
    Confirm a password reset
    
    - **token**: The password reset token received via email
    - **new_password**: The new password to set
    
    In a real application, this would:
    1. Verify the reset token
    2. Check if it's expired
    3. Update the user's password
    
    Returns:
        A message confirming the password has been reset
    """
    # In a real application, verify token and update password
    # For this example, we'll return a success message
    return {"message": "Password has been reset successfully"}