
import re
import nltk
from translation_server.core.config import Settings
from translation_server.schemas.languages import LanguageValidator
nltk.data.path = [Settings.NLTK_DATA_PATH]


def sentence_splitter(input_text, language_iso):
    """

    Takes an input text and returns a list of sentences.

    First remove newlines
    Version 0.1
        * Splits on ". "

    Todo: Split on other languages (chinese regex)
    Todo: Dont split if previous character is an abbreviation

    """

    input_text = input_text.replace("\n", " ") # Remove newlines
    input_text = input_text.replace("\t", " ") # Remove tabs
    input_text = input_text.replace("\r", " ") # Remove newlines


    try:  # nltk
        """
        Try and replace the language iso string to language string that nltk wants,
        It wants "english" not "en"
        """
        language_string = LanguageValidator.languages_iso_rev[language_iso]
        sentences = nltk.tokenize.sent_tokenize(input_text, language=language_string.lower())
        return sentences
    except LookupError: # Could not find language, try regex
        chinese_regex = "[^!?。\.\!\?]+[!?。\.\!\?]?"
        regular_regex = "(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s"
        if language_iso == "zh":
            return [s.strip() for s in re.split(chinese_regex, input_text)]
        else:
            return [s.strip() for s in re.split(regular_regex, input_text)]

    except:  # Super simple cant fail :^)
        return input_text.split(". ")

