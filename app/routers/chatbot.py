import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user

from app.schemas.chatbot import (
    ChatbotRequest,
    ChatbotResponse
)

from app.ai.chatbot_service import ChatbotService


router = APIRouter(
    prefix="/chatbot",
    tags=["AI Chatbot"]
)


@router.post(
    "/ask",
    response_model=ChatbotResponse
)
def ask_chatbot(
    request: ChatbotRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    conversation_id = request.conversation_id

    if not conversation_id:
        conversation_id = str(
            uuid.uuid4()
        )

    answer = ChatbotService.ask_question(
        db,
        request.question,
        conversation_id
    )

    return ChatbotResponse(
        answer=answer,
        conversation_id=conversation_id
    )