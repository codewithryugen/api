from pydantic import BaseModel

class ShakoSchema(BaseModel):
  prompt: str
  history: list = list()
  chat_id: str = None