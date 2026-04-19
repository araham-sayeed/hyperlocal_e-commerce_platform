from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.support.schemas import ContactOut, FAQOut, TicketCreate, TicketOut
from app.support.server_status import build_status_payload
from app.support import service

router = APIRouter(prefix="/support", tags=["Support"])


@router.get("/faqs", response_model=list[FAQOut])
def faqs(db: Session = Depends(get_db)):
    return service.list_faqs(db)


@router.get("/contacts", response_model=list[ContactOut])
def contacts(db: Session = Depends(get_db)):
    rows = service.list_contacts(db)
    return [ContactOut(area_name=r.area_name, support_phone=r.support_phone) for r in rows]


@router.post("/tickets", response_model=TicketOut)
def raise_ticket(body: TicketCreate, db: Session = Depends(get_db)):
    return service.raise_ticket(db, body)


@router.get("/status")
def support_status(db: Session = Depends(get_db)):
    return build_status_payload(service.ping_db(db))
