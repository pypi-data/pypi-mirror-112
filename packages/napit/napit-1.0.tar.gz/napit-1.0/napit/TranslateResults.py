class TranslateResults:
    def __init__(self, text, error):
        if error is not None:
            raise TranslateError(error)
        else:
            self.text = text


class TranslateError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
