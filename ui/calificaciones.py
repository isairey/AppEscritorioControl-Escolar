from PySide6.QtWidgets import *
from database import conectar


class CalificacionesWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.id_actual = None

        layout = QVBoxLayout()

        # FORMULARIO

        form = QHBoxLayout()

        self.cbAlumno = QComboBox()
        self.cbMateria = QComboBox()

        self.calificacion = QDoubleSpinBox()
        self.calificacion.setRange(0, 10)
        self.calificacion.setDecimals(1)

        form.addWidget(QLabel("Alumno"))
        form.addWidget(self.cbAlumno)

        form.addWidget(QLabel("Materia"))
        form.addWidget(self.cbMateria)

        form.addWidget(QLabel("Calificación"))
        form.addWidget(self.calificacion)

        layout.addLayout(form)

        # BOTONES

        botones = QHBoxLayout()

        self.btnAgregar = QPushButton("Guardar")
        self.btnEditar = QPushButton("Editar")
        self.btnEliminar = QPushButton("Eliminar")

        botones.addWidget(self.btnAgregar)
        botones.addWidget(self.btnEditar)
        botones.addWidget(self.btnEliminar)

        layout.addLayout(botones)

        # TABLA

        self.tabla = QTableWidget()

        self.tabla.setColumnCount(5)

        self.tabla.setHorizontalHeaderLabels([
            "ID",
            "Alumno",
            "Materia",
            "Calificación",
            "Promedio Alumno"
        ])

        self.tabla.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(self.tabla)

        self.setLayout(layout)

        # EVENTOS

        self.btnAgregar.clicked.connect(
            self.agregar
        )

        self.btnEditar.clicked.connect(
            self.editar
        )

        self.btnEliminar.clicked.connect(
            self.eliminar
        )

        self.tabla.cellClicked.connect(
            self.cargar_datos
        )

        self.cargar_combobox()
        self.cargar_tabla()

    # -----------------------------------

    def cargar_combobox(self):

        self.cbAlumno.clear()
        self.cbMateria.clear()

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id,nombre,apellido
        FROM alumnos
        """)

        alumnos = cursor.fetchall()

        for alumno in alumnos:

            self.cbAlumno.addItem(
                f"{alumno[1]} {alumno[2]}",
                alumno[0]
            )

        cursor.execute("""
        SELECT id,nombre
        FROM materias
        """)

        materias = cursor.fetchall()

        for materia in materias:

            self.cbMateria.addItem(
                materia[1],
                materia[0]
            )

        conn.close()

    # -----------------------------------

    def promedio_alumno(self, alumno_id):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT AVG(calificacion)
        FROM calificaciones
        WHERE alumno_id=?
        """, (alumno_id,))

        promedio = cursor.fetchone()[0]

        conn.close()

        return round(promedio or 0, 2)

    # -----------------------------------

    def cargar_tabla(self):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT
            c.id,
            a.nombre || ' ' || a.apellido,
            m.nombre,
            c.calificacion,
            c.alumno_id
        FROM calificaciones c
        INNER JOIN alumnos a
        ON c.alumno_id=a.id
        INNER JOIN materias m
        ON c.materia_id=m.id
        """)

        datos = cursor.fetchall()

        conn.close()

        self.tabla.setRowCount(
            len(datos)
        )

        for fila, dato in enumerate(datos):

            promedio = self.promedio_alumno(
                dato[4]
            )

            self.tabla.setItem(
                fila, 0,
                QTableWidgetItem(str(dato[0]))
            )

            self.tabla.setItem(
                fila, 1,
                QTableWidgetItem(dato[1])
            )

            self.tabla.setItem(
                fila, 2,
                QTableWidgetItem(dato[2])
            )

            self.tabla.setItem(
                fila, 3,
                QTableWidgetItem(str(dato[3]))
            )

            self.tabla.setItem(
                fila, 4,
                QTableWidgetItem(str(promedio))
            )

    # -----------------------------------

    def agregar(self):

        alumno_id = self.cbAlumno.currentData()
        materia_id = self.cbMateria.currentData()

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO calificaciones
        (
            alumno_id,
            materia_id,
            calificacion
        )
        VALUES(?,?,?)
        """, (
            alumno_id,
            materia_id,
            self.calificacion.value()
        ))

        conn.commit()
        conn.close()

        self.cargar_tabla()

    # -----------------------------------

    def editar(self):

        if not self.id_actual:
            return

        alumno_id = self.cbAlumno.currentData()
        materia_id = self.cbMateria.currentData()

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE calificaciones
        SET
            alumno_id=?,
            materia_id=?,
            calificacion=?
        WHERE id=?
        """, (
            alumno_id,
            materia_id,
            self.calificacion.value(),
            self.id_actual
        ))

        conn.commit()
        conn.close()

        self.cargar_tabla()

    # -----------------------------------

    def eliminar(self):

        if not self.id_actual:
            return

        respuesta = QMessageBox.question(
            self,
            "Eliminar",
            "¿Eliminar calificación?"
        )

        if respuesta != QMessageBox.Yes:
            return

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM calificaciones
        WHERE id=?
        """, (
            self.id_actual,
        ))

        conn.commit()
        conn.close()

        self.cargar_tabla()

    # -----------------------------------

    def cargar_datos(self, fila):

        self.id_actual = int(
            self.tabla.item(
                fila, 0
            ).text()
        )