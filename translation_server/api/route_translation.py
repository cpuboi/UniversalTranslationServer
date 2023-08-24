from fastapi import APIRouter
from translation_server.core.config import Settings
from translation_server.model_handler.translation_handler import translation_processor
from translation_server.schemas.translation import ReturnTranslation, InputTranslationModel
from translation_server.model_handler.model_handler import ModelHandler
from translation_server.api import messages
router = APIRouter()

translationModule = ModelHandler(device=Settings.DEVICE_LIST[0])


@router.post("/", response_model=ReturnTranslation)
def translate_text(input_model: InputTranslationModel):
    translation = translation_processor(input_model, translationModule)
    return translation

@router.get("/")
def get_default_site():
    usage = messages.message_howto
    return usage

