import os
import sys
from core import core
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QLabel, QFileDialog, QTextEdit
)


# импортируй свои функции из проекта
# from gost_34102012 import sign_file, verify_file


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GOST 34.10-2012 EDS Tool")
        self.setMinimumWidth(500)

        layout = QVBoxLayout()

        self.label = QLabel("Выберите файл")
        layout.addWidget(self.label)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        self.btn_file = QPushButton("📄 Выбрать файл")
        self.btn_file.clicked.connect(self.choose_file)
        layout.addWidget(self.btn_file)

        self.btn_key = QPushButton("📄 Сгенерировать ключи")
        self.btn_key.clicked.connect(self.generate_key)
        layout.addWidget(self.btn_key)

        self.btn_sign = QPushButton("✍️ Подписать файл")
        self.btn_sign.clicked.connect(self.sign_file)
        layout.addWidget(self.btn_sign)

        self.btn_verify = QPushButton("✔️ Проверить подпись")
        self.btn_verify.clicked.connect(self.verify_file)
        layout.addWidget(self.btn_verify)

        self.file_path = None

        self.setLayout(layout)

    def choose_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Выбор файла")
        if file:
            self.file_path = file
            self.label.setText(f"Файл: {file}")
            self.log.append(f"[+] Выбран файл: {file}")

    def generate_key(self):
        private_key, public_key = core.generate_keypair()
        core.save_private_key('private.key', private_key)
        core.save_public_key('public.key', public_key)
        self.log.append("[+] Ключевая пара успешно сгенерирована.")
        self.log.append("[+] Закрытый ключ сохранён в файл: private.key")
        self.log.append("[+] Открытый ключ сохранён в файл: public.key")

    def sign_file(self):
        if not self.file_path:
            self.log.append("[-] Файл не выбран")
            return

        data = core.read_file(self.file_path)
        private_key = core.load_private_key('private.key')
        sig_file = os.path.splitext(self.file_path)[0] + '.sig'

        signature = core.sign(data, private_key)
        core.save_signature(sig_file, signature)

        self.log.append(f"[+] Файл подписан: {self.file_path}. Подпись сохранена в файл: {sig_file}")

    def verify_file(self):
        if not self.file_path:
            self.log.append("[-] Файл не выбран")
            return

        data = core.read_file(self.file_path)
        public_key = core.load_public_key('public.key')
        signature = core.load_signature(os.path.splitext(self.file_path)[0] + '.sig')

        result = core.verify(data, public_key, signature)

        if result:
            self.log.append(f"[+] Проверка выполнена: {self.file_path}. Подпись корректна.")
        else:
            self.log.append(f"[-] Проверка выполнена: {self.file_path}. Подпись некорректна.")


def gui():
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
