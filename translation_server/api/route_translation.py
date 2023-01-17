from fastapi import APIRouter
from translation_server.core.config import Settings
from translation_server.model_handler.translation_handler import translation_processor
from translation_server.schemas.translation import ReturnTranslation, InputTranslationModel
from translation_server.model_handler.model_handler import ModelHandler
router = APIRouter()

translationModule = ModelHandler(device=Settings.DEVICE_LIST[0])


@router.post("/", response_model=ReturnTranslation)
def translate_text(input_model: InputTranslationModel):
    translation = translation_processor(input_model, translationModule)
    return translation

@router.get("/")
def get_default_site():
    usage = {"HOWTO": "POST these fields to localhost:7890/translate",
             "input_language": "ru",
             "output_language": "en",
             "input_text": "ВГР — это тип высокотемпературного реактора (ВТР), который теоретически может иметь температуру на выходе 1000 °C",
             "translation_model": "One of: default, opus-mt, nllb, m2m100"}
    return usage
