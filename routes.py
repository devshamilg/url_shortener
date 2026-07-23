from fastapi import APIRouter, HTTPException, Request
from scemas import URLRequest
from database import DBSession, URL
from nanoid import generate
from sqlalchemy import select
from fastapi.responses import RedirectResponse
from services.rate_limiter import check_rate_limit

router = APIRouter()

@router.post("/shorten")
def shorten_url(url: URLRequest, session: DBSession, request: Request):

    check_rate_limit(request)

    stmt = select(URL).where(URL.original_url == url.long_url)
    existing_url = session.execute(stmt).first()

    if existing_url:
        return {
            "short_url": f"http://127.0.0.1:8000/{existing_url.short_code}"
        }
    
    if url.custom_alias:
        stmt = select(URL).where(URL.short_code == url.custom_alias)
        existing_alias = session.execute(stmt).first()
        if existing_alias:
            raise HTTPException(status_code=400, detail="Custom alias already exists")
        code = url.custom_alias
    else:
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
    
    url.click_count += 1
    session.commit()

    return RedirectResponse(url.original_url)

