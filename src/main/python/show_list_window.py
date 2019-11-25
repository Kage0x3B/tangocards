from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QListView, QWidget, QAbstractItemView, QHBoxLayout, \
    QMessageBox, QInputDialog
from fbs_runtime.application_context.PyQt5 import ApplicationContext

from card_list import CardList
from flashcard_manager import FlashcardManager


class ShowListWindow(QMainWindow):
    def __init__(self, app_context: ApplicationContext, flashcard_manager: FlashcardManager, card_list: CardList, parent=None):
        super(ShowListWindow, self).__init__(parent)

        self.flashcard_manager = flashcard_manager
        self.card_list = card_list

        self.setFixedSize(600, 400)
        self.setWindowTitle(self.card_list.name + " - TangoCards")

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Initialized up here because the combobox already fires the currentIndexChanged signal on creation
        self.card_list_model = QStringListModel(self.card_list.get_card_name_list())
        self.card_list = QListView()
        self.card_list.setModel(self.card_list_model)
        self.card_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.card_list.doubleClicked.connect(self.on_list_doubleclick)

        main_layout.addWidget(self.card_list)

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

    def on_click_add(self):
        text, ok = QInputDialog.getText(self, 'Lernkartei erstellen', 'Namen für die Lernkartei:')

        if ok:
            if text is None or len(text) < 2:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Der Name ist leer oder zu kurz!")
                msg.exec_()

                return

            self.flashcard_manager.create_list(self.current_language, text)

            self.on_select_language(self.current_language.value)  # Update gui

    def on_click_learn(self):
        if len(self.card_list.selectedIndexes()) < 1:
            return

        card_list = self.flashcard_manager.get_flashcard_list_by_name(self.current_language,
                                                                      self.card_list.selectedIndexes()[0].data())
        print("learn ", card_list.name)

    def on_click_delete(self):
        if len(self.card_list.selectedIndexes()) < 1:
            return

        list_name = self.card_list.selectedIndexes()[0].data()

        choice = QMessageBox.question(self, 'Löschen',
                                      "Willst du wirklich die Liste \"" + list_name + "\" löschen?",
                                      QMessageBox.Yes | QMessageBox.No)

        if choice == QMessageBox.Yes:
            self.flashcard_manager.delete_list(self.current_language, list_name)

            self.on_select_language(self.current_language.value)  # Update gui
