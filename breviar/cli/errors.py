from colorama import Fore, Style

from breviar.core.errors import breviarError


class NotConfigured(breviarError):
    def __init__(self, service: str, code: str = None, message: str = None, *args):
        super().__init__(code, message, *args)
        self.message = f'Please configure {Fore.GREEN + service + Style.RESET_ALL} service. Run:\n' \
                       f'breviar configure'


class ConfigNotValid(breviarError):
    def __init__(self, service: str, code: str = None, message: str = None, *args):
        super().__init__(code, message, *args)
        self.message = f'Config of {Fore.GREEN + service + Style.RESET_ALL} service is not valid. To rewrite it run:\n' \
                       f'breviar configure'
