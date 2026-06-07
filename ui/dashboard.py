from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QDate
from database import conectar


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName("dashboard")

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(25, 25, 25, 25)
        mainLayout.setSpacing(20)

        # HEADER

        header = QFrame()
        header.setStyleSheet("""
            QFrame{
                background:qlineargradient(
                    x1:0,y1:0,x2:1,y2:0,
                    stop:0 #2563eb,
                    stop:1 #7c3aed
                );
                border-radius:20px;
            }
        """)

        headerLayout = QVBoxLayout()

        titulo = QLabel("🎓 TeacherDesk Pro")
        titulo.setStyleSheet("""
            font-size:30px;
            font-weight:bold;
            color:white;
        """)

        fecha = QLabel(
            QDate.currentDate().toString(
                "dddd dd MMMM yyyy"
            )
        )

        fecha.setStyleSheet("""
            color:white;
            font-size:14px;
        """)

        headerLayout.addWidget(titulo)
        headerLayout.addWidget(fecha)

        header.setLayout(headerLayout)

        mainLayout.addWidget(header)

        # TARJETAS

        cards = QHBoxLayout()

        self.cardAlumnos = self.crear_card(
            "👨‍🎓",
            "ALUMNOS",
            "#2563eb"
        )

        self.cardMaterias = self.crear_card(
            "📚",
            "MATERIAS",
            "#9333ea"
        )

        self.cardPromedio = self.crear_card(
            "📈",
            "PROMEDIO",
            "#16a34a"
        )

        cards.addWidget(
            self.cardAlumnos["frame"]
        )

        cards.addWidget(
            self.cardMaterias["frame"]
        )

        cards.addWidget(
            self.cardPromedio["frame"]
        )

        mainLayout.addLayout(cards)

        # PANEL INFERIOR

        bottom = QHBoxLayout()

        # ACTIVIDAD

        actividadFrame = QFrame()

        actividadFrame.setStyleSheet("""
            QFrame{
                background:#1a1a1a;
                border-radius:15px;
            }
        """)

        actividadLayout = QVBoxLayout()

        actividadTitulo = QLabel(
            "⚡ Actividad del Sistema"
        )

        actividadTitulo.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        self.actividad = QListWidget()

        actividadLayout.addWidget(
            actividadTitulo
        )

        actividadLayout.addWidget(
            self.actividad
        )

        actividadFrame.setLayout(
            actividadLayout
        )

        # RESUMEN

        resumenFrame = QFrame()

        resumenFrame.setStyleSheet("""
            QFrame{
                background:#1a1a1a;
                border-radius:15px;
            }
        """)

        resumenLayout = QVBoxLayout()

        resumenTitulo = QLabel(
            "📊 Resumen Escolar"
        )

        resumenTitulo.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        self.lblResumen = QLabel()

        self.lblResumen.setWordWrap(True)

        self.lblResumen.setStyleSheet("""
            font-size:15px;
            color:#cccccc;
        """)

        resumenLayout.addWidget(
            resumenTitulo
        )

        resumenLayout.addWidget(
            self.lblResumen
        )

        resumenFrame.setLayout(
            resumenLayout
        )

        bottom.addWidget(
            actividadFrame,
            2
        )

        bottom.addWidget(
            resumenFrame,
            1
        )

        mainLayout.addLayout(bottom)

        self.setLayout(mainLayout)

        self.actualizar()

    def crear_card(
        self,
        icono,
        titulo,
        color
    ):

        frame = QFrame()

        frame.setStyleSheet(f"""
            QFrame{{
                background:{color};
                border-radius:20px;
            }}
        """)

        layout = QVBoxLayout()

        icon = QLabel(icono)

        icon.setAlignment(
            Qt.AlignCenter
        )

        icon.setStyleSheet("""
            font-size:42px;
        """)

        title = QLabel(titulo)

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setStyleSheet("""
            font-size:16px;
            font-weight:bold;
            color:white;
        """)

        value = QLabel("0")

        value.setAlignment(
            Qt.AlignCenter
        )

        value.setStyleSheet("""
            font-size:34px;
            font-weight:bold;
            color:white;
        """)

        layout.addWidget(icon)
        layout.addWidget(title)
        layout.addWidget(value)

        frame.setLayout(layout)

        return {
            "frame": frame,
            "valor": value
        }

    def actualizar(self):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM alumnos"
        )
        alumnos = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM materias"
        )
        materias = cursor.fetchone()[0]

        cursor.execute("""
            SELECT AVG(calificacion)
            FROM calificaciones
        """)
        promedio = cursor.fetchone()[0]

        conn.close()

        promedio = round(
            promedio or 0,
            2
        )

        self.cardAlumnos["valor"].setText(
            str(alumnos)
        )

        self.cardMaterias["valor"].setText(
            str(materias)
        )

        self.cardPromedio["valor"].setText(
            str(promedio)
        )

        self.actividad.clear()

        self.actividad.addItem(
            f"👨‍🎓 Alumnos registrados: {alumnos}"
        )

        self.actividad.addItem(
            f"📚 Materias registradas: {materias}"
        )

        self.actividad.addItem(
            f"📈 Promedio general: {promedio}"
        )

        self.lblResumen.setText(
            f"""
Sistema escolar activo.

• Total de alumnos: {alumnos}

• Total de materias: {materias}

• Promedio general: {promedio}

Estado del sistema: Operativo ✅
"""
        )