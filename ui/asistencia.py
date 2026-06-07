from PySide6.QtWidgets import *
from PySide6.QtCore import QDate
from database import conectar


class AsistenciaWidget(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        form = QHBoxLayout()

        self.cbAlumno = QComboBox()

        self.fecha = QDateEdit()
        self.fecha.setDate(QDate.currentDate())

        self.estado = QComboBox()
        self.estado.addItems([
            "Presente",
            "Retardo",
            "Falta"
        ])

        self.btnGuardar = QPushButton(
            "Registrar"
        )

        form.addWidget(QLabel("Alumno"))
        form.addWidget(self.cbAlumno)

        form.addWidget(QLabel("Fecha"))
        form.addWidget(self.fecha)

        form.addWidget(QLabel("Estado"))
        form.addWidget(self.estado)

        form.addWidget(self.btnGuardar)

        layout.addLayout(form)

        self.tabla = QTableWidget()

        self.tabla.setColumnCount(4)

        self.tabla.setHorizontalHeaderLabels([
            "Alumno",
            "Fecha",
            "Estado",
            "ID"
        ])

        layout.addWidget(self.tabla)

        self.setLayout(layout)

        self.btnGuardar.clicked.connect(
            self.registrar
        )

        self.cargar_alumnos()
        self.cargar_tabla()

    def cargar_alumnos(self):

        self.cbAlumno.clear()

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id,nombre,apellido
        FROM alumnos
        """)

        for alumno in cursor.fetchall():

            self.cbAlumno.addItem(
                f"{alumno[1]} {alumno[2]}",
                alumno[0]
            )

        conn.close()

    def registrar(self):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO asistencia(
            alumno_id,
            fecha,
            estado
        )
        VALUES(?,?,?)
        """,(
            self.cbAlumno.currentData(),
            self.fecha.date().toString(
                "yyyy-MM-dd"
            ),
            self.estado.currentText()
        ))

        conn.commit()
        conn.close()

        self.cargar_tabla()

    def cargar_tabla(self):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT
        a.nombre || ' ' || a.apellido,
        s.fecha,
        s.estado,
        s.id
        FROM asistencia s
        INNER JOIN alumnos a
        ON a.id=s.alumno_id
        ORDER BY s.fecha DESC
        """)

        datos = cursor.fetchall()

        conn.close()

        self.tabla.setRowCount(
            len(datos)
        )

        for fila,dato in enumerate(datos):

            for columna,valor in enumerate(dato):

                self.tabla.setItem(
                    fila,
                    columna,
                    QTableWidgetItem(
                        str(valor)
                    )
                )