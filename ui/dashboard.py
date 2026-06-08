from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QDate
from database import conectar


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName("dashboard")

        # ESTILO GLOBAL
        self.setStyleSheet("""
            QWidget {
                background-color: #0B0F1A;
                color: #E2E8F0;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel {
                color: #CBD5E1;
            }
            QListWidget {
                background-color: #1E293B;
                border-radius: 12px;
                padding: 10px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #334155;
            }
        """)

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(30, 30, 30, 30)
        mainLayout.setSpacing(24)

        # ==========================
        # HEADER SIN BORDES
        # ==========================
        header = QFrame()
        header.setFixedHeight(120)

        header.setStyleSheet("""
            QFrame {
                background-color: #1E293B;
                border-radius: 20px;
            }
        """)

        headerLayout = QHBoxLayout()
        headerLayout.setContentsMargins(30, 20, 30, 20)

        icon_label = QLabel("🎓")
        icon_label.setStyleSheet("font-size: 48px;")

        text_col = QVBoxLayout()
        text_col.setSpacing(2)

        titulo = QLabel("TeacherDesk")
        titulo.setStyleSheet("font-size: 28px; font-weight: 700; color: #F8FAFC;")

        fecha = QLabel(QDate.currentDate().toString("dddd, dd 'de' MMMM 'de' yyyy"))
        fecha.setStyleSheet("font-size: 13px; color: #64748B;")

        text_col.addWidget(titulo)
        text_col.addWidget(fecha)

        headerLayout.addWidget(icon_label)
        headerLayout.addLayout(text_col)
        headerLayout.addStretch()

        header.setLayout(headerLayout)

        mainLayout.addWidget(header)

        # ==========================
        # TARJETAS
        # ==========================
        cards = QHBoxLayout()
        cards.setSpacing(20)

        self.cardAlumnos = self.crear_card("👨‍🎓", "Total Alumnos", "#3B82F6")
        self.cardMaterias = self.crear_card("📚", "Total Materias", "#8B5CF6")
        self.cardPromedio = self.crear_card("📊", "Promedio General", "#10B981")

        cards.addWidget(self.cardAlumnos["frame"])
        cards.addWidget(self.cardMaterias["frame"])
        cards.addWidget(self.cardPromedio["frame"])

        mainLayout.addLayout(cards)

        # ==========================
        # PANEL INFERIOR
        # ==========================
        bottom = QHBoxLayout()
        bottom.setSpacing(20)

        # ACTIVIDAD
        actividadFrame = QFrame()
        actividadFrame.setStyleSheet("""
            QFrame {
                background-color: #1E293B;
                border-radius: 20px;
            }
        """)

        actividadLayout = QVBoxLayout()
        actividadLayout.setContentsMargins(24, 24, 24, 24)
        actividadLayout.setSpacing(16)

        actividadTitulo = QHBoxLayout()
        
        actividadIcon = QLabel("⚡")
        actividadIcon.setStyleSheet("font-size: 24px;")

        actividadLabel = QLabel("Actividad Reciente")
        actividadLabel.setStyleSheet("font-size: 18px; font-weight: 700; color: #F8FAFC;")

        actividadTitulo.addWidget(actividadIcon)
        actividadTitulo.addWidget(actividadLabel)
        actividadTitulo.addStretch()

        self.actividad = QListWidget()
        self.actividad.setStyleSheet("""
            QListWidget {
                background-color: #0F172A;
                border-radius: 12px;
                padding: 8px;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #1E293B;
            }
        """)

        actividadLayout.addLayout(actividadTitulo)
        actividadLayout.addWidget(self.actividad)

        actividadFrame.setLayout(actividadLayout)

        # RESUMEN
        resumenFrame = QFrame()
        resumenFrame.setStyleSheet("""
            QFrame {
                background-color: #1E293B;
                border-radius: 20px;
            }
        """)

        resumenLayout = QVBoxLayout()
        resumenLayout.setContentsMargins(24, 24, 24, 24)
        resumenLayout.setSpacing(16)

        resumenTitulo = QHBoxLayout()
        
        resumenIcon = QLabel("📈")
        resumenIcon.setStyleSheet("font-size: 24px;")

        resumenLabel = QLabel("Resumen Escolar")
        resumenLabel.setStyleSheet("font-size: 18px; font-weight: 700; color: #F8FAFC;")

        resumenTitulo.addWidget(resumenIcon)
        resumenTitulo.addWidget(resumenLabel)
        resumenTitulo.addStretch()

        self.lblResumen = QLabel()
        self.lblResumen.setWordWrap(True)
        self.lblResumen.setStyleSheet("font-size: 14px; color: #94A3B8; line-height: 24px;")

        # Estado
        EstadoFrame = QFrame()
        EstadoFrame.setStyleSheet("""
            QFrame {
                background-color: #10B981;
                border-radius: 10px;
                padding: 12px;
                margin-top: 10px;
            }
        """)

        EstadoLayout = QHBoxLayout()
        
        estadoIcon = QLabel("🟢")
        estadoLabel = QLabel("Sistema Operativo")
        estadoLabel.setStyleSheet("font-weight: 700; color: white;")

        EstadoLayout.addWidget(estadoIcon)
        EstadoLayout.addWidget(estadoLabel)
        EstadoLayout.addStretch()

        EstadoFrame.setLayout(EstadoLayout)

        resumenLayout.addLayout(resumenTitulo)
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
    def crear_card(self, icono, titulo, color):

        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #1E293B;
                border-radius: 20px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        header = QFrame()
        header.setFixedHeight(60)
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 12px;
            }}
        """)

        headerLayout = QVBoxLayout()
        
        icon = QLabel(icono)
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet("font-size: 28px;")
        
        headerLayout.addWidget(icon)
        header.setLayout(headerLayout)

        title = QLabel(titulo)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 14px; font-weight: 600; color: #94A3B8;")

        value = QLabel("0")
        value.setAlignment(Qt.AlignCenter)
        value.setStyleSheet("font-size: 36px; font-weight: 700; color: #F8FAFC;")

        layout.addWidget(header)
        layout.addWidget(title)
        layout.addWidget(value)
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
        self.actividad.addItem(f"  👨‍🎓 Alumnos: {alumnos}")
        self.actividad.addItem(f"  📚 Materias: {materias}")
        self.actividad.addItem(f"  📊 Promedio: {promedio}")

        self.lblResumen.setText(
            f"""
- <b>{alumnos}</b> Alumnos
- <b>{materias}</b> Materias  
- <b>{promedio}</b> Promedio

<b>Actualizado:</b> {QDate.currentDate().toString("dd/MM/yyyy")}
            """
        )