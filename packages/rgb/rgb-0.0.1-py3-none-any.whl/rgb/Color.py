import re


class Color:
    def __init__(self, *args):
        rgb, r, g, b = self._validate_input(args)

        if rgb is not None:
            rgb = self._clean_rgb(rgb)
            r = int(rgb[0:2], base=16)
            g = int(rgb[2:4], base=16)
            b = int(rgb[4:6], base=16)
        else:
            rgb = f"{r:02x}{g:02x}{b:02x}"
        self.rgb = rgb
        self.r, self.g, self.b = r, g, b


    def __repr__(self):
        text = f" #{self.rgb} "

        display = f"Color #{self.rgb}: "
        # Default background, Color foreground
        display += f"\033[38;2;{self.r};{self.g};{self.b}m{text}\033[0m"
        # Color background, default foreground
        display += f"\033[48;2;{self.r};{self.g};{self.b}m{text}\033[0m"
        # Just Color
        display += f"\033[48;2;{self.r};{self.g};{self.b};38;2;{self.r};{self.g};{self.b}m{text}\033[0m"

        return display


    def _validate_input(self, args):
        rgb, r, g, b = None, None, None, None

        if len(args) not in [1, 3]:
            raise ValueError("Please specify color one way: (rgb=000000) or (r=0, g=0, b=0).")

        if len(args) == 1:
            rgb = args[0]
            if type(rgb) is not str:
                raise ValueError("Please specify color one way: (rgb=000000) or (r=0, g=0, b=0).")
            if not re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", rgb):
                raise ValueError(f"{rgb} is not a valid hex code.")

        else:
            r, g, b = args
            if not(0 <= r <= 255) or not(0 <= g <= 255) or not (0 <= b <= 255):
                raise ValueError(f"(r={r}, g={g}, b={b}) is not a valid color code.")
        
        return rgb, r, g, b


    def _clean_rgb(self, rgb):
        if rgb[0] == "#":
            rgb = rgb[1:]
        if len(rgb) == 3:
            rgb = f"{rgb[0]}{rgb[0]}{rgb[1]}{rgb[1]}{rgb[2]}{rgb[2]}"
        
        return rgb
