from colorama import Fore, Style

from slink.core.errors import SLinkError


class NotConfigured(SLinkError):
    def __init__(self, service: str, code: str = None, message: str = None, *args):
        super().__init__(code, message, *args)
        self.message = f'Please configure {Fore.GREEN + service + Style.RESET_ALL} service. Run:\n' \
                       f'slink configure -S {service}'


class ConfigNotValid(SLinkError):
    def __init__(self, service: str, code: str = None, message: str = None, *args):
        super().__init__(code, message, *args)
        self.message = f'Config of {Fore.GREEN + service + Style.RESET_ALL} service is not valid. To rewrite it run:\n' \
                       f'slink configure -S {service}'


