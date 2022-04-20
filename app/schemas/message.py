from pydantic import BaseModel


class MessageInSchema(BaseModel):
    text: str
    client_id: int


class MessageSchema(BaseModel):
    id: int
    text: str
    client_id: int
