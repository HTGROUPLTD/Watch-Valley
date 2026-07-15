from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, ConfigDict


# ---------------- accounts ----------------
class SignupIn(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class AccountOut(BaseModel):
    name: str
    email: EmailStr


class AccountDirectoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    email: EmailStr
    created_at: datetime


# ---------------- products ----------------
class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    gender: str
    price: float
    description: str
    image_url: Optional[str] = None
    dial: str
    strap: str
    accent: str
    popularity: int


class ProductCreateIn(BaseModel):
    name: str
    gender: str  # "men" | "women"
    price: float
    description: str = ""
    image_url: Optional[str] = None
    dial: str = "#121212"
    strap: str = "#8A8A8E"
    accent: str = "#C1272D"


class ProductUpdateIn(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    dial: Optional[str] = None
    strap: Optional[str] = None
    accent: Optional[str] = None


# ---------------- orders ----------------
class OrderItemIn(BaseModel):
    id: int
    name: str
    price: float
    qty: int


class OrderCreateIn(BaseModel):
    items: List[OrderItemIn]
    total: float
    name: str
    phone: str
    address: str
    account_email: Optional[EmailStr] = None
    account_name: Optional[str] = None


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    items: list
    total: float
    name: str
    phone: str
    address: str
    status: str
    account_email: Optional[str] = None
    account_name: Optional[str] = None
    created_at: datetime


class StatusUpdateIn(BaseModel):
    status: str


# ---------------- owner auth ----------------
class OwnerLoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
