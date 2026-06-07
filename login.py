from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from database import conectar


class LoginWindow(QWidget):

    def __init__(self, callback):
        super().__init__()

        self.callback = callback

        self.setWindowTitle("TeacherDesk Pro")
        self.resize(400, 300)

        layout = QVBoxLayout()

        titulo = QLabel("TeacherDesk Pro")
        titulo.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
            color:white;
        """)

        titulo.setAlignment(Qt.AlignCenter)

        self.usuario = QLineEdit()
        self.usuario.setPlaceholderText("Usuario")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Contraseña")
        self.password.setEchoMode(QLineEdit.Password)

        boton = QPushButton("Iniciar Sesión")
        boton.clicked.connect(self.login)

        layout.addStretch()
        layout.addWidget(titulo)
        layout.addWidget(self.usuario)
        layout.addWidget(self.password)
        layout.addWidget(boton)
        layout.addStretch()

        self.setLayout(layout)

    def login(self):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM usuarios
        WHERE usuario=?
        AND password=?
        """, (
            self.usuario.text(),
            self.password.text()
        ))

        usuario = cursor.fetchone()

        conn.close()

        if usuario:
            self.callback()
            self.close()
        else:
            QMessageBox.warning(
                self,
                "Error",
                "Usuario o contraseña incorrectos"
            )