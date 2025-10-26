from typing import Dict, List, Optional
from core.domain.models import User, UserId
from core.services.engine import UserRepository

class InMemoryUserRepository(UserRepository):
    _instance: Optional["InMemoryUserRepository"] = None

    def __init__(self):
        self.users: Dict[UserId, User] = {}

    @classmethod
    def get_instance(cls) -> "InMemoryUserRepository":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def add(self, user: User) -> None:
        self.users[user.id] = user

    def get_by_id(self, user_id: UserId) -> Optional[User]:
        return self.users.get(user_id)

    def list_all(self) -> List[User]:
        return list(self.users.values())
