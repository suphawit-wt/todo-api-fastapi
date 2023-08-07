from dataclasses import dataclass, field
from typing import List, Optional

from todo_api.core.exceptions import ConflictError
from todo_api.models.user import User


@dataclass
class UserRepositoryMock:
    users: List[User] = field(default_factory=list)
    next_id: int = 1

    async def get_by_username(self, username: str) -> Optional[User]:
        for user in self.users:
            if user.username == username:
                return user
        return None

    async def create(self, req: User) -> User:
        for user in self.users:
            if user.username == req.username:
                raise ConflictError("This Username already exists")
            if user.email == req.email:
                raise ConflictError("This Email already exists")
        req.id = self.next_id
        self.users.append(req)
        self.next_id += 1
        return req
