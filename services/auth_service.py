from models import User
from database import db


def register_user(email, password, is_admin=False):
    """Register a new user"""
    # Check if user already exists
    existing_user = User.query.filter_by(email=email.lower()).first()
    if existing_user:
        return None

    # Create new user
    new_user = User(
        email=email,
        password=password,
        is_admin=is_admin
    )

    db.session.add(new_user)
    db.session.commit()

    print(f"Потвърждение за регистрацията на {email}")
    return new_user.to_dict()


def login_user(email, password):
    """Login user with email and password"""
    user = User.query.filter_by(email=email.lower()).first()

    if user and user.password == password:
        return user.to_dict()

    return None


def get_user_by_id(user_id):
    """Get user by ID"""
    user = User.query.get(user_id)
    return user.to_dict() if user else None