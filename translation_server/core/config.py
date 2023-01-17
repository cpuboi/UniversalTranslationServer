

class Settings:
    PROJECT_NAME: str = "Translation Server"
    PROJECT_VERSION: str = "0.0.2"
    FASTAPI_PORT: int = 7890
    DEVICE_LIST: list = ["cpu"]

    #M2M_MODEL_PATH: str = "/models/m2m100"  # Add full path
    M2M_MODEL_PATH: str = "/home/user/projects/ai/models/facebook/m2m100_418M"
    M2M_MAX_TOKENS: int = 512  # Needs tweaking

    # TODO: Before NLLB works a converter between the "input language abbreviations" of NLLB to the ISO standard is required.
    NLLB_MODEL_PATH: str = "X/home/user/projects/ai/models/nllb/nllb-200-distilled-600M"
    NLLB_TEXT_LIMIT: int = 800  # To stop excessive input

    OPUS_MT_MODEL_PATH: str = "/home/user/projects/ai/models/Helsinki-NLP/opus-mt-ru-en"  # Only one language at a time
    OPUS_MT_MAX_TOKENS: int = 512 # Needs tweaking
    OPUS_MT_FROM_LANGUAGE: str = OPUS_MT_MODEL_PATH.strip("/").split("/")[-1].split("-")[-2]  # get the second last ISO name
    OPUS_MT_TO_LANGUAGE: str = OPUS_MT_MODEL_PATH.strip("/").split("/")[-1].split("-")[-1] # Get the last ISO name


