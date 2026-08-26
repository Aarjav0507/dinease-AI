from typing import Optional

from pydantic import BaseModel


class ChatbotRequest(BaseModel):

    question: str

    conversation_id: Optional[str] = None


class ChatbotResponse(BaseModel):

    answer: str

    conversation_id: str