import sys

from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

from database import crear_bd
from login import LoginWindow

from ui.dashboard import Dashboard
from ui.alumnos import AlumnosWidget
from ui.materias import MateriasWidget
from ui.calificaciones import CalificacionesWidget
from ui.asistencia import AsistenciaWidget
from ui.reportes import ReportesWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("🎓 TeacherDesk Pro")
        self.resize(1400, 800)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ==========================
        # MENU LATERAL
        # ==========================

        sidebar = QFrame()
        sidebar.setFixedWidth(260)

        sidebar.setStyleSheet("""
            QFrame {
                background-color: #0B0F1A;
            }
        """)

        sideLayout = QVBoxLayout()
        sideLayout.setContentsMargins(20, 30, 20, 20)
        sideLayout.setSpacing(8)

        # Logo
        logo = QLabel("🎓")
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("font-size: 40px;")

        logoTitulo = QLabel("TeacherDesk")
        logoTitulo.setAlignment(Qt.AlignCenter)
        logoTitulo.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #F8FAFC;
            padding: 5px;
        """)

        logoSub = QLabel("Sistema Escolar")
        logoSub.setAlignment(Qt.AlignCenter)
        logoSub.setStyleSheet("""
            font-size: 12px;
            color: #64748B;
            padding-bottom: 20px;
        """)

        sideLayout.addWidget(logo)
        sideLayout.addWidget(logoTitulo)
        sideLayout.addWidget(logoSub)

        # Botones
        self.btnDashboard = QPushButton(" 🏠  Dashboard")
        self.btnAlumnos = QPushButton(" 👨‍🎓  Alumnos")
        self.btnMaterias = QPushButton(" 📚  Materias")
        self.btnCalificaciones = QPushButton(" 📝  Calificaciones")
        self.btnAsistencia = QPushButton(" 📅  Asistencia")
        self.btnReportes = QPushButton(" 📊  Reportes")

        botones = [
            self.btnDashboard,
            self.btnAlumnos,
            self.btnMaterias,
            self.btnCalificaciones,
            self.btnAsistencia,
            self.btnReportes
        ]

        for btn in botones:
            btn.setMinimumHeight(48)
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding-left: 20px;
                    background-color: transparent;
                    color: #94A3B8;
                    border: none;
                    border-radius: 10px;
                    font-size: 15px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #1E293B;
                    color: #F8FAFC;
                }
            """)

            sideLayout.addWidget(btn)

        sideLayout.addStretch()

        # Version
        footer = QLabel("v1.0.0")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("""
            color: #475569;
            font-size: 12px;
            padding: 10px;
        """)

        sideLayout.addWidget(footer)

        sidebar.setLayout(sideLayout)

        # ==========================
        # CONTENIDO
        # ==========================

        self.stack = QStackedWidget()

        self.dashboard = Dashboard()
        self.alumnos = AlumnosWidget()
        self.materias = MateriasWidget()
        self.calificaciones = CalificacionesWidget()
        self.asistencia = AsistenciaWidget()
        self.reportes = ReportesWidget()

        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.alumnos)
        self.stack.addWidget(self.materias)
        self.stack.addWidget(self.calificaciones)
        self.stack.addWidget(self.asistencia)
        self.stack.addWidget(self.reportes)

        layout.addWidget(sidebar)
        layout.addWidget(self.stack)

        central.setLayout(layout)

        # ==========================
        # EVENTOS
        # ==========================
        self.btnDashboard.clicked.connect(lambda: self.mostrar_pagina(0))
        self.btnAlumnos.clicked.connect(lambda: self.mostrar_pagina(1))
        self.btnMaterias.clicked.connect(lambda: self.mostrar_pagina(2))
        self.btnCalificaciones.clicked.connect(lambda: self.mostrar_pagina(3))
        self.btnAsistencia.clicked.connect(lambda: self.mostrar_pagina(4))
        self.btnReportes.clicked.connect(lambda: self.mostrar_pagina(5))

    def mostrar_pagina(self, index):
        self.stack.setCurrentIndex(index)
        if index == 0:
            self.dashboard.actualizar()


def abrir_sistema():
    global ventana
    ventana = MainWindow()
    ventana.show()


if __name__ == "__main__":

    crear_bd()

    app = QApplication(sys.argv)

    app.setStyleSheet("""
        QWidget {
            background-color: #0B0F1A;
            color: #E2E8F0;
            font-family: 'Segoe UI', sans-serif;
            font-size: 14px;
        }

        QLabel {
            color: #CBD5E1;
        }

        QLineEdit,
        QComboBox,
        QDateEdit,
        QSpinBox,
        QDoubleSpinBox {
            background-color: #1E293B;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 12px;
            color: white;
        }

        QLineEdit:focus,
        QComboBox:focus {
            border-color: #3B82F6;
        }

        QLineEdit::placeholder {
            color: #64748B;
        }

        QPushButton {
            background-color: #3B82F6;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 12px 20px;
            font-weight: 600;
        }

        QPushButton:hover {
            background-color: #2563EB;
        }

        QPushButton:pressed {
            background-color: #1D4ED8;
        }

        QTableWidget {
            background-color: #0F172A;
            border: none;
            border-radius: 12px;
            gridline-color: #1E293B;
        }

        QTableWidget::item {
            padding: 12px;
            border-bottom: 1px solid #1E293B;
        }

        QTableWidget::item:selected {
            background-color: rgba(59, 130, 246, 0.2);
        }

        QHeaderView::section {
            background-color: #1E293B;
            padding: 14px;
            border: none;
            font-weight: 600;
            color: #94A3B8;
        }

        QListWidget {
            background-color: #1E293B;
            border: none;
            border-radius: 12px;
        }

        QListWidget::item {
            padding: 12px;
            border-bottom: 1px solid #334155;
        }

        QScrollBar:vertical {
            background: transparent;
            width: 8px;
        }

        QScrollBar::handle:vertical {
            background-color: #475569;
            border-radius: 4px;
        }

        QScrollBar::handle:vertical:hover {
            background-color: #64748B;
        }

        QMessageBox {
            background-color: #1E293B;
        }

        QMessageBox QPushButton {
            background-color: #3B82F6;
            padding: 8px 20px;
        }
    """)

    login = LoginWindow(abrir_sistema)
    login.show()

    sys.exit(app.exec())