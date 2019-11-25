from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QListView, QWidget, QAbstractItemView, QHBoxLayout, \
    QMessageBox, QInputDialog
from fbs_runtime.application_context.PyQt5 import ApplicationContext

from card_list import CardList
from flashcard_manager import FlashcardManager


class ShowListWindow(QMainWindow):
    def __init__(self, app_context: ApplicationContext, flashcard_manager: FlashcardManager, card_list: CardList,
                 parent=None):
        super(ShowListWindow, self).__init__(parent)

        self.flashcard_manager = flashcard_manager
        self.card_list = card_list

        self.setFixedSize(600, 400)
        self.setWindowTitle(self.card_list.name + " - TangoCards")

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        learn_button = QPushButton("Frag mich ab!")
        learn_button.clicked.connect(self.on_click_learn)
        main_layout.addWidget(learn_button)

        self.card_list_model = QStringListModel(self.card_list.get_card_name_list())
        self.cards_list_component = QListView()
        self.cards_list_component.setModel(self.card_list_model)
        self.cards_list_component.setEditTriggers(QAbstractItemView.NoEditTriggers)

        main_layout.addWidget(self.cards_list_component)

        tool_buttons_widget = QWidget()
        tool_buttons_layout = QHBoxLayout()
        tool_buttons_widget.setLayout(tool_buttons_layout)

        add_button = QPushButton("Hinzufügen")
        add_button.clicked.connect(self.on_click_add)
        delete_button = QPushButton("Löschen")
        delete_button.clicked.connect(self.on_click_delete)
        tool_buttons_layout.addWidget(add_button)
        tool_buttons_layout.addWidget(delete_button)

        main_layout.addWidget(tool_buttons_widget)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def update_list(self):
        self.card_list_model = QStringListModel(self.card_list.get_card_name_list())
        self.cards_list_component.setModel(self.card_list_model)
        self.cards_list_component.repaint()

    def on_click_add(self):
        word_text, ok1 = QInputDialog.getText(self, 'Karte hinzufügen', 'Wort:')

        if not ok1:
            return

        if word_text is None or len(word_text) < 2:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Der Text ist leer oder zu kurz!")
            msg.exec_()

            return

        if self.card_list.get_card(word_text) is not None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Wort ist bereits in der Lernkartei!")
            msg.exec_()

            return

        solution_text, ok2 = QInputDialog.getText(self, 'Karte hinzufügen', 'Lösung:')

        if not ok2:
            return

        if solution_text is None or len(word_text) < 2:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Der Text ist leer oder zu kurz!")
            msg.exec_()

            return

        self.card_list.add_card(word_text, solution_text)
        self.flashcard_manager.save_list(self.card_list)
        self.update_list()

    def on_click_learn(self):
        pass

    def on_click_delete(self):
        if len(self.cards_list_component.selectedIndexes()) < 1:
            return

        word_text = self.cards_list_component.selectedIndexes()[0].data()
        card = self.card_list.get_card(word_text)

        if card is not None:
            self.card_list.remove_card(card)
            self.flashcard_manager.save_list(self.card_list)
            self.update_list()
