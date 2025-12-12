from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class OrgCreate(BaseModel):
    organization_name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=6)

class OrgGet(BaseModel):
    organization_name: str

class OrgUpdate(BaseModel):
    current_name: str
    new_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class OrgDelete(BaseModel):
    organization_name: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class OrganizationOut(BaseModel):
    id: str
    organization_name: str
    collection_name: str
    admin_email: EmailStr
