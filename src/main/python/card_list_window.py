from PyQt5.QtCore import QStringListModel
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QListView, QWidget, QAbstractItemView, QComboBox
from fbs_runtime.application_context.PyQt5 import ApplicationContext

from flashcard_manager import FlashcardManager
from language import Language


class CardListWindow(QMainWindow):
    def __init__(self, app_context: ApplicationContext, flashcard_manager: FlashcardManager, *args, **kwargs):
        super(CardListWindow, self).__init__(*args, **kwargs)

        self.flashcard_manager = flashcard_manager

        self.resize(400, 600)
        self.setWindowTitle("Meine Lernkarteien - TangoCards")

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        language_select = QComboBox()

        for i in range(len(Language)):
            language = Language(i)
            language_select.insertItem(i, language.get_display_name(), language.value)
            language_select.setItemIcon(i, QIcon(app_context.get_resource("icons/flag_" + language.name + ".png")))

        main_layout.addWidget(language_select)

        card_list_model = QStringListModel(self.flashcard_manager.get_flashcard_lists(Language.english))
        card_list = QListView()
        card_list.setModel(card_list_model)
        card_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        main_layout.addWidget(card_list)

        add_button = QPushButton("Lernkartei hinzufügen")
        main_layout.addWidget(add_button)

        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)
