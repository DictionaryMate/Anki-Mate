import asyncio
import os

from dotenv import load_dotenv

from src.app import process_one_word

load_dotenv()
dictionary_api_key = os.getenv("MW_DICT_KEY")
thesaurus_api_key = os.getenv("MW_THE_KEY")
wordnik_api_key = os.getenv("WORDIK_API_KEY")

word = "idiosyncrasy"

asyncio.run(
    process_one_word(
        word,
        dictionary_api_key,  # type: ignore
        thesaurus_api_key,  # type: ignore
        wordnik_api_key,  # type: ignore
    )
)
