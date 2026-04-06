from pydantic import BaseModel
from typing import Optional

class LeadCreate(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    interest: Optional[str] = None
    budget: Optional[str] = None
    urgency: Optional[str] = 'low'
    message_raw: Optional[str] = None
    source: Optional[str] = 'csv_upload'

class LeadUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    stage: Optional[str] = None
    is_contacted: Optional[bool] = None
    notes: Optional[str] = None