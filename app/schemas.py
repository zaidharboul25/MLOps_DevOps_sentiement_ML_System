from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class TextCreate(BaseModel):
    content: str = Field(min_length=1, max_length=5000)

    @field_validator("content")
    @classmethod
    def content_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Le texte ne peut pas être vide.")
        return value


class TextRead(BaseModel):
    id: int
    content: str
    created_at: datetime
