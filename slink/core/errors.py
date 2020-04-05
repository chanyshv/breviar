from colorama import Fore, Style


class SLinkError(RuntimeError):
    _default_message = 'Unknown_error'
    _default_code = 'error'

    def __init__(self, code: str = None, message: str = None, *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.code = code or self._default_code
        self.message = message or self._default_message

    def __str__(self):
        return f'[{Fore.RED + self.code + Style.RESET_ALL}] {self.message}'


class WrongResponse(SLinkError):
    _default_message = 'Server sent wrong response'


class NoResponse(SLinkError):
    _default_message = 'Server does not respond'
