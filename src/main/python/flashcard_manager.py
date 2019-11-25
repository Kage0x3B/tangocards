import json
import os
import traceback

from PyQt5.QtWidgets import QMessageBox

import util
from card_list import CardList
from language import Language


class FlashcardManager:
    def __init__(self):
        self.data_dir = self.create_dir("data")
        self.card_list_dir = self.create_dir(os.path.join("data", "cardlists"))

        self.language_dirs = {}

        for language in Language:
            self.language_dirs[language.name] = self.create_dir(os.path.join("data", "cardlists", language.name))

        self.card_lists = {}

        self.load_lists()

    def load_lists(self):
        for language in Language:
            self.card_lists[language.value] = {}

            language_dir = self.language_dirs[language.name]

            for file in os.listdir(language_dir):
                if file.endswith(".json"):
                    try:
                        with open(os.path.join(language_dir, file)) as json_file:
                            card_list = CardList(file, language, json_data=json.load(json_file))
                            self.card_lists[language.value][card_list.id] = card_list
                    except:
                        print("Invalid", language.name, "card list '", file, "'")
                        traceback.print_exc()

    def save_list(self, card_list: CardList):
        with open(os.path.join(self.language_dirs[card_list.language.name], card_list.filename), 'w') as outfile:
            json.dump(card_list.to_dict(), outfile)

    def create_list(self, language: Language, name: str):
        card_list = CardList(util.slugify(name) + ".json", language, name=name)

        if self.get_flashcard_list_by_name(language, name) is not None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(
                "Die neue Liste konnte nicht erstellt werden, da eine andere mit dem gleichen Namen bereits existiert.")
            msg.setWindowTitle("Liste existiert bereits")
            msg.exec_()

            return

        self.card_lists[language.value][card_list.id] = card_list

        self.save_list(card_list)

    def get_flashcard_list_names(self, language: Language):
        lists = []

        for k, v in self.card_lists[language.value].items():
            lists.append(v.name)

        return lists

    def get_flashcard_list_by_name(self, language: Language, name: str):
        for k, card_list in self.card_lists[language.value].items():
            if card_list.name == name:
                return card_list

        return None

    def delete_list(self, language: Language, name: str):
        card_list = self.get_flashcard_list_by_name(language, name)

        if card_list is not None:
            os.remove(os.path.join(self.language_dirs[language.name], card_list.filename))
            del self.card_lists[language.value][card_list.id]

    @staticmethod
    def create_dir(relative_path: str):
        dir_path = os.path.join(os.getcwd(), relative_path)

        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        return dir_path
