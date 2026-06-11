from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from database import conectar


class LoginWindow(QWidget):

    def __init__(self, callback):
        super().__init__()

        self.callback = callback

        self.setWindowTitle("TeacherDesk Pro - Login")
        self.resize(450, 400)
        self.setStyleSheet("""
            QWidget {
                background-color: #0F172A;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # ===================== TÍTULO =====================
        titulo = QLabel(" TeacherDesk Pro")
        titulo.setFont(QFont("Arial", 24, QFont.Bold))
        titulo.setStyleSheet("color: white;")
        titulo.setAlignment(Qt.AlignCenter)

        subtitulo = QLabel("Control Escolar")
        subtitulo.setFont(QFont("Arial", 12))
        subtitulo.setStyleSheet("color: #94A3B8;")
        subtitulo.setAlignment(Qt.AlignCenter)

        # ===================== FORM =====================
        form = QVBoxLayout()
        form.setSpacing(15)

        label_usuario = QLabel(" Usuario")
        label_usuario.setStyleSheet("color: #CBD5E1; font-size: 14px;")

        self.usuario = QLineEdit()
        self.usuario.setPlaceholderText("Ingresa tu usuario")
        self.usuario.setFixedHeight(45)
        self.usuario.setStyleSheet("""
            QLineEdit {
                background-color: #1E293B;
                border: 2px solid #334155;
                border-radius: 10px;
                padding: 10px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3B82F6;
            }
            QLineEdit::placeholder {
                color: #64748B;
            }
        """)

        label_password = QLabel(" Contraseña")
        label_password.setStyleSheet("color: #CBD5E1; font-size: 14px;")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Ingresa tu contraseña")
        self.password.setFixedHeight(45)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet("""
            QLineEdit {
                background-color: #1E293B;
                border: 2px solid #334155;
                border-radius: 10px;
                padding: 10px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3B82F6;
            }
            QLineEdit::placeholder {
                color: #64748B;
            }
        """)

        # ===================== BOTÓN =====================
        boton = QPushButton(" Iniciar Sesión")
        boton.setFixedHeight(50)
        boton.setCursor(Qt.PointingHandCursor)
        boton.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                border: none;
                border-radius: 10px;
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
            QPushButton:pressed {
                background-color: #1D4ED8;
            }
        """)

        # ===================== MENSAJE =====================
        self.mensaje = QLabel("")
        self.mensaje.setAlignment(Qt.AlignCenter)
        self.mensaje.setStyleSheet("color: #EF4444; font-size: 12px;")

        # ===================== AGREGAR AL LAYOUT =====================
        layout.addStretch()
        layout.addWidget(titulo)
        layout.addWidget(subtitulo)
        layout.addStretch()

        form.addWidget(label_usuario)
        form.addWidget(self.usuario)
        form.addWidget(label_password)
        form.addWidget(self.password)

        layout.addLayout(form)
        layout.addWidget(boton)
        layout.addWidget(self.mensaje)
        layout.addStretch()

        self.setLayout(layout)

        # ===================== EVENTO =====================
        boton.clicked.connect(self.login)
        self.password.returnPressed.connect(self.login)

    def login(self):
        usuario = self.usuario.text().strip()
        password = self.password.text().strip()

        if not usuario or not password:
            self.mensaje.setText("⚠️ Ingresa usuario y contraseña")
            return

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, usuario, rol
            FROM usuarios
            WHERE usuario = ?
            AND password = ?
        """, (usuario, password))

        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            self.mensaje.setText("")
            self.callback()
            self.close()
        else:
            self.mensaje.setText("❌ Usuario o contraseña incorrectos")
            self.password.clear()