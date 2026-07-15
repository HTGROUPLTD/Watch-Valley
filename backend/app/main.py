import os
import random
import string
import shutil
import uuid
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from . import models, schemas, security
from .notifications import send_order_whatsapp
from .database import Base, engine, get_db
from .seed import seed_products

load_dotenv()

Base.metadata.create_all(bind=engine)

OWNER_EMAIL = os.getenv("OWNER_EMAIL", "htenterprisesofficial@gmail.com")
# If OWNER_PASSWORD_HASH isn't set, we hash OWNER_PASSWORD (or the default) at startup.
OWNER_PASSWORD_HASH = os.getenv("OWNER_PASSWORD_HASH") or security.hash_password(
    os.getenv("OWNER_PASSWORD", "*htgroup8*")
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="Watch Valley API")

# ⚠️ TEMPORARY: the /api/owner/* endpoints below currently have NO login
# requirement — anyone who can reach this server can view/edit orders,
# accounts, and products. This was intentionally relaxed so the dashboard
# is easy to browse while you're testing. Before this goes anywhere public,
# re-add `Depends(security.require_owner)` to each /api/owner/* route below,
# and restore the login screen in watch-valley-backend.jsx.

# CORS: wide open for local development. Tighten allow_origins to your real
# storefront/backend domains before deploying this to production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serves uploaded product photos at http://<host>/uploads/<filename>
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


@app.on_event("startup")
def on_startup():
    db = next(get_db())
    seed_products(db)


def gen_order_code() -> str:
    return "WV-" + "".join(random.choices(string.digits, k=8))


# =============================================================================
# ACCOUNTS (customer signup / login)
# =============================================================================
@app.post("/api/accounts/signup", response_model=schemas.AccountOut)
def signup(payload: schemas.SignupIn, db: Session = Depends(get_db)):
    email = payload.email.lower()
    existing = db.query(models.Account).filter(models.Account.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email already exists.")
    account = models.Account(
        name=payload.name,
        email=email,
        password_hash=security.hash_password(payload.password),
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return schemas.AccountOut(name=account.name, email=account.email)


@app.post("/api/accounts/login", response_model=schemas.AccountOut)
def login(payload: schemas.LoginIn, db: Session = Depends(get_db)):
    email = payload.email.lower()
    account = db.query(models.Account).filter(models.Account.email == email).first()
    if not account or not security.verify_password(payload.password, account.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password.")
    return schemas.AccountOut(name=account.name, email=account.email)


# =============================================================================
# PRODUCTS — public catalog (storefront)
# =============================================================================
@app.get("/api/products", response_model=List[schemas.ProductOut])
def list_products(gender: Optional[str] = None, q: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Product)
    if gender and gender != "all":
        query = query.filter(models.Product.gender == gender)
    if q:
        like = f"%{q.lower()}%"
        query = query.filter(models.Product.name.ilike(like))
    return query.order_by(models.Product.popularity.desc()).all()


# =============================================================================
# ORDERS
# =============================================================================
@app.post("/api/orders", response_model=schemas.OrderOut)
def create_order(payload: schemas.OrderCreateIn, db: Session = Depends(get_db)):
    if not payload.items:
        raise HTTPException(status_code=400, detail="Your cart is empty.")
    order = models.Order(
        code=gen_order_code(),
        items=[item.model_dump() for item in payload.items],
        total=payload.total,
        name=payload.name,
        phone=payload.phone,
        address=payload.address,
        account_email=payload.account_email,
        account_name=payload.account_name,
        status="pending",
    )
    db.add(order)
    # bump popularity so best-sellers rise to the top of the storefront
    for item in payload.items:
        product = db.query(models.Product).filter(models.Product.id == item.id).first()
        if product:
            product
