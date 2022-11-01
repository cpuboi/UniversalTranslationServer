from translation_server.schemas.translation import InputTranslationModel
from translation_server.schemas.languages import LanguageValidator
"""

"""


def translation_processor(input_model: InputTranslationModel, TranslationModule):
    # send model to ML process.
    try:
        LanguageValidator.language_iso_check(LanguageValidator.iso_set, input_model.input_language)
        LanguageValidator.language_iso_check(LanguageValidator.iso_set, input_model.output_language)
    except AttributeError as e:
        return {"msg": f"ERROR: {e}"}
    except ValueError as e:
        return {"msg": f"ERROR: {e}"}
    input_model.translated_text = TranslationModule.translate_m2m100(input_model.input_language,
                                                                     input_model.output_language,
                                                                     input_model.input_text)[0]
    input_model.msg = "ok"
    return input_model
