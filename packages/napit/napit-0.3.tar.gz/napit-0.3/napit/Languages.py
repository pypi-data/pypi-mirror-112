from enum import Enum


class Language(Enum):
    KOREAN = "ko"
    ENGLISH = "en"
    CHINESE = "zh-CN"
    CHINESE_TAIWAN = "zh-TW"
    SPANISH = "es"
    FRENCH = "fr"
    VIETNAMESE = "vi"
    THAI = "th"
    INDONESIAN = "id"


class InvalidLanguageException(Exception):
    def __str__(self):
        return "Invalid Language"
