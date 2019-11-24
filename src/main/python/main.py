import sys

from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication, QStyleFactory
from fbs_runtime.application_context.PyQt5 import ApplicationContext

from card_list_window import CardListWindow
from flashcard_manager import FlashcardManager


def create_palette():
    palette = QPalette()
    # palette.setColor(QPalette.Window, QColor(153, 153, 153))

    return palette


if __name__ == '__main__':
    app_context = ApplicationContext()
    app: QApplication = app_context.app

    app.setApplicationName("TangoCards")
    app.setOrganizationName("Syscy")
    app.setOrganizationDomain("syscy.de")
    app.setStyle("Fusion")
    app.setPalette(create_palette())

    flashcard_manager = FlashcardManager()

    window = CardListWindow(app_context, flashcard_manager)
    window.show()

    exit_code = app.exec_()
    sys.exit(exit_code)
