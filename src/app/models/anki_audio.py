from pydantic import BaseModel


class AnkiAudio(BaseModel):
    url: str
    filename: str
    fields: list[str]
