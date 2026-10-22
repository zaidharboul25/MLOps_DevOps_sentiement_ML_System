from dataclasses import dataclass


@dataclass(frozen=True)
class TextEntry:
    id: int
    content: str
    created_at: str
