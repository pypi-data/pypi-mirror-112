class Palette:
    def __init__(self, colors=None, name=None, metadata=None):
        self.colors = colors if colors is not None else []
        self.name = name if name is not None else "palette"
        self.metadata = metadata if metadata is not None else {}


    def __repr__(self):
        display = f"Palette {self.name} ({len(self.colors)} colors)\n"
        display += "\n".join([ f"- {[i]} {color.__repr__()}" for i, color in enumerate(self.colors) ])

        return display
