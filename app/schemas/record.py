from pydantic import BaseModel, Field
from datetime import date
from typing import Literal


class RecordCreate(BaseModel):
    amount: float = Field(gt=0)
    type: Literal["income", "expense"]
    category: str = Field(min_length=2, max_length=50)
    date: date
    description: str = Field(min_length=2, max_length=200)


class RecordUpdate(BaseModel):
    amount: float = Field(gt=0)
    type: Literal["income", "expense"]
    category: str = Field(min_length=2, max_length=50)
    date: date
    description: str = Field(min_length=2, max_length=200)