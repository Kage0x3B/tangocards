from enum import IntEnum, Enum

DISPLAY_NAMES = [
    "Englisch",
    "Französisch",
    "Japanisch",
    "Mandarin Chinesisch (vereinfacht)"
]


class Language(Enum):
    english = 0
    #german = 1
    french = 1
    japanese = 2
    chinese = 3

    def get_display_name(self):
        return DISPLAY_NAMES[self.value]
