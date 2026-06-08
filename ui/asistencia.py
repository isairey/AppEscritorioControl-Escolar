from PySide6.QtWidgets import *
from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QFont
from database import conectar


class AsistenciaWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Control de Asistencia")
        self.setStyleSheet(self.styles())

        self.datos = []

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # ===================== TÍTULO =====================
        titulo = QLabel("📋 Registro de Asistencia")
        titulo.setFont(QFont("Arial", 18, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(titulo)

        # ===================== BUSCADOR =====================
        self.txtBuscar = QLineEdit()
        self.txtBuscar.setPlaceholderText("🔎 Buscar alumno, materia o estado...")
        self.txtBuscar.textChanged.connect(self.filtrar_tabla)

        main_layout.addWidget(self.txtBuscar)

        # ===================== FORM =====================
        form = QHBoxLayout()

        self.cbAlumno = QComboBox()
        self.cbMateria = QComboBox()

        self.fecha = QDateEdit()
        self.fecha.setCalendarPopup(True)
        self.fecha.setDate(QDate.currentDate())

        self.estado = QComboBox()
        self.estado.addItems(["Presente", "Retardo", "Falta"])

        self.btnGuardar = QPushButton("➕ Registrar")

        form.addWidget(QLabel("Alumno"))
        form.addWidget(self.cbAlumno)

        form.addWidget(QLabel("Materia"))
        form.addWidget(self.cbMateria)

        form.addWidget(QLabel("Fecha"))
        form.addWidget(self.fecha)

        form.addWidget(QLabel("Estado"))
        form.addWidget(self.estado)

        form.addWidget(self.btnGuardar)

        main_layout.addLayout(form)

        # ===================== TABLA =====================
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels([
            "Alumno",
            "Materia",
            "Fecha",
            "Estado",
            "ID",
            "Acción"
        ])

        self.tabla.setAlternatingRowColors(True)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla.verticalHeader().setVisible(False)

        main_layout.addWidget(self.tabla)

        self.setLayout(main_layout)

        # ===================== EVENTOS =====================
        self.btnGuardar.clicked.connect(self.registrar)

        self.cargar_alumnos()
        self.cargar_materias()
        self.cargar_tabla()

    # ===================== ESTILOS =====================
    def styles(self):
        return """
        QWidget {
            background-color: #0b1220;
            color: #e5e7eb;
            font-size: 14px;
        }

        QLineEdit, QComboBox, QDateEdit {
            background-color: #334155;
            border: 1px solid #475569;
            padding: 6px;
            border-radius: 8px;
            color: white;
        }

        QPushButton {
            background-color: #22c55e;
            padding: 8px;
            border-radius: 8px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #16a34a;
        }

        QTableWidget {
            background-color: #1e293b;
            gridline-color: #334155;
            selection-background-color: #2563eb;
        }

        QHeaderView::section {
            background-color: #334155;
            padding: 6px;
            font-weight: bold;
            color: white;
        }

        QTableWidget::item {
            padding: 6px;
        }
        """

    # ===================== CARGAR ALUMNOS =====================
    def cargar_alumnos(self):
        self.cbAlumno.clear()
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT id, nombre, apellido FROM alumnos")

        for a in cursor.fetchall():
            self.cbAlumno.addItem(f"{a[1]} {a[2]}", a[0])

        conn.close()

    # ===================== CARGAR MATERIAS =====================
    def cargar_materias(self):
        self.cbMateria.clear()
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT id, nombre FROM materias")

        for m in cursor.fetchall():
            self.cbMateria.addItem(m[1], m[0])

        conn.close()

    # ===================== REGISTRAR =====================
    def registrar(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO asistencia (alumno_id, materia_id, fecha, estado)
        VALUES (?, ?, ?, ?)
        """, (
            self.cbAlumno.currentData(),
            self.cbMateria.currentData(),
            self.fecha.date().toString("yyyy-MM-dd"),
            self.estado.currentText()
        ))

        conn.commit()
        conn.close()

        self.cargar_tabla()

    # ===================== CARGAR TABLA =====================
    def cargar_tabla(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT 
            a.nombre || ' ' || a.apellido,
            m.nombre,
            s.fecha,
            s.estado,
            s.id
        FROM asistencia s
        INNER JOIN alumnos a ON a.id = s.alumno_id
        INNER JOIN materias m ON m.id = s.materia_id
        ORDER BY s.fecha DESC
        """)

        self.datos = cursor.fetchall()
        conn.close()

        self.mostrar_tabla(self.datos)

    # ===================== MOSTRAR TABLA =====================
    def mostrar_tabla(self, datos):
        self.tabla.setRowCount(len(datos))

        for fila, dato in enumerate(datos):
            for col, valor in enumerate(dato):
                self.tabla.setItem(fila, col, QTableWidgetItem(str(valor)))

            # Botón editar
            btn = QPushButton("✏ Editar")
            btn.clicked.connect(lambda _, r=dato: self.editar_asistencia(r))

            self.tabla.setCellWidget(fila, 5, btn)

    # ===================== EDITAR =====================
    def editar_asistencia(self, dato):
        id_asistencia = dato[4]

        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Asistencia")
        layout = QVBoxLayout(dialog)

        cbEstado = QComboBox()
        cbEstado.addItems(["Presente", "Retardo", "Falta"])
        cbEstado.setCurrentText(dato[3])

        btnGuardar = QPushButton("Guardar cambios")

        layout.addWidget(QLabel("Estado"))
        layout.addWidget(cbEstado)
        layout.addWidget(btnGuardar)

        def guardar():
            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("""
            UPDATE asistencia
            SET estado = ?
            WHERE id = ?
            """, (cbEstado.currentText(), id_asistencia))

            conn.commit()
            conn.close()

            dialog.close()
            self.cargar_tabla()

        btnGuardar.clicked.connect(guardar)

        dialog.exec()

    # ===================== FILTRO =====================
    def filtrar_tabla(self):
        texto = self.txtBuscar.text().lower()

        filtrados = []

        for fila in self.datos:
            alumno = str(fila[0]).lower()
            materia = str(fila[1]).lower()
            estado = str(fila[3]).lower()

            if texto in alumno or texto in materia or texto in estado:
                filtrados.append(fila)

        self.mostrar_tabla(filtrados)