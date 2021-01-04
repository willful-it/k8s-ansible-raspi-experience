from colorama import Back, Fore, Style


def print_title(text: str, extra: str = ""):
    print(Back.YELLOW + Fore.BLACK + text + Style.RESET_ALL, extra)
