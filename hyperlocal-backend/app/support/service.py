from sqlalchemy import text
from sqlalchemy.orm import Session

from app.support.models import FAQ, RegionalContact, Ticket
from app.support.schemas import TicketCreate


def list_faqs(db: Session):
    return db.query(FAQ).order_by(FAQ.id).all()


def list_contacts(db: Session):
    return db.query(RegionalContact).order_by(RegionalContact.area_name).all()


def raise_ticket(db: Session, data: TicketCreate) -> Ticket:
    contact = db.query(RegionalContact).first()
    phone = contact.support_phone if contact else "+91-20-0000-HELP"
    t = Ticket(
        user_role=data.user_role,
        user_ref=data.user_ref,
        issue_description=data.issue_description,
        status="open",
        assigned_phone=phone,
    )
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


def ping_db(db: Session) -> bool:
    try:
        db.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
