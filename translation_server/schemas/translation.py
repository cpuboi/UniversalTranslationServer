# Translation Schema


from typing import Optional
from pydantic import BaseModel, ValidationError, validator
from translation_server.schemas.languages import LanguageValidator


class InputTranslationModel(BaseModel):
    input_language: Optional[str] = None
    output_language: Optional[str] = None
    input_text: str
    translated_text: Optional[str] = None
    translation_model: Optional[str] = None
    msg: str = ""
    @validator('src_lang', 'dst_lang', check_fields=False)
    def language_must_be_iso(cls, v):
        " ISO 639-1  language code "
        if v not in LanguageValidator.iso_set:
            raise ValueError('Must be ISO-639-1 standard language, en, de, no, fi')
        return v


class ReturnTranslation(BaseModel):
    input_language: Optional[str] = None
    output_language: Optional[str] = None
    translated_text: Optional[str] = None
    translation_model: Optional[str] = None
    msg: Optional[str] = None

