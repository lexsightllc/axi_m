import pytest
from datetime import datetime
from uuid import uuid4

from core.domain.models import User, UserId
from core.domain.rules import validate_new_user_data


def test_user_update_updates_timestamp():
    user = User(name="Example", email="user@example.com")
    old_ts = user.updated_at
    user.update(name="Example2")
    assert user.name == "Example2"
    assert user.updated_at > old_ts


def test_validate_new_user_data_rejects_duplicate_email():
    existing = [User(name="A", email="a@example.com")]
    with pytest.raises(ValueError):
        validate_new_user_data(User(name="B", email="a@example.com"), existing)
