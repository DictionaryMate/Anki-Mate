import requests

from app import config
from app.anki_clients.utils import form_payload, get_card_templates, handle_response
from app.exceptions import AnkiClientException
from app.models.anki_action import AnkiAction
from app.models.anki_note import AnkiNote


class AnkiClient:
    def __init__(self) -> None:
        self.base_url = f"{config.ANKI_ADDRESS}:{config.ANKI_PORT}"

    def __request(self, action: AnkiAction, **params):
        payload = form_payload(action, **params)
        try:
            request = requests.post(self.base_url, data=payload)
        except requests.exceptions.ConnectionError:
            raise AnkiClientException(
                "Unable to connect to Anki. Please make sure Anki is running and AnkiConnect is installed correctly"
            )

        if request.status_code != 200:
            raise AnkiClientException(
                f"Error happened while requesting. Status code: {request.status_code}; Content: {request.content.decode('utf-8')}"
            )
        return handle_response(request.json())

    def health_check(self) -> dict:
        self.get_deck_names()
        return {"result": "success"}

    def is_duplicate(self, word) -> bool:
        return (
            len(
                self.__request(
                    AnkiAction.FIND_NOTES,
                    query=f"deck:{config.ANKI_DECK_NAME} word:{word}",
                )
            )
            > 0
        )

    def add_note(self, note: AnkiNote) -> int:
        note_payload = {"note": note.model_dump()}
        return self.__request(AnkiAction.ADD_NOTE, **note_payload)

    def get_deck_names(self) -> list[str]:
        return self.__request(AnkiAction.GET_DECK_NAMES)

    def create_deck(self, deck_name: str = config.ANKI_DECK_NAME) -> int | None:
        deck_names = self.get_deck_names()
        if deck_name not in deck_names:
            return self.__request(AnkiAction.CREATE_DECK, deck=deck_name)

        return None

    def get_model_names(self) -> list[str]:
        return self.__request(AnkiAction.GET_MODEL_NAMES)

    def create_model(self, model_name: str = config.ANKI_MODEL_NAME) -> dict | None:
        model_names = self.get_model_names()
        if model_name not in model_names:
            card_templates = get_card_templates()
            return self.__request(
                AnkiAction.CREATE_MODEL,
                modelName=config.ANKI_MODEL_NAME,
                inOrderFields=config.CARD_FIELDS,
                css=config.CARD_CSS,
                isCloze=False,
                cardTemplates=card_templates,
            )

        return None

    def create_note(self, note: AnkiNote) -> int:
        self.create_deck()
        self.create_model()
        return self.add_note(note)
