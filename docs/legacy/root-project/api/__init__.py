# SPDX-License-Identifier: MIT
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from core.exceptions import CoreException, NotFoundError, ConflictError, UnauthorizedError, InvalidInputError
from api.middleware import setup_auth_middleware
from api.routes.v1 import user as v1_user_routes

app = FastAPI(
    title="Nexus SaaS API",
    description="The RESTful API for the Nexus SaaS Platform, providing access to core services and data.",
    version="1.0.0",
    redoc_url="/docs",
    docs_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_auth_middleware(app)

@app.exception_handler(NotFoundError)
async def not_found_exception_handler(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": exc.message, "detail": exc.detail})

@app.exception_handler(ConflictError)
async def conflict_exception_handler(request: Request, exc: ConflictError):
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"message": exc.message, "detail": exc.detail})

@app.exception_handler(UnauthorizedError)
async def unauthorized_exception_handler(request: Request, exc: UnauthorizedError):
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": exc.message, "detail": exc.detail}, headers={"WWW-Authenticate": "Bearer"})

@app.exception_handler(InvalidInputError)
async def invalid_input_exception_handler(request: Request, exc: InvalidInputError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": exc.message, "errors": exc.errors, "detail": exc.detail})

@app.exception_handler(CoreException)
async def core_exception_handler(request: Request, exc: CoreException):
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "An unexpected server error occurred.", "detail": exc.detail or "Please try again later."})

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Nexus SaaS API is operational."}

@app.get("/ready")
async def readiness_check():
    return {"status": "ready", "message": "Nexus SaaS API is ready to serve traffic."}

app.include_router(v1_user_routes.router, prefix="/v1", tags=["Users"])
