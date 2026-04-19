from sqlalchemy.orm import Session

from app.chat import ai_bot
from app.chat.models import ChatSession, Message
from app.chat.schemas import ChatSessionCreate, MessageIn
from app.core.exceptions import ForbiddenError, NotFoundError
from app.users.customer.models import Customer


def create_session(db: Session, customer: Customer | None, data: ChatSessionCreate) -> ChatSession:
    s = ChatSession(customer_id=customer.id if customer else None, title=data.title)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


def append_turn(db: Session, customer: Customer | None, session_id: int, body: MessageIn) -> tuple[Message, Message, dict | None]:
    session = db.get(ChatSession, session_id)
    if not session:
        raise NotFoundError("Session not found")
    if session.customer_id is not None:
        if customer is None or session.customer_id != customer.id:
            raise ForbiddenError("Not your chat session")

    user_msg = Message(session_id=session.id, role="user", content=body.content)
    db.add(user_msg)
    db.flush()

    text, handoff = ai_bot.build_reply(body.content)
    bot_msg = Message(session_id=session.id, role="assistant", content=text)
    db.add(bot_msg)
    db.commit()
    db.refresh(user_msg)
    db.refresh(bot_msg)
    card = None
    if handoff:
        card = {"support_phone": "+91-20-0000-HELP", "region": "Pune", "message": text}
    return user_msg, bot_msg, card
