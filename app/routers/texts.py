import sqlite3

from fastapi import APIRouter, HTTPException, Request, Response, status

from app.database import connect, database_path
from app.schemas import TextCreate, TextRead

router = APIRouter(prefix="/api/texts", tags=["texts"])


def _read(row: sqlite3.Row) -> TextRead:
    return TextRead(id=row["id"], content=row["content"], created_at=row["created_at"])


@router.get("", response_model=list[TextRead])
def list_texts(request: Request, limit: int = 100, offset: int = 0) -> list[TextRead]:
    if limit < 1 or limit > 500 or offset < 0:
        raise HTTPException(status_code=422, detail="limit doit être entre 1 et 500 et offset positif.")
    with connect(database_path(request)) as connection:
        rows = connection.execute(
            "SELECT id, content, created_at FROM texts ORDER BY id DESC LIMIT ? OFFSET ?", (limit, offset)
        ).fetchall()
    return [_read(row) for row in rows]


@router.post("", response_model=TextRead, status_code=status.HTTP_201_CREATED)
def create_text(payload: TextCreate, request: Request) -> TextRead:
    with connect(database_path(request)) as connection:
        cursor = connection.execute("INSERT INTO texts (content) VALUES (?)", (payload.content,))
        row = connection.execute(
            "SELECT id, content, created_at FROM texts WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
    return _read(row)


@router.get("/{text_id}", response_model=TextRead)
def get_text(text_id: int, request: Request) -> TextRead:
    with connect(database_path(request)) as connection:
        row = connection.execute(
            "SELECT id, content, created_at FROM texts WHERE id = ?", (text_id,)
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Texte introuvable.")
    return _read(row)


@router.delete("/{text_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_text(text_id: int, request: Request) -> Response:
    with connect(database_path(request)) as connection:
        cursor = connection.execute("DELETE FROM texts WHERE id = ?", (text_id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Texte introuvable.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
