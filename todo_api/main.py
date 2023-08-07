import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="Todo API FastAPI",
    description="This is CRUD Todo API project using FastAPI, PostgreSQL, SQLAlchemy, Alembic, Pytest, MyPy, Poetry, Docker, JWT and Swagger",
    version="1.0.0",
)


@app.get("/")
def get_root() -> dict[str, str]:
    return {"message": "Hello, world."}


def start() -> None:
    uvicorn.run("todo_api.main:app", host="0.0.0.0", port=8000, workers=4)


def dev() -> None:
    uvicorn.run("todo_api.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    start()
