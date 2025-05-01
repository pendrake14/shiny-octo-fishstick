# apps/users/models/__init__.py

from .user import User, UserTypeChoices
from .user_profile import UserProfile

__all__ = ['User', 'UserTypeChoices', 'UserProfile']