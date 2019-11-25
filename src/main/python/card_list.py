import uuid

from language import Language

DEFAULT_DATA = {
    "cards": [],
    "id": uuid.uuid4().hex,
    "name": "Invalid list",
    "icon": "default.png"
}


class CardList:
    def __init__(self, filename: str, language: Language, json_data=None, name=None):
        self.filename = filename
        self.language = language

        if json_data is None:
            json_data = DEFAULT_DATA.copy()
            json_data["id"] = uuid.uuid4().hex

        if name is None:
            name = json_data["name"]

        self.cards = []
        self.id = json_data["id"]
        self.name = name
        self.icon = json_data["icon"]

        for card_data in json_data["cards"]:
            self.cards.append(Card(card_data["word"], card_data["solution"]))

    def add_card(self, word, solution):
        card = Card(word, solution)
        self.cards.append(card)

    def remove_card(self, card):
        self.cards.remove(card)

    def get_card_name_list(self):
        return map(lambda c: c.word, self.cards)

    def get_card(self, word):
        for card in self.cards:
            if card.word == word:
                return card

        return None

    def to_dict(self):
        data = {
            "cards": [],
            "id": self.id,
            "name": self.name,
            "icon": self.icon
        }

        for card in self.cards:
            data["cards"].append({
                "word": card.word,
                "solution": card.solution
            })

        return data


class Card:
    def __init__(self, word: str, solution: str):
        self.word = word
        self.solution = solution
