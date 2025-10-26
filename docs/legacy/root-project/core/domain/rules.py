# SPDX-License-Identifier: MIT
from typing import List
from core.domain.models import User


def validate_new_user_data(user: User, existing: List[User]):
    if any(u.email == user.email for u in existing):
        raise ValueError("User with email already exists")
