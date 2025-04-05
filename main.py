# -*- coding: utf-8 -*-
import sys, subprocess, os
from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon
from pypresence import Presence
from datetime import datetime
CONFIG_FILE = "config.txt"
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sigma Rich Presence")
        self.setGeometry(100, 100, 500, 400)
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.rpc = None
        self.create_rich_presence_tab()
        self.create_settings_tab()
        self.create_about_tab()
        self.load_config()
    # --- Tab 1: Rich Presence ---
    def create_rich_presence_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        self.details_input = QLineEdit()
        self.details_input.setPlaceholderText("Details")
        self.state_input = QLineEdit()
        self.state_input.setPlaceholderText("State")
        self.start_button = QPushButton("Start Rich Presence")
        self.start_button.clicked.connect(self.start_rpc)
        layout.addWidget(QLabel("Details:"))
        layout.addWidget(self.details_input)
        layout.addWidget(QLabel("State:"))
        layout.addWidget(self.state_input)
        layout.addWidget(self.start_button)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Rich Presence")
    # --- Tab 2: Settings ---
    def create_settings_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        self.client_id_input = QLineEdit()
        self.client_id_input.setPlaceholderText("Client ID")
        self.theme_selector = QComboBox()
        self.theme_selector.addItems(["Light", "Dark"])
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save_config)
        layout.addWidget(QLabel("Client ID:"))
        layout.addWidget(self.client_id_input)
        layout.addWidget(QLabel("Theme:"))
        layout.addWidget(self.theme_selector)
        layout.addWidget(save_btn)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Settings")
    # --- Tab 3: About ---
    def create_about_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Made by Sigma Boy 😎"))
        github_btn = QPushButton("Open GitHub")
        github_btn.clicked.connect(lambda: os.system("start https://github.com/bowser-2077/SigmaPresence"))
        update_btn = QPushButton("Update")
        update_btn.clicked.connect(self.run_updater)
        layout.addWidget(github_btn)
        layout.addWidget(update_btn)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "About")
    def start_rpc(self):
        client_id = self.client_id_input.text()
        if not client_id:
            QMessageBox.warning(self, "Erreur", "Client ID manquant.")
            return
        try:
            self.rpc = Presence(client_id)
            self.rpc.connect()
            self.rpc.update(
                details=self.details_input.text(),
                state=self.state_input.text(),
                start=int(datetime.now().timestamp())
            )
            QMessageBox.information(self, "OK", "Rich Presence lancee.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))
    def save_config(self):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                f.write(self.client_id_input.text() + "\n")
                f.write(self.theme_selector.currentText() + "\n")
            QMessageBox.information(self, "OK", "Configuration sauvegardee.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))
    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
                if len(lines) >= 1:
                    self.client_id_input.setText(lines[0])
                if len(lines) >= 2:
                    index = self.theme_selector.findText(lines[1])
                    if index != -1:
                        self.theme_selector.setCurrentIndex(index)
    def run_updater(self):
        self.close()
        subprocess.Popen(["python", "updater.py"], shell=True)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
