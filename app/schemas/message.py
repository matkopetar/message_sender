from pydantic import BaseModel


class MessageSchema(BaseModel):
    id: int
    text: str
    client_id: int
