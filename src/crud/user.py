from sqlmodel import Session, select
from src.models.users import User
from src.schemas.auth import RegisterIn
from src.utils.auth import get_password_hash

def create_user(user_data: RegisterIn, session: Session):
    """Create a new user with hashed password"""
    # Hash the password
    hashed_password = get_password_hash(user_data.password)
    
    # Create user object
    user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_password
    )
    
    # Add to database
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user

def get_user_by_email(email: str, session: Session):
    """Get a user by email"""
    return session.exec(select(User).where(User.email == email)).first()

def get_user_by_id(user_id: int, session: Session):
    """Get a user by ID"""
    return session.get(User, user_id)

def update_user(user_id: int, user_data: dict, session: Session):
    """Update user information"""
    user = get_user_by_id(user_id, session)
    if not user:
        return None
    
    for key, value in user_data.items():
        if key == "password" and value:
            value = get_password_hash(value)
        setattr(user, key, value)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user
