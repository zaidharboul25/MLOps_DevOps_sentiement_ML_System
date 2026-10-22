from datetime import date

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.database import connect, database_path

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def _entry(row):
    return {"id": row["id"], "content": row["content"], "created_at": row["created_at"]}


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html")


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    with connect(database_path(request)) as connection:
        total = connection.execute("SELECT count(*) FROM texts").fetchone()[0]
        today = connection.execute(
            "SELECT count(*) FROM texts WHERE date(created_at) = ?", (date.today().isoformat(),)
        ).fetchone()[0]
        recent = connection.execute("SELECT * FROM texts ORDER BY id DESC LIMIT 5").fetchall()
    return templates.TemplateResponse(request, "dashboard.html", {"total": total, "today": today, "recent": [_entry(row) for row in recent]})


@router.get("/texts/new", response_class=HTMLResponse)
def new_text(request: Request, error: str | None = None):
    return templates.TemplateResponse(request, "new_text.html", {"error": error})


@router.post("/texts/new")
def submit_text(request: Request, content: str = Form(...)):
    if not content.strip():
        return templates.TemplateResponse(request, "new_text.html", {"error": "Saisissez un texte avant de l’enregistrer.", "content": content}, status_code=422)
    if len(content) > 5000:
        return templates.TemplateResponse(request, "new_text.html", {"error": "Le texte ne peut pas dépasser 5 000 caractères.", "content": content[:5000]}, status_code=422)
    with connect(database_path(request)) as connection:
        cursor = connection.execute("INSERT INTO texts (content) VALUES (?)", (content,))
    return RedirectResponse(f"/texts/{cursor.lastrowid}?saved=1", status_code=303)


@router.get("/history", response_class=HTMLResponse)
def history(request: Request):
    with connect(database_path(request)) as connection:
        rows = connection.execute("SELECT * FROM texts ORDER BY id DESC").fetchall()
    return templates.TemplateResponse(request, "history.html", {"texts": [_entry(row) for row in rows]})


@router.get("/texts/{text_id}", response_class=HTMLResponse)
def detail(request: Request, text_id: int, saved: bool = False):
    with connect(database_path(request)) as connection:
        row = connection.execute("SELECT * FROM texts WHERE id = ?", (text_id,)).fetchone()
    if row is None:
        return templates.TemplateResponse(request, "not_found.html", status_code=404)
    return templates.TemplateResponse(request, "detail.html", {"text": _entry(row), "saved": saved})


@router.post("/texts/{text_id}/delete")
def delete_text_page(request: Request, text_id: int):
    with connect(database_path(request)) as connection:
        connection.execute("DELETE FROM texts WHERE id = ?", (text_id,))
    return RedirectResponse("/history", status_code=303)
