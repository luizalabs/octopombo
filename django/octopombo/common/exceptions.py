class HttpError(Exception):

    code = 500
    message = 'Internal server error'

    def __init__(self, code=None, message=None):
        if code:
            self.code = code
        if message:
            self.message = message

    def __str__(self):
        return '{name}({code})'.format(
            name=self.__class__.__name__,
            code=self.code
        )
