from fastapi import APIRouter, Depends

from todo_api.core.dependencies import get_auth_service
from todo_api.schemas.request.login_request import LoginRequest
from todo_api.schemas.request.register_request import RegisterRequest
from todo_api.schemas.response.api_response import ApiResponse
from todo_api.schemas.response.token_response import TokenResponse
from todo_api.services.auth_service import AuthService

router = APIRouter()


@router.post("/login", response_model_exclude_none=True)
async def login(
    req: LoginRequest, auth_service: AuthService = Depends(get_auth_service)
) -> ApiResponse[TokenResponse]:
    token: TokenResponse = await auth_service.login(req)
    return ApiResponse[TokenResponse](data=token)


@router.post("/register", status_code=201, response_model_exclude_none=True)
async def register(
    req: RegisterRequest, auth_service: AuthService = Depends(get_auth_service)
) -> ApiResponse[None]:
    await auth_service.register(req)
    return ApiResponse[None](message="Register Successfully")
