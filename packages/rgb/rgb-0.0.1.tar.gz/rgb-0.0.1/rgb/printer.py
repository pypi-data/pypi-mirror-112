from .Color import Color


def rgbprint(text, color=None):
    if color is None:
        print(text)
        return

    if type(color) == str:
        color = Color(color)
    elif not isinstance(color, Color):
        raise ValueError("colorize() requires color specified with a hex code or a Color() instance.")
    
    print(colorize(text, color))


def colorize(text, color):
    if type(color) == str:
        color = Color(rgb=color)
    elif not isinstance(color, Color):
        raise ValueError("colorize() requires color specified with a hex code or a Color() instance.")

    return f"\033[38;2;{color.r};{color.g};{color.b}m{text}\033[0m"
