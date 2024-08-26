from datetime import datetime

from dictionary_wrapper.models.common_models import WordField  # type: ignore

from src.app import config
from src.app.exceptions import AnkiClientException
from src.app.models.aki_dto import AnkiDto
from src.app.models.anki_action import AnkiAction
from src.app.models.anki_audio import AnkiAudio
from src.app.models.anki_field import AnkiField
from src.app.models.anki_note import AnkiNote


def handle_response(response: dict):
    if len(response) != 2:
        raise AnkiClientException("response has an unexpected number of fields")
    if "error" not in response:
        raise AnkiClientException("response is missing required error field")
    if "result" not in response:
        raise AnkiClientException("response is missing required result field")
    if response["error"] is not None:
        raise AnkiClientException(response["error"])
    return response["result"]


def form_payload(action: AnkiAction, **params):
    return AnkiDto(params=params, action=action).model_dump_json()


def get_card_templates():
    return [
        {
            "Name": "Learning Card",
            "Front": config.LEARNING_CARD_FRONT_HTML,
            "Back": config.LEARNING_CARD_BACK_HTML,
        },
        {
            "Name": "Testing Card",
            "Front": config.TESTING_FRONT_HTML,
            "Back": config.TESTING_BACK_HTML,
        },
    ]


def convert_word_to_anki_format(word: WordField) -> AnkiNote:
    def_dicts = [d.model_dump() for d in word.definitions]
    def_strs = ["<br>".join(d.values()) for d in def_dicts]
    def_str = "<br><br>".join(def_strs)
    syn_str = "; ".join(
        [
            f"{syn.partOfSpeech}: {syn.words}"
            for syn in word.synonyms
            if len(syn.words) > 0
        ]
    )
    ant_str = "; ".join(
        [
            f"{ant.partOfSpeech}: {ant.words}"
            for ant in word.antonyms
            if len(ant.words) > 0
        ]
    )
    test_sentences = "<br><br>".join(
        [
            f"{sentence.replace(word.word, '_______')}"
            for sentence in word.exampleSentences
        ]
    )

    anki_field = AnkiField(
        word=word.word,
        phonetic=word.phonetic,
        definitions=def_str,
        synonyms=syn_str,
        antonyms=ant_str,
        etymology="<br>".join(word.etymologies),
        testSentence=test_sentences,
        picture="",
    )
    file_name = f"{word.word}_{datetime.now().strftime('%s')}.mp3"
    anki_audio = AnkiAudio(url=word.audioLink, filename=file_name, fields=["phonetic"])
    anki_note = AnkiNote(fields=anki_field, audio=anki_audio)

    return anki_note
