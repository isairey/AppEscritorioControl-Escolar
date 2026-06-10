from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QDate
from database import conectar


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName("dashboard")

        self.setStyleSheet("""
            QWidget {
                background-color: #0B0F1A;
                color: #E2E8F0;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel {
                color: #E2E8F0;
            }
            QListWidget {
                background-color: #0F172A;
                border: none;
                border-radius: 12px;
                padding: 10px;
                color: #94A3B8;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #1E293B;
            }
        """)

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(40, 40, 40, 40)
        mainLayout.setSpacing(20)

        # ==========================
        # HEADER
        # ==========================
        header = QFrame()
        header.setFixedHeight(100)
        header.setStyleSheet("background-color: #1E293B; border-radius: 16px;")

        headerLayout = QHBoxLayout()
        headerLayout.setContentsMargins(30, 0, 30, 0)

        # TITULO
        titulo = QLabel("TeacherDesk Pro")
        titulo.setStyleSheet("font-size: 26px; font-weight: 600; color: #F8FAFC;")

        fecha = QLabel(QDate.currentDate().toString("dddd, dd MMMM yyyy").title())
        fecha.setStyleSheet("font-size: 14px; color: #64748B; margin-top: 5px;")

        titleLayout = QVBoxLayout()
        titleLayout.addWidget(titulo)
        titleLayout.addWidget(fecha)
        titleLayout.addStretch()

        headerLayout.addLayout(titleLayout)
        headerLayout.addStretch()

        header.setLayout(headerLayout)

        mainLayout.addWidget(header)

        # ==========================
        # TARJETAS
        # ==========================
        cards = QHBoxLayout()
        cards.setSpacing(15)

        self.cardAlumnos = self.crear_card("ALUMNOS", "Total Alumnos", "#3B82F6")
        self.cardMaterias = self.crear_card("MATERIAS", "Total Materias", "#8B5CF6")
        self.cardPromedio = self.crear_card("PROMEDIO", "Promedio General", "#10B981")

        cards.addWidget(self.cardAlumnos["frame"])
        cards.addWidget(self.cardMaterias["frame"])
        cards.addWidget(self.cardPromedio["frame"])

        mainLayout.addLayout(cards)

        # ==========================
        # PANEL INFERIOR
        # ==========================
        bottom = QHBoxLayout()
        bottom.setSpacing(15)

        # ACTIVIDAD
        actividadFrame = QFrame()
        actividadFrame.setStyleSheet("background-color: #1E293B; border-radius: 16px;")

        actividadLayout = QVBoxLayout()
        actividadLayout.setContentsMargins(24, 24, 24, 24)
        actividadLayout.setSpacing(12)

        actividadLabel = QLabel("ACTIVIDAD RECIENTE")
        actividadLabel.setStyleSheet("font-size: 14px; font-weight: 600; color: #64748B; letter-spacing: 1px;")

        self.actividad = QListWidget()
        self.actividad.setStyleSheet("""
            QListWidget {
                background-color: #0F172A;
                border-radius: 10px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #1E293B;
                color: #CBD5E1;
            }
        """)

        actividadLayout.addWidget(actividadLabel)
        actividadLayout.addWidget(self.actividad)

        actividadFrame.setLayout(actividadLayout)

        # RESUMEN
        resumenFrame = QFrame()
        resumenFrame.setStyleSheet("background-color: #1E293B; border-radius: 16px;")

        resumenLayout = QVBoxLayout()
        resumenLayout.setContentsMargins(24, 24, 24, 24)
        resumenLayout.setSpacing(12)

        resumenLabel = QLabel("RESUMEN ESCOLAR")
        resumenLabel.setStyleSheet("font-size: 14px; font-weight: 600; color: #64748B; letter-spacing: 1px;")

        self.lblResumen = QLabel()
        self.lblResumen.setWordWrap(True)
        self.lblResumen.setStyleSheet("font-size: 14px; color: #94A3B8; line-height: 26px;")

        # Estado
        EstadoFrame = QFrame()
        EstadoFrame.setStyleSheet("background-color: #064E3B; border-radius: 8px; padding: 14px; margin-top: 8px;")

        EstadoLayout = QHBoxLayout()
        
        EstadoLabel = QLabel("SISTEMA ACTIVO")
        EstadoLabel.setStyleSheet("font-size: 13px; font-weight: 600; color: #34D399; letter-spacing: 1px;")

        EstadoLayout.addWidget(EstadoLabel)
        EstadoLayout.addStretch()

        EstadoFrame.setLayout(EstadoLayout)

        resumenLayout.addWidget(resumenLabel)
        resumenLayout.addWidget(self.lblResumen)
        resumenLayout.addWidget(EstadoFrame)

        resumenFrame.setLayout(resumenLayout)

        bottom.addWidget(actividadFrame, 2)
        bottom.addWidget(resumenFrame, 1)

        mainLayout.addLayout(bottom)

        self.setLayout(mainLayout)

        self.actualizar()

    # ==========================
    # CREAR TARJETAS
    # ==========================
    def crear_card(self, titulo_corto, titulo_largo, color):

        frame = QFrame()
        frame.setStyleSheet("background-color: #1E293B; border-radius: 16px;")

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # TITULO(CHICO)
        title = QLabel(titulo_corto)
        title.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {color}; letter-spacing: 1px;")

        # VALOR GRANDE
        value = QLabel("0")
        value.setStyleSheet("font-size: 42px; font-weight: 700; color: #F8FAFC; margin-top: 10px;")

        # DESCRIPCION
        desc = QLabel(titulo_largo)
        desc.setStyleSheet("font-size: 13px; color: #64748B;")

        layout.addWidget(title)
        layout.addWidget(value)
        layout.addWidget(desc)
        layout.addStretch()

        frame.setLayout(layout)

        return {"frame": frame, "valor": value}

    # ==========================
    # ACTUALIZAR
    # ==========================
    def actualizar(self):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM alumnos")
        alumnos = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM materias")
        materias = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(calificacion) FROM calificaciones")
        promedio = cursor.fetchone()[0]

        conn.close()

        promedio = round(promedio or 0, 2)

        self.cardAlumnos["valor"].setText(str(alumnos))
        self.cardMaterias["valor"].setText(str(materias))
        self.cardPromedio["valor"].setText(str(promedio))

        self.actividad.clear()
        self.actividad.addItem(f"Alumnos registrados: {alumnos}")
        self.actividad.addItem(f"Materias activas: {materias}")
        self.actividad.addItem(f"Promedio general: {promedio}")

        self.lblResumen.setText(
            f"<b>{alumnos}</b> Alumnos<br>"
            f"<b>{materias}</b> Materias<br>"
            f"<b>{promedio}</b> Promedio<br><br>"
            f"Actualizado: {QDate.currentDate().toString('dd/MM/yyyy')}"
        )