import json

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.core.auth import decode_token
from app.database import get_db
from app.dependencies import get_optional_customer
from app.chat.schemas import (
    ChatSessionCreate,
    ChatSessionOut,
    ChatTurnResponse,
    HandoffCard,
    MessageIn,
    MessageOut,
)
from app.chat import service
from app.users.customer.models import Customer

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/sessions", response_model=ChatSessionOut)
def create_chat_session(
    body: ChatSessionCreate,
    db: Session = Depends(get_db),
    customer: Customer | None = Depends(get_optional_customer),
):
    return service.create_session(db, customer, body)


@router.post("/sessions/{session_id}/messages", response_model=ChatTurnResponse)
def post_message(
    session_id: int,
    body: MessageIn,
    db: Session = Depends(get_db),
    customer: Customer | None = Depends(get_optional_customer),
):
    user_msg, bot_msg, card = service.append_turn(db, customer, session_id, body)
    handoff = (
        HandoffCard(support_phone=card["support_phone"], region=card["region"], message=card["message"])
        if card
        else None
    )
    return ChatTurnResponse(
        user_message=MessageOut.model_validate(user_msg),
        assistant_message=MessageOut.model_validate(bot_msg),
        handoff=handoff,
    )


@router.websocket("/ws/{session_id}")
async def chat_ws(
    websocket: WebSocket,
    session_id: int,
    token: str | None = Query(default=None),
):
    await websocket.accept()
    customer = None
    if token:
        try:
            payload = decode_token(token)
            if payload.get("role") == "customer":
                from app.database import SessionLocal

                db = SessionLocal()
                try:
                    customer = db.get(Customer, int(payload["sub"]))
                finally:
                    db.close()
        except ValueError:
            await websocket.send_text(json.dumps({"error": "invalid_token"}))
            await websocket.close()
            return

    from app.database import SessionLocal

    db = SessionLocal()
    try:
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)
            content = data.get("content", "")
            user_msg, bot_msg, card = service.append_turn(
                db, customer, session_id, MessageIn(content=content)
            )
            out = {
                "user": MessageOut.model_validate(user_msg).model_dump(mode="json"),
                "assistant": MessageOut.model_validate(bot_msg).model_dump(mode="json"),
                "handoff": card,
            }
            await websocket.send_text(json.dumps(out))
    except WebSocketDisconnect:
        pass
    finally:
        db.close()
