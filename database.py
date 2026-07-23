import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column
from sqlalchemy import String
from typing import Annotated
from fastapi import Depends
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

class Base(DeclarativeBase):
    pass

class URL(Base):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(primary_key=True)

    short_code: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        index=True,
    )

    original_url: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    click_count: Mapped[int] = mapped_column(default=0)

def get_db():
    with Session(engine) as session:
        yield session

DBSession = Annotated[Session, Depends(get_db)]
