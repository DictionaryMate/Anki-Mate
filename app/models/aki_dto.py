from pydantic import BaseModel, Field

from app import config
from app.models.anki_action import AnkiAction


class AnkiDto(BaseModel):
    params: dict
    action: AnkiAction
    version: int = Field(default=config.ANKI_CONNECT_VERSION)
