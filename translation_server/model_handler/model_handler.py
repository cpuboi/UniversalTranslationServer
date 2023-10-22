"""
The Model Handler is a class that handles several ML language models.

Todo: Add a priority function that will based on translation language use the correct software.
Todo: Unload model from GPU.

TODO: Add several Opus translation handlers
TODO: Map ISO language to all translation modules
"""

import os

import torch

from translation_server.core.config import Settings
from translation_server.log.config import logger
from translation_server.model_handler.models.m2m100.m2m100_handler import M2m100Handler
from translation_server.model_handler.models.nllb.nllb_handler import NLLBHandler
from translation_server.model_handler.models.opus_mt.opus_mt_handler import OpusMtHandler

from translation_server.language_utils.sentence_splitter import sentence_splitter
from translation_server.memory.translation_memory import TranslationMemory


class ModelHandler:
    def __init__(self, device):
        logger.info(f"load models to device {device}")
        self.device = device
        try:
            self.device_name = torch.cuda.get_device_name(self.device)
        except:
            self.device_name = None
        self.m2m100 = False
        self.opus_mt = False
        self.nllb = False
        self.__available_models = set(("nllb", "m2m100", "opus-mt", "default"))
        self.m2m100_loaded = False
        self.opus_mt_loaded = False
        self.nllb_loaded = False
        if Settings.MEMORY: # TODO MOVE THIS OUT
            self.memory = TranslationMemory(Settings.MEMORY_DATABASE)
            logger.info(f"translation memory loaded")
        else:
            self.memory = None

        " Load all models "
        " TODO: Validate paths exist "
        self.m2m100 = M2m100Handler()
        if os.path.exists(Settings.M2M_MODEL_PATH):
            self.m2m100.load_model()
            self.m2m100_loaded = True
            logger.info(f"m2m100 model loaded")
        else:
            logger.info(f"m2m100 model path does not exist: {Settings.M2M_MODEL_PATH}")

        self.opus_mt = OpusMtHandler()
        if os.path.exists(Settings.OPUS_MT_MODEL_PATH):
            self.opus_mt.load_model()
            self.opus_mt_loaded = True
            logger.info(f"Opus model loaded")
        else:
            logger.info(f"opus-mt model path does not exist: {Settings.OPUS_MT_MODEL_PATH}")

        self.nllb = NLLBHandler()
        if os.path.exists(Settings.NLLB_MODEL_PATH):
            self.nllb.load_model()
            self.nllb_loaded = True
            logger.info(f"NLLB model loaded")

        else:
            logger.info(f"nllb model path does not exist: {Settings.NLLB_MODEL_PATH}")

    def __translation_model_exists(self, translation_model):
        if translation_model in self.__available_models:
            return True
        return False


    def translate(self, input_language: str, output_language: str, input_text: str, translation_model: str = "default") -> (
    str, str):
        """

        Translation function
        Will try with opus-mt first, then nllb and lastly m2m100 depending on which model is loaded.

        If memory is set to True in config the check if sentence has been translated before.
            translation_memory first splits the text to sentences
            it then checks whether those sentences have been translated before, if so it uses what is stored in memory.
            Finally re-assemble sentences from memory and machine translated sentences and return string

        TODO: Will need to split up sentences # Memsplit generates same text as non mem split
        TODO: Create a run_translation function
        TODO: Return if reply was cached

        """

        def check_translation_memory(_input_language: str, _output_language: str, _input_text: str, _nlp_model):
            "Check if translation already has been made"
            memory_dict = self.memory.sentence_in_memory(_input_language, _output_language, _input_text, _nlp_model)
            cached = False
            if memory_dict["translated_text"]:
                _translated_text = memory_dict["translated_text"]
                cached = True
            else:  # Memory returned Null, perform translation and add to memory
                if _nlp_model == "opus-mt":
                    _translated_text = self.opus_mt.translate_text(_input_text)
                elif _nlp_model == "nllb":
                    _translated_text = self.nllb.translate_text(_input_language, _output_language, _input_text)
                elif _nlp_model == "m2m100":
                    _translated_text = self.m2m100.translate_text(_input_language, _output_language, _input_text)
                else:
                    _translated_text = ""
                self.memory.add_sentence_to_memory(_input_language,
                                                   _output_language,
                                                   _input_text,
                                                   _translated_text,
                                                   _nlp_model)
            return _translated_text, cached


        if not self.__translation_model_exists(translation_model):
            return "", "", f"Error: select one of these models: {self.__available_models}"

        """
        Start with splitting sentences 
        """
        split_sentences = sentence_splitter(input_text, input_language)
        translated_sentences = []
        cached = False
        cache_counter = 0
        sentence_counter = 0
        cached_pct = 0
        """
        Then feed sentences to one of the models
        """
        if (translation_model == "default" or translation_model == "opus-mt") \
                and self.opus_mt_loaded \
                and input_language == Settings.OPUS_MT_FROM_LANGUAGE \
                and output_language == Settings.OPUS_MT_TO_LANGUAGE:
            """ 
            If translation model is not defined, check if to use opus-mt first since it is efficient.
            If model is loaded and the input and output language is the same as the model file, then translate.
            """
            nlp_model = "opus-mt"
            for sentence in split_sentences:
                sentence_counter += 1
                if self.memory:
                    translated_sentence, cached = check_translation_memory(input_language, output_language, sentence, nlp_model)
                    if cached:
                        cache_counter += 1
                else:
                    translated_sentence = self.opus_mt.translate_text(sentence)
                translated_sentences.append(translated_sentence)
            msg = "ok"

        elif (translation_model == "default" or translation_model == "nllb") and self.nllb_loaded:  # Prioritize NLLB over m2m100
            nlp_model = "nllb"
            for sentence in split_sentences:
                sentence_counter += 1
                if self.memory:
                    translated_sentence, cached = check_translation_memory(input_language, output_language, sentence, nlp_model)
                    if cached:
                        cache_counter += 1
                else:
                    translated_sentence = self.nllb.translate_text(input_language, output_language, sentence)
                translated_sentences.append(translated_sentence)
            msg = "ok"

        elif (translation_model == "default" or translation_model == "m2m100") and self.m2m100_loaded:
            nlp_model = "m2m100"
            for sentence in split_sentences:
                sentence_counter += 1
                if self.memory:
                    translated_sentence, cached = check_translation_memory(input_language, output_language, sentence, nlp_model)
                    if cached:
                        cache_counter += 1
                else:
                    translated_sentence = self.m2m100.translate_text(input_language, output_language, sentence)
                translated_sentences.append(translated_sentence)
            msg = "ok"

        else:
            translated_text = ""
            nlp_model = "Model not loaded"
            msg = f"select translation model: {self.__available_models}"

        translated_text = '. '.join(translated_sentences)  # Re-assemble
        cached_pct = int((cache_counter / sentence_counter) * 100)
        return translated_text, nlp_model, msg, cached_pct

    def list_gpu(self):
        return torch.cuda.is_available()




class MultiGPUHandler:
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
        for device in range(0, self.cuda_devices):
            cuda_name = f"cuda:{device}"
            self.cuda_pool.append(ModelHandler(cuda_name))

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
