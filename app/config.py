ANKI_CONNECT_VERSION = 6
ANKI_ADDRESS = "http://localhost"
ANKI_PORT = 8765
ANKI_DECK_NAME = "EnglishVocab"
ANKI_MODEL_NAME = "EnglishVocab"


CARD_FIELDS = [
    "word",
    "audio",
    "phonetic",
    "definitions",
    "synonyms",
    "antonyms",
    "etymology",
    "PIEroot",
    "howToUse",
    "picture",
    "testSentence",
]
CARD_CSS = ".card {\n    font-family: arial;\n    font-size: 20px;\n    color: black;\n    background-color: white;\n\t\tline-height: 150%;\n}\n\n.front {\n\ttext-align: center;\n}\n\n.phonetic {\n  text-align: center;\n\tcolor: gray;\n}\n.nightMode .phonetic {\n    color: lightgray;\n}\n\n.synonyms .content {\n\tcolor: green;\n}\n.nightMode .synonyms .content {\n\tcolor: lightgreen;\n}\n\n.antonyms .content {\n\tcolor: orange;\n}\n\n"  # noqa: E501

LEARNING_CARD_FRONT_HTML = '<div class="front">{{word}} {{audio}}</div>'
LEARNING_CARD_BACK_HTML = '<div class="front"><h2>{{FrontSide}}</h2></div>\n\n<hr id=answer>\n\n<div class="phonetic">{{phonetic}}</div>\n<br>\n\n<div class="meaning">\n\t{{definitions}}\n</div>\n\n<hr>\n<div class="synonyms">\n\t<h3>Synonyms</h3>\n\t<div class="content">\n\t\t{{synonyms}}\n\t</div>\n</div>\n\n<div class="antonyms">\n\t<h3>Antonyms</h3>\n\t<div class="content">\n\t\t{{antonyms}}\n\t</div>\n</div>\n\n<hr>\n<div class="etymology">\n\t<h3>Etymology</h3>\n\t{{etymology}}\n\t\n\t<h4>PIE Root</h4>\n\t{{PIEroot}}\n\n</div>\n<hr>\n\n<div class="notes">\n\t<h3>How To Use</h3>\n\t{{howToUse}}\n</div>\n\n<hr>\n{{picture}}\n'  # noqa: E501

TESTING_FRONT_HTML = "{{testSentence}}"
TESTING_BACK_HTML = '<div>{{testSentence}}</div>\n<hr id=answer>\n<div class="front"><h2>{{word}} {{audio}}</h2></div>\n\n<hr>\n\n<div class="phonetic">{{phonetic}}</div>\n<br>\n\n<div class="meaning">\n\t{{definitions}}\n</div>\n\n<hr>\n<div class="synonyms">\n\t<h3>Synonyms</h3>\n\t<div class="content">\n\t\t{{synonyms}}\n\t</div>\n</div>\n\n<div class="antonyms">\n\t<h3>Antonyms</h3>\n\t<div class="content">\n\t\t{{antonyms}}\n\t</div>\n</div>\n\n<hr>\n<div class="etymology">\n\t<h3>Etymology</h3>\n\t{{etymology}}\n\n\t<h3>PIE Root</h3>\n\t{{PIEroot}}\n</div>\n<hr>\n\n<div class="notes">\n\t<h3>How To Use</h3>\n\t{{howToUse}}\n</div>\n\n<hr>\n{{picture}}'  # noqa: E501
