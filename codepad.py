import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QMenu, QAction, QMessageBox, QTextBrowser, QVBoxLayout, QWidget, QPushButton
from base64 import b64encode
from codecs import encode
import chardet
from PyQt5.QtWidgets import QMessageBox, QPushButton






def apply_dark_theme():
    dark_stylesheet = """
    QMainWindow {
        background-color: #31363b;
        color: #eff0f1;
    }
    QTextEdit {
        background-color: #24282a;
        color: #eff0f1;
    }
    """
    app.setStyleSheet(dark_stylesheet)

def identify_encoding():
    selected_text = text_edit.textCursor().selectedText()
    encoding_info = chardet.detect(selected_text.encode())
    encoding = encoding_info['encoding']
    message = f"Detected Encoding: {encoding}"
    show_message("Encoding Identification", message)

def convert_base64():
    selected_text = text_edit.textCursor().selectedText()
    base64_text = b64encode(selected_text.encode()).decode()
    replace_selected_text(base64_text)

def convert_rot13():
    selected_text = text_edit.textCursor().selectedText()
    rot13_text = encode(selected_text, 'rot_13')
    replace_selected_text(rot13_text)

def convert_hex():
    selected_text = text_edit.textCursor().selectedText()
    hex_text = selected_text.encode().hex()
    replace_selected_text(hex_text)

# Other functions remain unchanged

def replace_selected_text(new_text):
    cursor = text_edit.textCursor()
    cursor.insertText(new_text)
    text_edit.setTextCursor(cursor)




def show_message(title, message):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setFixedSize(58*10, 12*20)  # Setting fixed size to 28x5 characters
    ok_button = QPushButton("OK")
    msg.addButton(ok_button, QMessageBox.AcceptRole)
    msg.exec_()


def run_url():
    selected_text = text_edit.textCursor().selectedText()
    if selected_text.startswith("http://") or selected_text.startswith("https://"):
        try:
            response = requests.get(selected_text)
            status_message = f"Status: {response.status_code} - {response.reason}"
            show_message("URL Status", status_message)
        except requests.RequestException as e:
            show_message("Error", f"An error occurred: {str(e)}")
    else:
        show_message("Invalid URL", "Please select a valid URL starting with 'http://' or 'https://'.")


def convert_to_lowercase():
    selected_text = text_edit.textCursor().selectedText()
    converted_text = ''
    for char in selected_text:
        if char.isalpha():
            converted_text += char.lower()
        else:
            converted_text += char
    replace_selected_text(converted_text)

def convert_to_uppercase():
    selected_text = text_edit.textCursor().selectedText()
    converted_text = ''
    for char in selected_text:
        if char.isalpha():
            converted_text += char.upper()
        else:
            converted_text += char
    replace_selected_text(converted_text)



app = QApplication(sys.argv)
apply_dark_theme()  # Applying dark theme immediately
window = QMainWindow()
window.resize(98*10, 23*20)  # Setting initial size to 115x25 characters
text_edit = QTextEdit()
window.setCentralWidget(text_edit)

context_menu = QMenu()

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

# New "Extras" submenu
extras_menu = QMenu("Extras", window)
context_menu.addMenu(extras_menu)

lowercase_action = QAction("Convert to Lowercase", window)
lowercase_action.triggered.connect(convert_to_lowercase)
extras_menu.addAction(lowercase_action)

uppercase_action = QAction("Convert to Uppercase", window)
uppercase_action.triggered.connect(convert_to_uppercase)
extras_menu.addAction(uppercase_action)


# Other context menu actions remain unchanged

text_edit.setContextMenuPolicy(3)  # This sets the context menu policy to CustomContextMenu
text_edit.customContextMenuRequested.connect(lambda x: context_menu.popup(text_edit.mapToGlobal(x)))

window.show()
sys.exit(app.exec_())
