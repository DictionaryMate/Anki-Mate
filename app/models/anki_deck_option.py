from pydantic import BaseModel, Field

from app import config


class _AnkiDeckDuplicateScopeOption(BaseModel):
    deckName: str = Field(default=config.ANKI_DECK_NAME)
    checkChildren: bool = Field(default=False)
    checkAllModels: bool = Field(default=False)


class AnkiDeckOption(BaseModel):
    allowDuplicate: bool = Field(default=False)
    duplicateScope: str = Field(default="deck")
    duplicateScopeOptions: _AnkiDeckDuplicateScopeOption = Field(
        default=_AnkiDeckDuplicateScopeOption()
    )
