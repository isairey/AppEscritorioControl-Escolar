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

        self.tabla.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.tabla.setAlternatingRowColors(False)  # 🔥 quitamos blanco/negro feo
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla.verticalHeader().setVisible(False)

        # 🔥 filas más altas (arregla botón aplastado)
        self.tabla.verticalHeader().setDefaultSectionSize(40)

        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        main_layout.addWidget(self.tabla)

        self.setLayout(main_layout)

        # ===================== EVENTOS =====================
        self.btnGuardar.clicked.connect(self.registrar)

        self.cargar_alumnos()
        self.cargar_materias()
        self.cargar_tabla()

    # ===================== ESTILOS PRO =====================
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
            padding: 7px;
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
            border-radius: 10px;
        }

        QHeaderView::section {
            background-color: #334155;
            padding: 8px;
            font-weight: bold;
            color: white;
            border: none;
        }

        QTableWidget::item {
            padding: 10px;
            color: #e5e7eb;
        }

        QTableWidget::item:selected {
            background-color: #2563eb;
        }

        QTableWidget::item:hover {
            background-color: #243244;
        }
        """

    # ===================== ALUMNOS =====================
    def cargar_alumnos(self):
        self.cbAlumno.clear()
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT id, nombre, apellido FROM alumnos")

        for a in cursor.fetchall():
            self.cbAlumno.addItem(f"{a[1]} {a[2]}", a[0])

        conn.close()

    # ===================== MATERIAS =====================
    def cargar_materias(self):
        self.cbMateria.clear()
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT id, nombre FROM materias")
        materias = cursor.fetchall()  # Guardar en variable primero
        print(f"Materias cargadas: {len(materias)}")  # Ahora sí funciona
        for m in materias:
            self.cbMateria.addItem(m[1], m[0])

        conn.close()

   # ===================== REGISTRAR =====================
    # ===================== REGISTRAR =====================
    def registrar(self):

        
        if self.cbAlumno.count() == 0:
            QMessageBox.warning(
                self,
                "Aviso",
                "No hay alumnos registrados."
            )
            return

        if self.cbMateria.count() == 0:
            QMessageBox.warning(
                self,
                "Aviso",
                "No hay materias registradas."
            )
            return

        # Obtener los valores
        alumno_id = self.cbAlumno.currentData()
        materia_id = self.cbMateria.currentData()
        fecha = self.fecha.date().toString("yyyy-MM-dd")

        conn = conectar()
        cursor = conn.cursor()

        # Verificar si ya existe LAS TRES condiciones juntas
        cursor.execute("""
            SELECT id FROM asistencia
            WHERE alumno_id = ?
            AND materia_id = ?
            AND fecha = ?
        """, (alumno_id, materia_id, fecha))

        existe = cursor.fetchone()
        print(existe) 
        print(alumno_id, materia_id, fecha)
        print(f"alumno: {alumno_id}, materia: {materia_id}, fecha: {fecha}")
        print(f"alumno index: {self.cbAlumno.currentIndex()}, materia index: {self.cbMateria.currentIndex()}")
        if existe:
            conn.close()
            QMessageBox.warning(
                self,
                "Asistencia Duplicada",
                "Este alumno ya tiene asistencia registrada para esta materia en esa fecha."
            )
            return

        # Registrar nueva asistencia
        cursor.execute("""
            INSERT INTO asistencia (alumno_id, materia_id, fecha, estado)
            VALUES (?, ?, ?, ?)
        """, (alumno_id, materia_id, fecha, self.estado.currentText()))

        conn.commit()
        conn.close()

        self.cargar_tabla()

        QMessageBox.information(
            self,
            "Correcto",
            "Asistencia registrada correctamente."
        )
    # ===================== TABLA =====================
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
                item = QTableWidgetItem(str(valor))
                item.setTextAlignment(Qt.AlignCenter)
                self.tabla.setItem(fila, col, item)

            btn = QPushButton("✏ Editar")
            btn.setMinimumHeight(30)
            btn.setMinimumWidth(90)

            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3b82f6;
                    color: white;
                    border-radius: 8px;
                    padding: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2563eb;
                }
            """)

            btn.clicked.connect(lambda _, r=dato: self.editar_asistencia(r))

            self.tabla.setCellWidget(fila, 5, btn)

    # ===================== EDITAR =====================
    def editar_asistencia(self, dato):
        id_asistencia = dato[4]

        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Asistencia")
        dialog.setFixedWidth(320)

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

        filtrados = [
            fila for fila in self.datos
            if texto in str(fila[0]).lower()
            or texto in str(fila[1]).lower()
            or texto in str(fila[3]).lower()
        ]

        self.mostrar_tabla(filtrados)

    def showEvent(self, event):
        super().showEvent(event)

        self.cargar_alumnos()
        self.cargar_materias()
        self.cargar_tabla()