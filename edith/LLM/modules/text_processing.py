import re
import enchant

class TextProcessing:
    def __init__(self):
        self.dictionary = enchant.Dict("en_US")

    def clean_text(self, text: str) -> str:
        """Clean text by correcting misspelled words."""
        cleaned_words = []
        for word in text.split():
            if self.dictionary.check(word):
                cleaned_words.append(word)
            else:
                suggestions = self.dictionary.suggest(word)
                cleaned_words.append(suggestions[0] if suggestions else word)
        return " ".join(cleaned_words).lower()

    def convert_decimal_to_verbal(self, sentence: str) -> str:
        """Convert decimal numbers in a sentence to verbal form."""
        return re.sub(r'\b\d+\.\d+\b', self._replace_decimal, sentence)

    def _replace_decimal(self, match) -> str:
        """Helper method to replace decimal match with verbal representation."""
        number = match.group(0)
        integer_part, decimal_part = number.split('.')
        return f"{integer_part} point {decimal_part}"

    def get_text_after_keyword(self, input_string: str, keyword: str) -> str:
        parts = input_string.split(keyword, 1)
        return parts[1].strip() if len(parts) > 1 else None

    def detect_wake_word(self, transcription: str) -> bool:
        """Detect if the wake word 'edith' is present in the transcription."""
        return "edith" in transcription.lower()
