from colorthief import ColorThief


class ColorPicker(ColorThief):
    def __init__(self, file):
        super().__init__(file)
        self.color_thief = ColorThief(file)
        self.dominant_color = self.color_thief.get_color(quality=1)
        self.palette = self.color_thief.get_palette(color_count=11)
