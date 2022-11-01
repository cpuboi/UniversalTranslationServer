
"""
The Translation module is a class that handles several ML language models.

Todo: Add a priority function that will based on translation language use the correct software.
Todo: Unload model from GPU.
TODO: Add Pydantic, hm, then again this should be in the web interface
"""

import torch
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer  # M2m100
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM  # opus


class TranslationModule():
    def __init__(self, device):
        self.m2m100_loaded = False
        self.opus_mt_loaded = False
        self.device = device
        try:
            self.device_name = torch.cuda.get_device_name(self.device)
        except:
            self.device_name = None

    def load_m2m100(self, model_path):
        self.m2m100_device = self.device  # Can be cuda:0, cuda:1, cpu
        self.m2m100_model = M2M100ForConditionalGeneration.from_pretrained(model_path)
        self.m2m100_model.to(self.device)  # Load the model to the device, has to fit in RAM.
        self.m2m100_tokenizer = M2M100Tokenizer.from_pretrained(model_path)
        self.m2m100_loaded = True



    def translate_m2m100(self, input_language, output_language, input_text):
        self.m2m100_tokenizer.src_lang = input_language
        __encoded_input_language = self.m2m100_tokenizer(input_text, return_tensors="pt").to(self.device)
        __generated_tokens = self.m2m100_model.generate(**__encoded_input_language, forced_bos_token_id=self.m2m100_tokenizer.get_lang_id(output_language)).to(self.device)
        __translated_text = self.m2m100_tokenizer.batch_decode(__generated_tokens, skip_special_tokens=True)
        return __translated_text


    def load_opus(self, model_path, input_language=None, output_language=None):
        """
        Opus uses a static model with predefined languages.
        opus-mt-ru-en will only translate from Russian to English for example.
        input_language and output_language is only a placeholder to make coding easier.
        """
        self.opus_device = self.device
        self.opus_tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.opus_model = AutoModelForSeq2SeqLM.from_pretrained(model_path).to(self.device)
        self.opus_input_language = input_language
        self.opus_output_language = output_language
        self.opus_loaded = True


    def translate_opus(self, input_text):
        """This code snippet could probably be more beautiful.
        It does what it's supposed to do. It could do with some improvement.
        """
        output_text_list = []

        sentences = input_text.split(". ")
        if input_text == "":
            return ""  # This is an ugly fix
        for sentence in sentences:
            sentence = sentence[:480]  # Truncate characters of the sentence to max 480
            input_ids = self.opus_tokenizer(sentence, return_tensors="pt").to(
                self.device).input_ids
            outputs = self.opus_model.generate(input_ids=input_ids, num_beams=3, num_return_sequences=1)
            translated_text = self.opus_tokenizer.batch_decode(outputs, skip_special_tokens=True)
            output_text_list.append(translated_text[0])
        final_translated_text = '. '.join(output_text_list)
        final_translated_text = self.__opus_blacklist_strings(final_translated_text)
        return final_translated_text


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

    def list_gpu(self):
        return torch.cuda.is_available()


class MultiGPUHandler():
    """
    Handles multi GPU scenarios.
    """
    def __init__(self):
        self.cuda_is_available = torch.cuda.is_available()
        if self.cuda_is_available:
            self.cuda_devices = torch.cuda.device_count()
            self.__create_cuda_pool()
        else:
            self.cuda_devices = 0
        self.__pool_rotator_counter = 0

    def __create_cuda_pool(self):
        self.cuda_pool = []
        for device in range(0,self.cuda_devices):
            cuda_name = f"cuda:{device}"
            self.cuda_pool.append(TranslationModule(cuda_name))



    def pool_load_m2m100(self):
        pass

    def pool_load_opus(self):
        pass

    def pool_get_least_used(self):
        """
        With the help of async, get status of all GPU's in the system.
        """
        pass

    def pool_get_next_in_line(self):
            __gpu_get = self.__pool_rotator_counter % self.cuda_devices
            self.__pool_rotator_counter += 1
            return self.cuda_pool[__gpu_get]



