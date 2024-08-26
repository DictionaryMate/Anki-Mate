from pydantic import BaseModel, Field

from src.app import config
from src.app.models.anki_audio import AnkiAudio
from src.app.models.anki_deck_option import AnkiDeckOption
from src.app.models.anki_field import AnkiField


class AnkiNote(BaseModel):
    fields: AnkiField
    deckName: str = Field(default=config.ANKI_DECK_NAME)
    modelName: str = Field(default=config.ANKI_MODEL_NAME)
    options: AnkiDeckOption = Field(default=AnkiDeckOption())
    tags: list[str] | None = None
    audio: AnkiAudio | None = None
    video: list[dict] | None = None
    picture: list[dict] | None = None
