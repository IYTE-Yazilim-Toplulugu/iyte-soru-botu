from dataclasses import dataclass

from pydantic import BaseModel
from shared_kernel import Role
from ulid import ULID


@dataclass
class UserDTO(BaseModel):
    id: ULID
    email: str
    name: str
    surname: str
    role: Role
