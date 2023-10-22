from translation_server.schemas.translation import InputTranslationModel
from translation_server.schemas.languages import LanguageValidator
from translation_server.model_handler.model_handler import ModelHandler

"""
Handles translation requests and sends them to the model handler. 
"""


def translation_processor(input_model: InputTranslationModel, model_handler: ModelHandler):
    # send model to ML process.
    try:
        LanguageValidator.language_iso_check(LanguageValidator.iso_set, input_model.input_language)
        LanguageValidator.language_iso_check(LanguageValidator.iso_set, input_model.output_language)
    except AttributeError as e:
        return {"msg": f"ERROR: {input_model.input_language} {e}"}
    except ValueError as e:
        return {"msg": f"ERROR: {input_model.output_language} {e}"}

    translated_text, nlp_model, msg, cached = model_handler.translate(input_model.input_language,
                                input_model.output_language,
                                input_model.input_text,
                                input_model.translation_model)
    input_model.translation_model = nlp_model
    input_model.translated_text = translated_text
    input_model.msg = msg
    input_model.cached_pct = cached

    return input_model

