import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QMenu, QAction, QMessageBox, QStackedWidget, QPushButton, QTextBrowser, QVBoxLayout, QWidget
import base64
import codecs
from pydracula import DraculaStyle

def apply_dracula_theme():
    app.setStyleSheet(DraculaStyle().get_stylesheet())

def identify_encoding():
    selected_text = text_edit.textCursor().selectedText()
    encoding_info = chardet.detect(selected_text.encode())
    encoding = encoding_info['encoding']
    message = f"Detected Encoding: {encoding}"
    show_message("Encoding Identification", message)

def convert_base64():
    selected_text = text_edit.textCursor().selectedText()
    base64_text = base64.b64encode(selected_text.encode()).decode()
    replace_selected_text(base64_text)

def convert_rot13():
    selected_text = text_edit.textCursor().selectedText()
    rot13_text = codecs.encode(selected_text, 'rot_13')
    replace_selected_text(rot13_text)

def convert_hex():
    selected_text = text_edit.textCursor().selectedText()
    hex_text = selected_text.encode().hex()
    replace_selected_text(hex_text)

def show_message(title, message):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.exec_()

def replace_selected_text(new_text):
    cursor = text_edit.textCursor()
    cursor.insertText(new_text)
    text_edit.setTextCursor(cursor)

def run_url():
    selected_text = text_edit.textCursor().selectedText()
    if selected_text.startswith("http://") or selected_text.startswith("https://"):
        response = requests.get(selected_text)
        create_new_response_window(response.text)

def create_new_response_window(response_text):
    response_window = QMainWindow()
    response_widget = QWidget()
    response_layout = QVBoxLayout()

    response_browser = QTextBrowser()
    response_browser.setPlainText(response_text)
    response_layout.addWidget(response_browser)

    close_button = QPushButton("Close")
    close_button.clicked.connect(response_window.close)
    response_layout.addWidget(close_button)

    response_widget.setLayout(response_layout)
    response_window.setCentralWidget(response_widget)
    response_window.setWindowTitle("URL Response")
    response_window.show()

app = QApplication(sys.argv)
window = QMainWindow()
text_edit = QTextEdit()
window.setCentralWidget(text_edit)

context_menu = QMenu()

apply_dracula_action = QAction("Apply Dracula Theme", window)
apply_dracula_action.triggered.connect(apply_dracula_theme)
context_menu.addAction(apply_dracula_action)

identify_action = QAction("Identify Encoding", window)
identify_action.triggered.connect(identify_encoding)
context_menu.addAction(identify_action)

base64_action = QAction("Convert to Base64", window)
base64_action.triggered.connect(convert_base64)
context_menu.addAction(base64_action)

rot13_action = QAction("Convert to ROT13", window)
rot13_action.triggered.connect(convert_rot13)
context_menu.addAction(rot13_action)

hex_action = QAction("Convert to Hex", window)
hex_action.triggered.connect(convert_hex)
context_menu.addAction(hex_action)

run_url_action = QAction("Run URL", window)
run_url_action.triggered.connect(run_url)
context_menu.addAction(run_url_action)

text_edit.setContextMenuPolicy(3)  # This sets the context menu policy to CustomContextMenu
text_edit.customContextMenuRequested.connect(lambda x: context_menu.popup(text_edit.mapToGlobal(x)))

window.show()
sys.exit(app.exec_())
