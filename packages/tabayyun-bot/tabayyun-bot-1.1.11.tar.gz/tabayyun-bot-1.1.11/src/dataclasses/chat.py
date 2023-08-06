from pydantic import BaseModel


class Chat(BaseModel):
    chat_id: int
    sender_id: str
    sender: str
    str_message: str
