# SPDX-License-Identifier: MIT
from typing import Optional, List, Protocol
from uuid import UUID

from core.domain.models import User, UserId
from core.domain.rules import validate_new_user_data
from core.exceptions import NotFoundError, ConflictError

class UserRepository(Protocol):
    def add(self, user: User) -> None: ...
    def get_by_id(self, user_id: UserId) -> Optional[User]: ...
    def list_all(self) -> List[User]: ...

class UserManagementService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, user: User) -> User:
        existing = self.user_repo.list_all()
        validate_new_user_data(user, existing)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id: UserId) -> User:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User", str(user_id))
        return user

    def update_user(
        self,
        user_id: UserId,
        name: Optional[str] = None,
        email: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> User:
        """Update a user's details."""
        user = self.get_user(user_id)
        user.update(name=name, email=email, is_active=is_active)
        return user

    def deactivate_user(self, user_id: UserId) -> User:
        """Mark a user as inactive."""
        user = self.get_user(user_id)
        user.update(is_active=False)
        return user
