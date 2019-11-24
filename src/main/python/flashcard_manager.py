import os

from language import Language


class FlashcardManager:
    def __init__(self):
        self.data_dir = self.create_dir("data")
        self.card_list_dir = self.create_dir("data/cardlists")

    def create_dir(self, rel_path):
        dir_path = os.path.join(os.getcwd(), rel_path)

        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        return dir_path

    def get_flashcard_lists(self, language: Language):
        return ["Tiere", "Familie", "Zahlen von 1-10"]
