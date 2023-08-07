import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from todo_api.api.routes import api_router
from todo_api.core.exceptions import AppException
from todo_api.core.settings import CORS_ORIGIN, DOCS_URL, OPENAPI_URL, REDOC_URL
from todo_api.schemas.response.api_response import ApiResponse

app = FastAPI(
    title="Todo API FastAPI",
    description="This is CRUD Todo API project using FastAPI, PostgreSQL, SQLAlchemy, Alembic, Pytest, MyPy, Poetry, Docker, JWT and Swagger",
    version="1.0.0",
    docs_url=DOCS_URL,
    redoc_url=REDOC_URL,
    openapi_url=OPENAPI_URL,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGIN,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(api_router, prefix="/api")


@app.exception_handler(AppException)
async def app_exception_handler(req: Request, e: AppException) -> JSONResponse:
    res = ApiResponse(code=e.code, message=e.message).model_dump(exclude_none=True)
    return JSONResponse(status_code=e.status_code, content=res)


@app.exception_handler(RequestValidationError)
async def request_validation_handler(
    req: Request, e: RequestValidationError
) -> JSONResponse:
    res = ApiResponse(code="INVALID_INPUT", errors=e.errors()).model_dump(
        exclude_none=True
    )
    return JSONResponse(status_code=400, content=res)


def start() -> None:
    uvicorn.run("todo_api.main:app", host="0.0.0.0", port=8000, workers=4)


def dev() -> None:
    uvicorn.run("todo_api.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    start()
