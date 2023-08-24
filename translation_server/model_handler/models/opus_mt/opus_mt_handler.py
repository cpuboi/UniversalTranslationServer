" Nllb base class and functions "

import torch
from translation_server.log.config import logger
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from translation_server.core.config import Settings

"""
https://huggingface.co/Helsinki-NLP/opus-mt-ru-en
https://huggingface.co/Helsinki-NLP/opus-mt-da-en
"""



class OpusMtHandler:
    def __init__(self, device: str = Settings.DEVICE_LIST[0]):
        self.device = device
        try:
            self.device_name = torch.cuda.get_device_name(self.device)
        except:
            self.device_name = None
        self.model_path = Settings.OPUS_MT_MODEL_PATH
        self.model = None
        self.tokenizer = None
        self.languages = ""
        self.model_loaded = False


    def load_model(self):
        """
        Opus uses a static model with predefined languages.
        opus-mt-dk-en will for example only translate from Danish to English.
        """
        self.opus_device = self.device
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_path).to(self.device)
        self.model_loaded = True


    def translate_text(self, input_text):
        """
        This code snippet could probably be more beautiful.
        It does what it's supposed to do. It could do with some improvement.
        """
        output_text_list = []

        sentences = input_text.split(". ")
        if input_text == "":
            return ""  # This is an ugly fix
        for sentence in sentences:
            sentence = sentence[:400]  # Truncate characters of the sentence to max length 400
            input_ids = self.tokenizer(sentence, return_tensors="pt").to(
                self.device).input_ids
            outputs = self.model.generate(input_ids=input_ids, num_beams=3, num_return_sequences=1, max_new_tokens=Settings.OPUS_MT_MAX_TOKENS)
            translated_text = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)
            output_text_list.append(translated_text[0])

        return self.__opus_blacklist_strings('. '.join(output_text_list))


    def __opus_blacklist_strings(self, in_string):
        """Opus has problems translating certain characters which results in repetitions of the following strings.
        This is probably not the most efficient way of doing this either. """
        blacklist_string_list = [
            "yeah, yeah,",
            "You're gonna get it. You're gonna get it.",
            "We're gonna have to get you out of here. We're gonna get you out of here.",
            "and I'm gonna get you out of here, and I'm gonna get you out of here, ",
            "okay, okay, ",
            "It's okay. It's okay,",
            "it's okay, it's okay.",
            "I'm sorry. I'm sorry.",
            "ooh, ooh, ",
            "whoa, whoa, whoa, ",
            "I'm in the middle of it. I'm in the middle of it.",
            "like, like, ",
            "you, you, ",
            "oh, oh, ",
            "hey, hey, ",
            "uh, uh, uh, ",
            "♪ I'm in the middle of it ♪",
            "♪ I've got my hands full ♪",
            "♪ I'm gonna go with you ♪",
            "We're gonna do this. We're gonna do this.",
            "OH-OH-",
            "uh-uh-",
            "JOHN, JOHN, ",
            "FUTURE, FUTURE,",
            "FREE, FREE, ",
            "u-u-u-",
            "O-O-O-",
            ".  ",
            "THOSE THOSE ",
            "hhhh"
        ]
        for item in blacklist_string_list:
            in_string = in_string.replace(item, "")
        return in_string

