from pydantic import BaseModel


class AddRole(BaseModel):
    server: str
    user: str
    tiempo: str