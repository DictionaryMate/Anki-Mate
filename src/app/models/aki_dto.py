from pydantic import BaseModel, Field

from src.app import config
from src.app.models.anki_action import AnkiAction


class AnkiDto(BaseModel):
    params: dict
    action: AnkiAction
    version: int = Field(default=config.ANKI_CONNECT_VERSION)
