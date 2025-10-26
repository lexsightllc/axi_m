# SPDX-License-Identifier: MIT
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreateInput(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserUpdateInput(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    is_active: Optional[bool]
