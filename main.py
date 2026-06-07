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
        sidebar.setFixedWidth(240)

        sidebar.setStyleSheet("""
            QFrame{
                background:#0F172A;
                border-right:1px solid #1E293B;
            }
        """)

        sideLayout = QVBoxLayout()

        logo = QLabel("🎓 TeacherDesk")
        logo.setAlignment(Qt.AlignCenter)

        logo.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
            color:white;
            padding:20px;
        """)

        sideLayout.addWidget(logo)

        self.btnDashboard = QPushButton("🏠 Dashboard")
        self.btnAlumnos = QPushButton("👨‍🎓 Alumnos")
        self.btnMaterias = QPushButton("📚 Materias")
        self.btnCalificaciones = QPushButton("📝 Calificaciones")
        self.btnAsistencia = QPushButton("📅 Asistencia")
        self.btnReportes = QPushButton("📊 Reportes")

        botones = [
            self.btnDashboard,
            self.btnAlumnos,
            self.btnMaterias,
            self.btnCalificaciones,
            self.btnAsistencia,
            self.btnReportes
        ]

        for btn in botones:

            btn.setMinimumHeight(50)

            btn.setStyleSheet("""
                QPushButton{
                    text-align:left;
                    padding-left:20px;
                    border:none;
                    background:transparent;
                    color:white;
                    font-size:15px;
                }

                QPushButton:hover{
                    background:#1E293B;
                    border-radius:10px;
                }
            """)

            sideLayout.addWidget(btn)

        sideLayout.addStretch()

        footer = QLabel("v1.0.0")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("""
            color:#94A3B8;
            padding:15px;
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

        self.btnDashboard.clicked.connect(
            lambda: self.mostrar_pagina(0)
        )

        self.btnAlumnos.clicked.connect(
            lambda: self.mostrar_pagina(1)
        )

        self.btnMaterias.clicked.connect(
            lambda: self.mostrar_pagina(2)
        )

        self.btnCalificaciones.clicked.connect(
            lambda: self.mostrar_pagina(3)
        )

        self.btnAsistencia.clicked.connect(
            lambda: self.mostrar_pagina(4)
        )

        self.btnReportes.clicked.connect(
            lambda: self.mostrar_pagina(5)
        )

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

    QWidget{
        background:#020617;
        color:white;
        font-family:'Segoe UI';
        font-size:14px;
    }

    QLineEdit,
    QComboBox,
    QDateEdit,
    QSpinBox,
    QDoubleSpinBox{
        background:#111827;
        border:1px solid #334155;
        border-radius:10px;
        padding:8px;
        color:white;
    }

    QPushButton{
        background:#2563EB;
        color:white;
        border:none;
        border-radius:10px;
        padding:10px;
        font-weight:bold;
    }

    QPushButton:hover{
        background:#1D4ED8;
    }

    QTableWidget{
        background:#111827;
        border:none;
        border-radius:10px;
        gridline-color:#1E293B;
    }

    QHeaderView::section{
        background:#1E293B;
        padding:8px;
        border:none;
        font-weight:bold;
        color:white;
    }

    QListWidget{
        background:#111827;
        border:none;
        border-radius:10px;
        padding:10px;
    }

    QScrollBar:vertical{
        background:#0F172A;
        width:10px;
        border:none;
    }

    QScrollBar::handle:vertical{
        background:#334155;
        border-radius:5px;
    }

    QScrollBar::handle:vertical:hover{
        background:#475569;
    }

    """)

    login = LoginWindow(
        abrir_sistema
    )

    login.show()

    sys.exit(app.exec())