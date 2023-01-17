" Nllb base class and functions "

import torch
from translation_server.log.config import logger
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer  # M2m100

from translation_server.core.config import Settings
"""
TODO: Rename input_language"""


class M2m100Handler:
    def __init__(self, device: str = Settings.DEVICE_LIST[0]):
        self.device = device
        try:
            self.device_name = torch.cuda.get_device_name(self.device)
        except:
            self.device_name = None
        self.model_path = Settings.M2M_MODEL_PATH
        self.model_loaded = False
        self.model = None
        self.languages = ()
        self.tokenizers = {}


    def load_model(self):
        self.model = M2M100ForConditionalGeneration.from_pretrained(self.model_path)
        self.model.to(self.device)  # Load the model to the device, has to fit in RAM.
        self.tokenizer = M2M100Tokenizer.from_pretrained(self.model_path)
        self.model_loaded = True

    def translate_text(self, input_language, output_language, input_text):
        self.tokenizer.src_lang = input_language
        __encoded_input_language = self.tokenizer(input_text, return_tensors="pt").to(self.device)
        __generated_tokens = self.model.generate(**__encoded_input_language,
                                                 forced_bos_token_id=self.tokenizer.get_lang_id(output_language),
                                                 max_new_tokens=Settings.M2M_MAX_TOKENS).to(self.device)
        __translated_text = self.tokenizer.batch_decode(__generated_tokens, skip_special_tokens=True)[0]
        return __translated_text

