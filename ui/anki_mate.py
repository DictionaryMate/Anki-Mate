import os
import re

from dotenv import load_dotenv
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.validation import Function
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Log,
    ProgressBar,
    RadioButton,
    RadioSet,
    Static,
)

from app import process_one_word
from ui.models.input_option import InputOptionEnum

load_dotenv()
dictionary_api_key = str(os.getenv("MW_DICT_KEY"))
thesaurus_api_key = str(os.getenv("MW_THE_KEY"))
wordnik_api_key = str(os.getenv("WORDIK_API_KEY"))


class AnkiMate(App):
    input_option: InputOptionEnum = InputOptionEnum.ADD_ONE_WORD
    CSS_PATH = "styles/ankimate.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield ScrollableContainer(
            Static(
                "A list of words should be comma-separated; The file should be in txt format and the content in the file should be a list of words separated by comma",
                id="instruction",
            ),
            RadioSet(
                RadioButton(
                    "Add one word to Anki",
                    id=InputOptionEnum.ADD_ONE_WORD.value,
                ),
                RadioButton(
                    "Add list of words to Anki",
                    id=InputOptionEnum.ADD_LIST_OF_WORDS.value,
                ),
                RadioButton(
                    "Add list of words by txt / csv file to Anki",
                    id=InputOptionEnum.ADD_LIST_OF_WORDS_BY_FILE.value,
                ),
                id="options",
            ),
            Input(
                id="input",
                placeholder="Enter input",
                validate_on=[],
                validators=[Function(self.validate_input, "Invalid input")],
            ),
            ProgressBar(id="progress_bar", show_eta=False),
            Log(id="log", highlight=True),
            Button("Start", id="start_button", variant="primary"),
        )

    def on_mount(self) -> None:
        self._set_init_status()

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        self.input_option = InputOptionEnum(event.pressed.id)
        self._reset_input()

    def on_input_changed(self, event: Input.Changed) -> None:
        self.query_one("#start_button", Button).disabled = not bool(event.value)

    def validate_input(self, value: str) -> bool:
        if self.input_option == InputOptionEnum.ADD_ONE_WORD:
            pattern = r"^[A-Za-z]+$"
            return bool(re.fullmatch(pattern, value))

        if self.input_option == InputOptionEnum.ADD_LIST_OF_WORDS:
            pattern = r"^\s*([A-Za-z]+)(\s*,\s*[A-Za-z]+)*\s*$"
            return bool(re.fullmatch(pattern, value))

        if self.input_option == InputOptionEnum.ADD_LIST_OF_WORDS_BY_FILE:
            path_exists = bool(os.path.exists(value))
            correct_format = value.endswith(".txt")
            return path_exists and correct_format

        return bool(value)

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        input = self.query_one("#input", Input)
        validate_result = input.validate(input.value)
        if not validate_result.is_valid:  # type: ignore
            return

        self._disable_all()
        self._clear_and_hide_log()
        user_input = self.query_one("#input", Input).value
        await self.process(user_input)

        self._reset_input()

    def _disable_all(self) -> None:
        self.query_one("#input", Input).disabled = True
        self.query_one("#start_button", Button).disabled = True
        self.query_one("#options", RadioSet).disabled = True

    def _set_init_status(self) -> None:
        self.query_one("#input", Input).disabled = False
        self.query_one("#start_button", Button).disabled = True
        self.query_one("#options", RadioSet).disabled = False
        self.query_one("#options", RadioSet).query_one(
            f"#{InputOptionEnum.ADD_ONE_WORD.value}", RadioButton
        ).value = True
        self.query_one("#progress_bar", ProgressBar).display = False
        self._clear_and_hide_log()

    def _reset_input(self) -> None:
        self.query_one("#input", Input).disabled = False
        self.query_one("#input", Input).value = ""
        self.query_one("#progress_bar", ProgressBar).display = False
        self.query_one("#options", RadioSet).disabled = False
        self.query_one("#options", RadioSet).focus()

    def _handle_success_result(self) -> None:
        self.query_one("#progress_bar", ProgressBar).display = False
        self.notify("Success")

    def _handle_fail_result(self, error_msg, severity="error") -> None:
        self.query_one("#progress_bar", ProgressBar).display = False
        self.notify(f"Failed: {error_msg}", severity=severity)

    def _handle_list_of_words_fail_result(
        self, failures: list[tuple[str, str]], input_words: list[str]
    ) -> None:
        self.query_one("#progress_bar", ProgressBar).display = False
        self._update_log(failures, input_words)
        if len(failures) < len(input_words):
            self.notify(
                f"{len(input_words) - len(failures)} words failed",
                severity="warning",
            )
        else:
            self.notify("All words failed", severity="error")

    def _clear_and_hide_log(self) -> None:
        self.query_one(Log).clear()
        self.query_one(Log).display = False

    def _update_log(
        self, failures: list[tuple[str, str]], input_words: list[str]
    ) -> None:
        failed_words = [failure[0] for failure in failures]
        self.query_one(Log).write_line(f"Failed words: {failed_words}")
        self.query_one(Log).write_line(f"Input words: {input_words}")
        self.query_one(Log).write_line("\n")
        for failure in failures:
            self.query_one(Log).write_line(f"{failure[0]}: {failure[1]}")
        self.query_one(Log).display = True

    async def _process_word_batch(self, list_of_words: list[str]) -> None:
        failures = []
        progress_bar = self.query_one(ProgressBar)
        progress_bar.update(total=len(list_of_words))
        progress_bar.display = True
        for word in list_of_words:
            try:
                await process_one_word(
                    word, dictionary_api_key, thesaurus_api_key, wordnik_api_key
                )
                progress_bar.advance(1)

            except Exception as e:
                progress_bar.advance(1)
                failures.append((word, str(e)))

        if len(failures) == 0:
            self._handle_success_result()
        else:
            self._handle_list_of_words_fail_result(failures, list_of_words)

    async def process(self, user_input: str) -> None:
        if self.input_option == InputOptionEnum.ADD_ONE_WORD:
            progress_bar = self.query_one(ProgressBar)
            progress_bar.update(total=None)
            progress_bar.display = True

            try:
                await process_one_word(
                    user_input, dictionary_api_key, thesaurus_api_key, wordnik_api_key
                )
                self._handle_success_result()
            except Exception as e:
                self._handle_fail_result(str(e))

        elif self.input_option == InputOptionEnum.ADD_LIST_OF_WORDS:
            list_of_words = user_input.split(",")
            await self._process_word_batch(list_of_words)

        elif self.input_option == InputOptionEnum.ADD_LIST_OF_WORDS_BY_FILE:
            with open(user_input, "r") as f:
                input_words = f.read().split(",")
                await self._process_word_batch(input_words)


if __name__ == "__main__":
    app = AnkiMate()
    result = app.run()
    print(result)
