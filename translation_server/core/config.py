

class Settings:
    PROJECT_NAME: str = "Translation Server"
    PROJECT_VERSION: str = "0.0.4"
    FASTAPI_PORT: int = 7890
    DEVICE_LIST: list = ["cuda:0"]  # cuda:0 for Nvidia GPU , "cpu" for cpu
    #DEVICE_LIST: list = ["cpu"]  # cuda:0 for Nvidia GPU , "cpu" for cpu

    M2M_MODEL_PATH: str = "/models/facebook/m2m100_1.2B"
    M2M_MAX_TOKENS: int = 512  # Needs tweaking

    # TODO: Before NLLB works a converter between the "input language abbreviations" of NLLB to the ISO standard is required.
    NLLB_MODEL_PATH: str = "/models/nllb/nllb-200-distilled-600M"
    NLLB_TEXT_LIMIT: int = 800  # To stop excessive input

    OPUS_MT_MODEL_PATH: str = "/models/Helsinki-NLP/opus-mt-ru-en"  # Only one language at a time
    OPUS_MT_MAX_TOKENS: int = 512 # Needs tweaking
    OPUS_MT_FROM_LANGUAGE: str = OPUS_MT_MODEL_PATH.strip("/").split("/")[-1].split("-")[-2]  # get the second last ISO name
    OPUS_MT_TO_LANGUAGE: str = OPUS_MT_MODEL_PATH.strip("/").split("/")[-1].split("-")[-1] # Get the last ISO name


    # Memory that stores all sentence translations
    # If you translate the same type of documents over and over this will save time.
    # All translations are stored, not ideal for privacy.
    MEMORY: bool = True
    MEMORY_DATABASE = "/models/translation_memory.db"  # Piggybacking on the models dir..
    #MEMORY_DATABASE = ":memory:"  # Put the memory in RAM, this is better for privacy but will not persist


    NLTK_DATA_PATH: str = "translation_server/external_data/nltk/"
