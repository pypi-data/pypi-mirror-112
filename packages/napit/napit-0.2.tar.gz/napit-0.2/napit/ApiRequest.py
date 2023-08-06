from Credentials import *
import requests
from Credentials import Credentials
from TranslateResults import TranslateResults
from Languages import *


def send(credentials, source_language, target_language, text):
    if not isinstance(credentials, Credentials):
        raise InvalidCredentialException
    if not isinstance(source_language, Language) or not isinstance(target_language, Language):
        raise InvalidLanguageException
    headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Naver-Client-Id": credentials.client_id,
            "X-Naver-Client-Secret": credentials.client_secret
    }
    data = {"source": source_language.value, "target": target_language.value, "text": text}
    try:
        json = requests.post("https://openapi.naver.com/v1/papago/n2mt", data=data, headers=headers).json()
        return TranslateResults(json["message"]["result"]["translatedText"], None)
    except Exception:
        return TranslateResults(None, requests)
