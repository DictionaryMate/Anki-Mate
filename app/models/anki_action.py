from enum import Enum


class AnkiAction(Enum):
    ADD_NOTE = "addNote"
    FIND_NOTES = "findNotes"
    GET_DECK_NAMES = "deckNames"
    CREATE_DECK = "createDeck"
    GET_MODEL_NAMES = "modelNames"
    CREATE_MODEL = "createModel"
