from pydantic import BaseModel


class AnkiField(BaseModel):
    word: str
    phonetic: str
    definitions: str
    synonyms: str
    antonyms: str
    etymology: str
    PIEroot: str | None = ""
    howToUse: str | None = ""
    testSentence: str
    picture: str | None = ""
