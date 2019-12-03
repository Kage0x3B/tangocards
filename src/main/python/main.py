import sys

from PyQt5.QtWidgets import QApplication
from fbs_runtime.application_context.PyQt5 import ApplicationContext

from card_list_window import CardListWindow
from flashcard_manager import FlashcardManager

STYLESHEET = """
QMainWindow, QDialog {
    background-color: #444;
}

QPushButton {
    color: #333;
    background-color: rgb(255, 25, 38);
}

QLabel {
    color: #ddd;
}

QLineEdit {
    background-color: #ddd;
}

QListView {
    color: #ddd;
    background-color: #555;
    border: 1px solid rgba(255, 25, 38, 0.3);
}

QListView::item:selected:active:hover {
    background-color: rgba(255, 25, 38, 0.5);
}

QListView::item:selected:active:!hover {
    background-color: rgba(255, 25, 38, 0.2);
}

QListView::item:!selected:hover {
    background-color: rgba(255, 100, 38, 0.5);
}

QComboBox {
    color: #333;
    background-color: rgba(255, 25, 38, 0.4);
}
"""

# def create_palette():
#    palette = QPalette()
#    palette.setColor(QPalette.Window, QColor(153, 153, 153))
#
#    return palette


if __name__ == '__main__':
    app_context = ApplicationContext()
    app: QApplication = app_context.app

    app.setApplicationName("TangoCards")
    app.setOrganizationName("Syscy")
    app.setOrganizationDomain("syscy.de")
    app.setStyle("Fusion")
    app.setStyleSheet(STYLESHEET)
    # app.setPalette(create_palette())

    flashcard_manager = FlashcardManager()

    window = CardListWindow(app_context, flashcard_manager)
    window.show()

    exit_code = app.exec_()
    sys.exit(exit_code)
