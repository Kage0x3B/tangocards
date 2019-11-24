from enum import IntEnum, Enum

DISPLAY_NAMES = [
    "Englisch",
    "Deutsch",
    "Französisch",
    "Japanisch",
    "Chinesisch"
]


class Language(Enum):
    english = 0
    german = 1
    french = 2
    japanese = 3
    chinese = 4

    def get_display_name(self):
        return DISPLAY_NAMES[self.value]
