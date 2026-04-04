from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from app.db.database import get_db
from app.models.record import Record
from app.api.deps import require_role
from app.models.user import User

router = APIRouter()

@router.get("/summary")
def get_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["analyst", "admin"]))
):
    total_income = db.query(func.sum(Record.amount)).filter(Record.type == "income").scalar() or 0
    total_expense = db.query(func.sum(Record.amount)).filter(Record.type == "expense").scalar() or 0

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": total_income - total_expense
    }

@router.get("/category-wise")
def category_wise(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["analyst", "admin"]))
):
    data = db.query(
        Record.category,
        func.sum(Record.amount).label("total")
    ).group_by(Record.category).all()

    return [{"category": d[0], "total": d[1]} for d in data]

@router.get("/recent")
def recent_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["viewer", "analyst", "admin"]))
):
    records = db.query(Record).order_by(Record.date.desc()).limit(5).all()
    return records

@router.get("/monthly-trends")
def monthly_trends(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["analyst", "admin"]))
):
    data = db.query(
        func.strftime("%Y-%m", Record.date),
        func.sum(Record.amount)
    ).group_by(func.strftime("%Y-%m", Record.date)).all()

    return [{"month": d[0], "total": d[1]} for d in data]