
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication
from database import conectar


class LoginWindow(QWidget):

    def __init__(self, callback):
        super().__init__()

        self.callback = callback

        self.setWindowTitle("TeacherDesk Pro")
        self.resize(550, 650)

        self.setObjectName("LoginWindow")

        self.setStyleSheet("""
        #LoginWindow{
            background:qlineargradient(
                x1:0,y1:0,x2:1,y2:1,
                stop:0 #0F172A,
                stop:1 #1E293B
            );
        }
        """)

        self.centrar_ventana()

        # =========================
        # LAYOUT PRINCIPAL
        # =========================

        main_layout = QVBoxLayout()
        main_layout.addStretch()

        # =========================
        # TARJETA
        # =========================

        card = QFrame()
        card.setFixedWidth(430)

        card.setStyleSheet("""
        QFrame{
            background-color:#111827;
            border:2px solid #1E40AF;
            border-radius:25px;
        }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(35, 35, 35, 35)
        card_layout.setSpacing(15)

        # =========================
        # LOGO
        # =========================

        logo = QLabel("🎓")
        logo.setAlignment(Qt.AlignCenter)

        logo.setStyleSheet("""
        QLabel{
            font-size:80px;
            color:#60A5FA;
            border:none;
            background:transparent;
        }
        """)

        titulo = QLabel("TeacherDesk Pro")
        titulo.setAlignment(Qt.AlignCenter)

        titulo.setStyleSheet("""
        QLabel{
            color:white;
            font-size:30px;
            font-weight:800;
            background:transparent;
            border:none;
        }
        """)

        subtitulo = QLabel("Sistema Inteligente de Control Escolar")
        subtitulo.setAlignment(Qt.AlignCenter)

        subtitulo.setStyleSheet("""
        QLabel{
            color:#94A3B8;
            font-size:14px;
            font-weight:500;
            background:transparent;
            border:none;
        }
        """)

        separador = QFrame()
        separador.setFrameShape(QFrame.HLine)

        separador.setStyleSheet("""
        background:#334155;
        max-height:1px;
        border:none;
        """)

        # =========================
        # USUARIO
        # =========================

        lbl_usuario = QLabel("Usuario")

        lbl_usuario.setStyleSheet("""
        QLabel{
            color:#CBD5E1;
            font-size:14px;
            font-weight:600;
            border:none;
            background:transparent;
        }
        """)

        self.usuario = QLineEdit()
        self.usuario.setPlaceholderText("Ingrese su usuario")
        self.usuario.setFixedHeight(50)

        self.usuario.setStyleSheet("""
        QLineEdit{
            background:#0F172A;
            border:2px solid #334155;
            border-radius:14px;
            padding-left:15px;
            color:white;
            font-size:14px;
        }

        QLineEdit:focus{
            border:2px solid #60A5FA;
        }

        QLineEdit::placeholder{
            color:#64748B;
        }
        """)

        # =========================
        # PASSWORD
        # =========================

        lbl_password = QLabel("Contraseña")

        lbl_password.setStyleSheet("""
        QLabel{
            color:#CBD5E1;
            font-size:14px;
            font-weight:600;
            border:none;
            background:transparent;
        }
        """)

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText("Ingrese su contraseña")
        self.password.setFixedHeight(50)

        self.password.setStyleSheet("""
        QLineEdit{
            background:#0F172A;
            border:2px solid #334155;
            border-radius:14px;
            padding-left:15px;
            color:white;
            font-size:14px;
        }

        QLineEdit:focus{
            border:2px solid #60A5FA;
        }

        QLineEdit::placeholder{
            color:#64748B;
        }
        """)

        # =========================
        # BOTÓN
        # =========================

        boton = QPushButton("Iniciar Sesión")
        boton.setCursor(Qt.PointingHandCursor)
        boton.setFixedHeight(55)

        boton.setStyleSheet("""
        QPushButton{
            background-color:#2563EB;
            border:none;
            border-radius:14px;
            color:white;
            font-size:16px;
            font-weight:700;
        }

        QPushButton:hover{
            background-color:#3B82F6;
        }

        QPushButton:pressed{
            background-color:#1D4ED8;
        }
        """)

        # =========================
        # MENSAJE
        # =========================

        self.mensaje = QLabel("")
        self.mensaje.setAlignment(Qt.AlignCenter)

        self.mensaje.setStyleSheet("""
        QLabel{
            color:#EF4444;
            font-size:13px;
            font-weight:600;
            border:none;
            background:transparent;
        }
        """)

        # =========================
        # FOOTER
        # =========================

        footer = QLabel("Versión 2.0 • TeacherDesk Pro")
        footer.setAlignment(Qt.AlignCenter)

        footer.setStyleSheet("""
        QLabel{
            color:#64748B;
            font-size:11px;
            border:none;
            background:transparent;
        }
        """)

        # =========================
        # AGREGAR WIDGETS
        # =========================

        card_layout.addWidget(logo)
        card_layout.addWidget(titulo)
        card_layout.addWidget(subtitulo)
        card_layout.addWidget(separador)

        card_layout.addWidget(lbl_usuario)
        card_layout.addWidget(self.usuario)

        card_layout.addWidget(lbl_password)
        card_layout.addWidget(self.password)

        card_layout.addSpacing(10)

        card_layout.addWidget(boton)
        card_layout.addWidget(self.mensaje)

        card_layout.addSpacing(10)

        card_layout.addWidget(footer)

        main_layout.addWidget(card, alignment=Qt.AlignCenter)
        main_layout.addStretch()

        self.setLayout(main_layout)

        boton.clicked.connect(self.login)
        self.password.returnPressed.connect(self.login)

    def centrar_ventana(self):
        pantalla = QGuiApplication.primaryScreen().availableGeometry()

        x = pantalla.x() + (pantalla.width() - self.width()) // 2
        y = pantalla.y() + (pantalla.height() - self.height()) // 2

        self.move(x, y)

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

