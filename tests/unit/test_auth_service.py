import pytest
import pytest_asyncio

from todo_api.core.exceptions import AppException
from todo_api.core.security import hash_password
from todo_api.models.user import User
from todo_api.repositories.mock.user_repository_mock import UserRepositoryMock
from todo_api.repositories.user_repository import UserRepository
from todo_api.schemas.request.login_request import LoginRequest
from todo_api.schemas.request.register_request import RegisterRequest
from todo_api.schemas.response.token_response import TokenResponse
from todo_api.services.auth_service import AuthService


@pytest_asyncio.fixture
async def user_repo() -> UserRepositoryMock:
    return UserRepositoryMock()


@pytest_asyncio.fixture
async def auth_service(user_repo: UserRepository) -> AuthService:
    return AuthService(user_repo)


@pytest.mark.asyncio
async def test_login_success(
    auth_service: AuthService, user_repo: UserRepositoryMock
) -> None:
    user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        password=hash_password("password"),
        first_name="Test",
        last_name="User",
    )
    await user_repo.create(user)

    req = LoginRequest(username="testuser", password="password")
    token: TokenResponse = await auth_service.login(req)

    assert token is not None


@pytest.mark.asyncio
async def test_login_invalid_username(auth_service: AuthService) -> None:
    req = LoginRequest(username="nonexist", password="password")

    with pytest.raises(AppException) as ex:
        await auth_service.login(req)

    assert ex.value.code == "UNAUTHORIZED"
    assert ex.value.status_code == 401
    assert ex.value.message == "Invalid username or password"


@pytest.mark.asyncio
async def test_login_invalid_password(
    auth_service: AuthService, user_repo: UserRepositoryMock
) -> None:
    user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        password=hash_password("password"),
        first_name="Test",
        last_name="User",
    )
    await user_repo.create(user)

    req = LoginRequest(username="testuser", password="wrongpassword")

    with pytest.raises(AppException) as ex:
        await auth_service.login(req)

    assert ex.value.code == "UNAUTHORIZED"
    assert ex.value.status_code == 401
    assert ex.value.message == "Invalid username or password"


@pytest.mark.asyncio
async def test_register_success(auth_service: AuthService) -> None:
    req = RegisterRequest(
        username="newuser",
        email="newuser@example.com",
        password="newpassword",
        first_name="New",
        last_name="User",
    )

    try:
        await auth_service.register(req)
    except AppException as ex:
        pytest.fail(ex.message)


@pytest.mark.asyncio
async def test_register_username_taken(
    auth_service: AuthService, user_repo: UserRepositoryMock
) -> None:
    user = User(
        id=1,
        username="existinguser",
        email="existing@example.com",
        password=hash_password("password"),
        first_name="Existing",
        last_name="User",
    )
    await user_repo.create(user)

    req = RegisterRequest(
        username="existinguser",
        email="newuser@example.com",
        password="newpassword",
        first_name="New",
        last_name="User",
    )

    with pytest.raises(AppException) as ex:
        await auth_service.register(req)

    assert ex.value.code == "CONFLICT"
    assert ex.value.status_code == 409
    assert ex.value.message == "This Username already exists"


@pytest.mark.asyncio
async def test_register_email_taken(
    auth_service: AuthService, user_repo: UserRepositoryMock
) -> None:
    user = User(
        id=1,
        username="existinguser",
        email="existing@example.com",
        password=hash_password("password"),
        first_name="Existing",
        last_name="User",
    )
    await user_repo.create(user)

    req = RegisterRequest(
        username="newuser",
        email="existing@example.com",
        password="newpassword",
        first_name="New",
        last_name="User",
    )

    with pytest.raises(AppException) as ex:
        await auth_service.register(req)

    assert ex.value.code == "CONFLICT"
    assert ex.value.status_code == 409
    assert ex.value.message == "This Email already exists"
