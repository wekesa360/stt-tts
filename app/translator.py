from transformers import pipeline
import json
import re


with open("phrase_mappings.json", "r") as f:
    phrase_mapping = json.load(f)


class UnifiedTranslator:
    def __init__(self, model_name, phrase_mapping):
        self.model = pipeline("translation", model=model_name)
        self.phrase_mapping = phrase_mapping

    def translate(self, text):
        text_lower = text.lower().strip()
        print(f"Input text: {text_lower}")

        # Check if the text matches any pattern in the phrase_mapping (English to Swahili)
        for pattern, translation in self.phrase_mapping.items():
            try:
                pattern_regex = re.compile(
                    re.escape(pattern).replace(r"\{name\}", r"([\w'-]+)").strip(),
                    re.IGNORECASE,
                )
                print(f"Checking pattern: {pattern}")
                match = pattern_regex.fullmatch(text_lower)
                if match:
                    print(f"Match found: {match.group(0)}")
                    if "{name}" in pattern:
                        return translation.format(name=match.group(1))
                    else:
                        return translation
            except re.error as e:
                print(f"Regex error with pattern {pattern}: {e}")
        try:
            print(f"Fallback to model translation for text: {text}")
            translation = self.model(text)[0]
            return translation["translation_text"]
        except Exception as e:
            print(f"Model translation error: {e}")
            return "Translation error occurred"


english_to_swahili = UnifiedTranslator(
    "Bildad/English-Swahili_Translation", phrase_mapping
)
swahili_to_english = UnifiedTranslator(
    "Bildad/Swahili-English_Translation", phrase_mapping
)


def en_to_sw(text):
    return english_to_swahili.translate(text)


def sw_to_en(text):
    return swahili_to_english.translate(text)
