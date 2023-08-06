from colorama import init, Fore

init()


def colorize(string, color: str) -> str:
    """
    Returns a string colored with the selected color.\n
    Available colors: black, red, green, yellow, blue, magenta, cyan, white, reset
    """
    return str(getattr(Fore, color.upper()) + str(string) + Fore.RESET)
