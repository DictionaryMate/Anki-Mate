import os

from dictionary_wrapper import get_word_field_async  # type: ignore

from app.anki_clients.client import AnkiClient
from app.anki_clients.utils import convert_word_to_anki_format
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

    note_id = anki_client.create_note(anki_note)

    return note_id


async def process_words(
    words: list[str],
    dictionary_api_key: str,
    thesaurus_api_key: str,
    wordnik_api_key: str,
) -> list[tuple[str, str]]:
    # failures is a list of word-failed_reason tupple
    failures = []
    for word in words:
        try:
            await process_one_word(
                word, dictionary_api_key, thesaurus_api_key, wordnik_api_key
            )
        except Exception as e:
            failures.append((word, str(e)))

    return failures


async def process_file(
    file_path: str,
    dictionary_api_key: str,
    thesaurus_api_key: str,
    wordnik_api_key: str,
):
    if not os.path.exists(file_path):
        raise Exception("File not found")

    # check if file is txt
    if not file_path.endswith(".txt"):
        raise Exception("File format not supported")

    # the content in the file is a list of words separated by comma
    with open(file_path, "r") as f:
        words = f.read().split(",")

    failed_words = await process_words(
        words, dictionary_api_key, thesaurus_api_key, wordnik_api_key
    )

    return failed_words, words
