from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from app.db.database import get_db
from app.models.record import Record
from app.schemas.record import RecordCreate, RecordUpdate
from app.api.deps import get_current_user, require_role
from app.models.user import User

router = APIRouter()


# ✅ CREATE RECORD (Admin only)
@router.post("/")
def create_record(
    record: RecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    new_record = Record(
        amount=record.amount,
        type=record.type,
        category=record.category,
        date=record.date,
        description=record.description,
        user_id=current_user.id
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return {
        "message": "Record created successfully",
        "record_id": new_record.id
    }


# ✅ GET ALL RECORDS (Viewer, Analyst, Admin)
@router.get("/")
def get_records(
    skip: int = 0,
    limit: int = 10,
    type: Optional[str] = None,
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["viewer", "analyst", "admin"]))
):
    query = db.query(Record)

    if type:
        query = query.filter(Record.type == type)

    if category:
        query = query.filter(Record.category == category)

    if start_date:
        query = query.filter(Record.date >= start_date)

    if end_date:
        query = query.filter(Record.date <= end_date)

    records = query.offset(skip).limit(limit).all()

    return records


# ✅ GET SINGLE RECORD
@router.get("/{record_id}")
def get_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["viewer", "analyst", "admin"]))
):
    record = db.query(Record).filter(Record.id == record_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    return record


# ✅ UPDATE RECORD (Admin only)
@router.put("/{record_id}")
def update_record(
    record_id: int,
    updated: RecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    record = db.query(Record).filter(Record.id == record_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    record.amount = updated.amount
    record.type = updated.type
    record.category = updated.category
    record.date = updated.date
    record.description = updated.description

    db.commit()

    return {"message": "Record updated successfully"}


# ✅ DELETE RECORD (Admin only)
@router.delete("/{record_id}")
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    record = db.query(Record).filter(Record.id == record_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    db.delete(record)
    db.commit()

    return {"message": "Record deleted successfully"}