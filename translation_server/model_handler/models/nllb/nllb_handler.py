" Nllb base class and functions "

import torch
from translation_server.log.config import logger
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from translation_server.core.config import Settings
from translation_server.model_handler.models.nllb.languages import nllb_language_set



class NLLBHandler:
    """
    Handler for all translation models.
    """
    def __init__(self, device: str = Settings.DEVICE_LIST[0]):
        self.device = device
        try:
            self.device_name = torch.cuda.get_device_name(self.device)
        except Exception as e:

            self.device_name = None
        self.model_path = Settings.NLLB_MODEL_PATH
        self.model_loaded = False
        self.model = None
        self.languages = nllb_language_set
        self.tokenizers = {}

    def load_model(self):
        "Loads model"
        try:
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_path, use_auth_token=True)
            self.model_loaded = True
        except Exception as e:
            logger.error("could not load model ", e)
            self.model_loaded = True

    def get_tokenizer(self, input_language: str):
        " Is input_language a valid string?"
        if input_language in self.languages:
            if input_language not in self.tokenizers:  # input_language has not been tokenized before
                self.tokenizers[input_language] = AutoTokenizer.from_pretrained(self.model_path,
                                                                                use_auth_token=True,
                                                                                src_lang=input_language)
            return self.tokenizers[input_language]  # Tokenizer exists, return
        else:
            raise ValueError(f" {input_language} is not a valid language for NLLB")

    def translate_text(self, input_language: str, output_language: str, input_text: str):
        """ Translate text based on input_language and output language.
        translate_text first checks if the input language has been tokenized with the get_tokenizer function
            if not then tokenize and add to: self.tokenizers
        """

        tokenizer = self.get_tokenizer(input_language)

        inputs = tokenizer(input_text, return_tensors="pt")
        translated_tokens = self.model.generate(**inputs,
                                                forced_bos_token_id=tokenizer.lang_code_to_id[output_language],
                                                max_length=Settings.NLLB_TEXT_LIMIT)

        output_text = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
        return output_text

