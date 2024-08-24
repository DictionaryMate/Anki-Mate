from dictionary_wrapper import get_word_field_async  # type: ignore

from app.anki_clients.client import AnkiClient
from app.anki_clients.utils import convert_word_to_anki_format
from app.exceptions import AnkiClientException
from app.logger import Logger

logger = Logger()


async def process_one_word(
    word: str, dictionary_api_key: str, thesaurus_api_key: str, wordnik_api_key: str
):
    field = await get_word_field_async(
        word, dictionary_api_key, thesaurus_api_key, wordnik_api_key
    )
    anki_note = convert_word_to_anki_format(field)

    anki_client = AnkiClient()

    try:
        note_id = anki_client.create_note(anki_note)
    except AnkiClientException as e:
        logger.log_error(e)
        return None

    return note_id
