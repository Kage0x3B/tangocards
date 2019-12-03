from PyQt5.QtCore import QStringListModel, QModelIndex
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QListView, QWidget, QAbstractItemView, QComboBox, \
    QHBoxLayout, QMessageBox, QInputDialog
from fbs_runtime.application_context.PyQt5 import ApplicationContext

from flashcard_manager import FlashcardManager
from language import Language
from show_list_window import ShowListWindow


class CardListWindow(QMainWindow):
    def __init__(self, app_context: ApplicationContext, flashcard_manager: FlashcardManager, *args, **kwargs):
        super(CardListWindow, self).__init__(*args, **kwargs)

        self.app_context = app_context
        self.flashcard_manager = flashcard_manager
        self.current_language = Language(0)

        self.setFixedSize(400, 600)
        self.setWindowTitle("Meine Lernkarteien - TangoCards")

        main_widget = QWidget()
        main_widget.setProperty("cssClass", "background")
        main_layout = QVBoxLayout()

        # Initialized up here because the combobox already fires the currentIndexChanged signal on creation
        self.card_list_model = QStringListModel(self.flashcard_manager.get_flashcard_list_names(self.current_language))
        self.card_list = QListView()
        self.card_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.card_list.doubleClicked.connect(self.on_list_doubleclick)

        language_select = QComboBox()
        language_select.currentIndexChanged.connect(self.on_select_language)

        for language in Language:
            # if len(self.flashcard_manager.get_flashcard_lists(language)) < 1:
            #    continue

            language_select.insertItem(language.value, language.get_display_name(), language.value)
            language_select.setItemIcon(language.value,
                                        QIcon(app_context.get_resource("icons/flag_" + language.name + ".png")))

        main_layout.addWidget(language_select)
        main_layout.addWidget(self.card_list)

        tool_buttons_widget = QWidget()
        tool_buttons_layout = QHBoxLayout()
        tool_buttons_widget.setLayout(tool_buttons_layout)

        learn_button = QPushButton("Lernen")
        learn_button.clicked.connect(self.on_click_learn)
        add_button = QPushButton("Hinzufügen")
        add_button.clicked.connect(self.on_click_add)
        delete_button = QPushButton("Löschen")
        delete_button.clicked.connect(self.on_click_delete)
        tool_buttons_layout.addWidget(learn_button)
        tool_buttons_layout.addWidget(add_button)
        tool_buttons_layout.addWidget(delete_button)

        main_layout.addWidget(tool_buttons_widget)

        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)

    def on_select_language(self, language_id):
        self.current_language = Language(language_id)

        self.card_list_model = QStringListModel(self.flashcard_manager.get_flashcard_list_names(self.current_language))
        self.card_list.setModel(self.card_list_model)
        self.card_list.repaint()

    def on_click_learn(self):
        if len(self.card_list.selectedIndexes()) < 1:
            return

        card_list = self.flashcard_manager.get_flashcard_list_by_name(self.current_language,
                                                                      self.card_list.selectedIndexes()[0].data())

        window = ShowListWindow(self.app_context, self.flashcard_manager, card_list, parent=self)
        window.show()

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

    def on_list_doubleclick(self, model_index: QModelIndex):
        card_list = self.flashcard_manager.get_flashcard_list_by_name(self.current_language, model_index.data())

        window = ShowListWindow(self.app_context, self.flashcard_manager, card_list, parent=self)
        window.show()
