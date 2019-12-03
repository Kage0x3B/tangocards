import random
from threading import Timer

from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, \
    QSizePolicy
from fbs_runtime.application_context.PyQt5 import ApplicationContext

import util
from card_list import CardList, Card
from flashcard_manager import FlashcardManager


class LearnWindow(QMainWindow):
    def __init__(self, app_context: ApplicationContext, flashcard_manager: FlashcardManager, card_list: CardList,
                 parent=None):
        super(LearnWindow, self).__init__(parent)

        self.app_context = app_context
        self.flashcard_manager = flashcard_manager
        self.card_list = card_list

        self.setFixedSize(400, 200)
        self.setWindowTitle("Abfrage: " + self.card_list.name + " - TangoCards")

        main_widget = QWidget()
        main_widget.setProperty("cssClass", "background")
        main_layout = QVBoxLayout()

        upper_container = QWidget()
        upper_layout = QHBoxLayout()
        upper_container.setLayout(upper_layout)
        left_container = QWidget()
        left_layout = QVBoxLayout()
        left_container.setLayout(left_layout)
        right_container = QWidget()
        right_layout = QVBoxLayout()
        right_container.setLayout(right_layout)

        self.word_text = QLabel()
        left_layout.addWidget(QLabel("Wort:"))
        left_layout.addWidget(self.word_text)
        left_layout.addItem(QSpacerItem(150, 10, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding))

        self.solution_text_box = QLineEdit()
        right_layout.addWidget(QLabel("Lösung:"))
        right_layout.addWidget(self.solution_text_box)
        right_layout.addItem(QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding))

        upper_layout.addWidget(left_container)
        upper_layout.addWidget(right_container)

        main_layout.addWidget(upper_container)

        self.enter_button = QPushButton("Überprüfen")
        self.enter_button.clicked.connect(self.check_word)
        main_layout.addWidget(self.enter_button)
        self.result_label = QLabel()
        main_layout.addWidget(self.result_label)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.current_card: Card = None

        self.next_word()

    def next_word(self):
        self.current_card = random.choice(self.card_list.cards)
        self.word_text.setText(self.current_card.word)
        self.solution_text_box.setText("")
        self.result_label.setText("")

        self.enter_button.setEnabled(True)
        self.solution_text_box.setEnabled(True)

    def check_word(self):
        solution = self.current_card.solution
        solution_attempt = self.solution_text_box.text()

        if util.slugify(solution) == util.slugify(solution_attempt):
            self.result_label.setText("Richtig!")
        else:
            self.result_label.setText("Leider falsch, Lösung: " + solution)

        self.enter_button.setEnabled(False)
        self.solution_text_box.setEnabled(False)

        Timer(3.0, self.next_word).start()
