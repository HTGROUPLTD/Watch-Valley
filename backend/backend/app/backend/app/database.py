from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite file lives alongside the app — zero setup required.
# For production, swap this for a real Postgres URL, e.g.:
#   postgresql://user:password@host:5432/watch_valley
SQLALCHEMY_DATABASE_URL = "sqlite:///./watch_valley.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
