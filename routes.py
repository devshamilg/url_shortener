from fastapi import APIRouter, HTTPException
from scemas import URLRequest
from database import DBSession, URL
from nanoid import generate
from sqlalchemy import select
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.post("/shorten")
def shorten_url(url: URLRequest, session: DBSession):
    code = generate(size=6)
    new_url = URL(short_code = code, original_url = url.long_url)
    session.add(new_url)
    session.commit()
    session.refresh(new_url)
    return {
        "short_url": f"http://127.0.0.1:8000/{new_url.short_code}"
    }   

@router.get("/{code}")
def redirect(code: str, session: DBSession):
    stmt = select(URL).where(URL.short_code==code)
    url = session.execute(stmt).scalar_one_or_none()

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    return RedirectResponse(url.original_url)

