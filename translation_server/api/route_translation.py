from fastapi import APIRouter
from translation_server.core.config import Settings
from translation_server.model_handler.translation_handler import translation_processor
from translation_server.schemas.translation import ReturnTranslation, InputTranslationModel
from translation_server.model_handler.translation_module import TranslationModule
router = APIRouter()

translationModule = TranslationModule(device=Settings.DEVICELIST[0])
translationModule.load_m2m100(model_path=Settings.m2m_model_path)

@router.post("/", response_model=ReturnTranslation)
def translate_text(input_model: InputTranslationModel):
    translation = translation_processor(input_model, translationModule)
    return translation
