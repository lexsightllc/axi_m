from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from typing import List

from core.services.engine import UserManagementService
from core.services.validation import UserCreateInput, UserUpdateInput
from core.domain.models import User as DomainUser
from core.exceptions import NotFoundError, ConflictError, UnauthorizedError, InvalidInputError
from data.repositories.user_repository import InMemoryUserRepository

router = APIRouter()

def get_user_service() -> UserManagementService:
    return UserManagementService(InMemoryUserRepository.get_instance())

@router.post("/users", response_model=DomainUser, status_code=status.HTTP_201_CREATED)
async def create_user(user_input: UserCreateInput, user_service: UserManagementService = Depends(get_user_service)):
    try:
        user = DomainUser(name=user_input.name, email=user_input.email)
        return user_service.create_user(user)
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=e.detail)

@router.get("/users/{user_id}", response_model=DomainUser)
async def get_user(user_id: UUID, user_service: UserManagementService = Depends(get_user_service)):
    try:
        return user_service.get_user(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)

@router.put("/users/{user_id}", response_model=DomainUser)
async def update_user(user_id: UUID, user_input: UserUpdateInput, user_service: UserManagementService = Depends(get_user_service)):
    try:
        return user_service.update_user(user_id, name=user_input.name, email=user_input.email, is_active=user_input.is_active)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=e.detail)

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_user(user_id: UUID, user_service: UserManagementService = Depends(get_user_service)):
    try:
        user_service.deactivate_user(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)
