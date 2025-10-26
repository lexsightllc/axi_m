from uuid import uuid4, UUID
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    email: EmailStr
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

    def update(self, **kwargs) -> None:
        """Update user fields and refresh ``updated_at`` timestamp."""
        for field, value in kwargs.items():
            if hasattr(self, field) and value is not None:
                setattr(self, field, value)
        self.updated_at = datetime.utcnow()

UserId = UUID
