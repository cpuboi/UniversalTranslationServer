from pydantic import BaseModel


class LanguageValidator:
    languages_iso: dict = {"Afrikaans": "af", "Amharic": "am", "Arabic": "ar", "Asturian": "ast", "Azerbaijani": "az",
                           "Bashkir": "ba", "Belarusian": "be", "Bulgarian": "bg", "Bengali": "bn", "Breton": "br",
                           "Bosnian": "bs", "Catalan; Valencian": "ca", "Cebuano": "ceb", "Czech": "cs", "Welsh": "cy",
                           "Danish": "da", "German": "de", "Greeek": "el", "English": "en", "Spanish": "es",
                           "Estonian": "et", "Persian": "fa", "Fulah": "ff", "Finnish": "fi", "French": "fr",
                           "Western Frisian": "fy", "Irish": "ga", "Gaelic; Scottish Gaelic": "gd", "Galician": "gl",
                           "Gujarati": "gu", "Hausa": "ha", "Hebrew": "he", "Hindi": "hi", "Croatian": "hr",
                           "Haitian; Haitian Creole": "ht", "Hungarian": "hu", "Armenian": "hy", "Indonesian": "id",
                           "Igbo": "ig", "Iloko": "ilo", "Icelandic": "is", "Italian": "it", "Japanese": "ja",
                           "Javanese": "jv", "Georgian": "ka", "Kazakh": "kk", "Central Khmer": "km", "Kannada": "kn",
                           "Korean": "ko", "Luxembourgish; Letzeburgesch": "lb", "Ganda": "lg", "Lingala": "ln",
                           "Lao": "lo", "Lithuanian": "lt", "Latvian": "lv", "Malagasy": "mg", "Macedonian": "mk",
                           "Malayalam": "ml", "Mongolian": "mn", "Marathi": "mr", "Malay": "ms", "Burmese": "my",
                           "Nepali": "ne", "Dutch; Flemish": "nl", "Norwegian": "no", "Northern Sotho": "ns",
                           "Occitan": "post 1500", "Oriya": "or", "Panjabi; Punjabi": "pa", "Polish": "pl",
                           "Pushto; Pashto": "ps", "Portuguese": "pt", "Romanian; Moldavian; Moldovan": "ro",
                           "Russian": "ru", "Sindhi": "sd", "Sinhala; Sinhalese": "si", "Slovak": "sk",
                           "Slovenian": "sl",
                           "Somali": "so", "Albanian": "sq", "Serbian": "sr", "Swati": "ss", "Sundanese": "su",
                           "Swedish": "sv", "Swahili": "sw", "Tamil": "ta", "Thai": "th", "Tagalog": "tl",
                           "Tswana": "tn",
                           "Turkish": "tr", "Ukrainian": "uk", "Urdu": "ur", "Uzbek": "uz", "Vietnamese": "vi",
                           "Wolof": "wo", "Xhosa": "xh", "Yiddish": "yi", "Yoruba": "yo", "Chinese": "zh", "Zulu": "zu"}

    languages_iso_rev = {'af': 'Afrikaans',
                         'am': 'Amharic',
                         'ar': 'Arabic',
                         'ast': 'Asturian',
                         'az': 'Azerbaijani',
                         'ba': 'Bashkir',
                         'be': 'Belarusian',
                         'bg': 'Bulgarian',
                         'bn': 'Bengali',
                         'br': 'Breton',
                         'bs': 'Bosnian',
                         'ca': 'Catalan; Valencian',
                         'ceb': 'Cebuano',
                         'cs': 'Czech',
                         'cy': 'Welsh',
                         'da': 'Danish',
                         'de': 'German',
                         'el': 'Greeek',
                         'en': 'English',
                         'es': 'Spanish',
                         'et': 'Estonian',
                         'fa': 'Persian',
                         'ff': 'Fulah',
                         'fi': 'Finnish',
                         'fr': 'French',
                         'fy': 'Western Frisian',
                         'ga': 'Irish',
                         'gd': 'Gaelic; Scottish Gaelic',
                         'gl': 'Galician',
                         'gu': 'Gujarati',
                         'ha': 'Hausa',
                         'he': 'Hebrew',
                         'hi': 'Hindi',
                         'hr': 'Croatian',
                         'ht': 'Haitian; Haitian Creole',
                         'hu': 'Hungarian',
                         'hy': 'Armenian',
                         'id': 'Indonesian',
                         'ig': 'Igbo',
                         'ilo': 'Iloko',
                         'is': 'Icelandic',
                         'it': 'Italian',
                         'ja': 'Japanese',
                         'jv': 'Javanese',
                         'ka': 'Georgian',
                         'kk': 'Kazakh',
                         'km': 'Central Khmer',
                         'kn': 'Kannada',
                         'ko': 'Korean',
                         'lb': 'Luxembourgish; Letzeburgesch',
                         'lg': 'Ganda',
                         'ln': 'Lingala',
                         'lo': 'Lao',
                         'lt': 'Lithuanian',
                         'lv': 'Latvian',
                         'mg': 'Malagasy',
                         'mk': 'Macedonian',
                         'ml': 'Malayalam',
                         'mn': 'Mongolian',
                         'mr': 'Marathi',
                         'ms': 'Malay',
                         'my': 'Burmese',
                         'ne': 'Nepali',
                         'nl': 'Dutch; Flemish',
                         'no': 'Norwegian',
                         'ns': 'Northern Sotho',
                         'post 1500': 'Occitan',
                         'or': 'Oriya',
                         'pa': 'Panjabi; Punjabi',
                         'pl': 'Polish',
                         'ps': 'Pushto; Pashto',
                         'pt': 'Portuguese',
                         'ro': 'Romanian; Moldavian; Moldovan',
                         'ru': 'Russian',
                         'sd': 'Sindhi',
                         'si': 'Sinhala; Sinhalese',
                         'sk': 'Slovak',
                         'sl': 'Slovenian',
                         'so': 'Somali',
                         'sq': 'Albanian',
                         'sr': 'Serbian',
                         'ss': 'Swati',
                         'su': 'Sundanese',
                         'sv': 'Swedish',
                         'sw': 'Swahili',
                         'ta': 'Tamil',
                         'th': 'Thai',
                         'tl': 'Tagalog',
                         'tn': 'Tswana',
                         'tr': 'Turkish',
                         'uk': 'Ukrainian',
                         'ur': 'Urdu',
                         'uz': 'Uzbek',
                         'vi': 'Vietnamese',
                         'wo': 'Wolof',
                         'xh': 'Xhosa',
                         'yi': 'Yiddish',
                         'yo': 'Yoruba',
                         'zh': 'Chinese',
                         'zu': 'Zulu'}

    iso_set: set = set(
        ['th', 'kn', 'ml', 'lo', 'uz', 'ar', 'he', 'ca', 'gl', 'lv', 'it', 'ka', 'tr', 'ht', 'ff', 'ru', 'sd', 'sk',
         'lb', 'tl', 'af', 'ps', 'mn', 'fa', 'hr', 'bn', 'es', 'km', 'fi', 'kk', 'is', 'fr', 'en', 'ms', 'gd', 'mg',
         'su', 'de', 'am', 'my', 'et', 'ln', 'ceb', 'lt', 'pa', 'hy', 'mr', 'vi', 'ss', 'az', 'ga', 'da', 'hu', 'sw',
         'gu', 'nl', 'sl', 'ig', 'or', 'lg', 'sr', 'ur', 'el', 'uk', 'ilo', 'ja', 'ba', 'ko', 'wo', 'xh', 'so', 'ns',
         'ast', 'bs', 'yi', 'pl', 'sv', 'yo', 'br', 'ta', 'si', 'hi', 'bg', 'ha', 'mk', 'fy', 'cs', 'zh', 'ne', 'tn',
         'jv', 'sq', 'id', 'post 1500', 'no', 'pt', 'be', 'cy', 'zu', 'ro'])

    def language_iso_check(self, v):
        if v not in LanguageValidator.iso_set:
            raise ValueError('Must be ISO-639-1 standard language: en, de, no, fi')
        return v
