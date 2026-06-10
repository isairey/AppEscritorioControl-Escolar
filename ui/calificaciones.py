from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from database import conectar


class CalificacionesWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.id_actual = None

        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(18)

        header = QFrame()
        header.setStyleSheet("""
            QFrame{
                background:qlineargradient(x1:0,y1:0,x2:1,y2:0,
                stop:0 #1E293B, stop:1 #0F172A);
                border-radius:15px;
                padding:18px;
            }
        """)

        h = QVBoxLayout()

        titulo = QLabel(" Gestión de Calificaciones")
        titulo.setStyleSheet("font-size:30px;font-weight:bold;color:white;")

        subtitulo = QLabel("Sistema escolar profesional")
        subtitulo.setStyleSheet("color:#94A3B8;font-size:14px;")

        h.addWidget(titulo)
        h.addWidget(subtitulo)

        header.setLayout(h)
        layout.addWidget(header)

        self.tabs = QTabWidget()

        self.tabs.setStyleSheet("""
            QTabWidget::pane{border:none;}

            QTabBar::tab{
                background:#111827;
                color:#94A3B8;
                padding:10px;
                border-radius:10px;
                margin-right:5px;
            }

            QTabBar::tab:selected{
                background:#2563EB;
                color:white;
            }
        """)

        self.tabRegistro = QWidget()
        self.tabLista = QWidget()

        self.tabs.addTab(self.tabRegistro, " Registro")
        self.tabs.addTab(self.tabLista, " Lista")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self.ui_registro()
        self.ui_lista()

        self.cargar_combobox()
        self.cargar_tabla()

    def ui_registro(self):

        layout = QVBoxLayout()

        card = QFrame()
        card.setStyleSheet("background:#0B1220;border-radius:15px;padding:20px;")

        form = QGridLayout()

        self.cbAlumno = QComboBox()
        self.cbMateria = QComboBox()
        
        # NUEVO: Selector de parcial
        self.cbParcial = QComboBox()
        self.cbParcial.addItems(["1er Parcial", "2do Parcial", "3er Parcial"])

        self.calificacion = QDoubleSpinBox()
        self.calificacion.setRange(0, 10)
        self.calificacion.setDecimals(1)

        for w in [self.cbAlumno, self.cbMateria, self.cbParcial, self.calificacion]:
            w.setStyleSheet("""
                background:#111827;border:1px solid #1F2937;
                border-radius:10px;padding:10px;color:white;
            """)

        form.addWidget(QLabel("Alumno"), 0, 0)
        form.addWidget(self.cbAlumno, 1, 0)

        form.addWidget(QLabel("Materia"), 0, 1)
        form.addWidget(self.cbMateria, 1, 1)
        
        form.addWidget(QLabel("Parcial"), 0, 2)
        form.addWidget(self.cbParcial, 1, 2)

        form.addWidget(QLabel("Calificación"), 2, 0)
        form.addWidget(self.calificacion, 3, 0, 1, 2)

        self.btnGuardar = QPushButton(" Guardar")
        self.btnGuardar.clicked.connect(self.guardar_calificacion)
        self.btnGuardar.setStyleSheet("""
            QPushButton{background:#16A34A;color:white;
            padding:12px;border-radius:10px;font-weight:bold;}
        """)

        form.addWidget(self.btnGuardar, 4, 0, 1, 2)

        card.setLayout(form)
        layout.addWidget(card)
        layout.addStretch()

        self.tabRegistro.setLayout(layout)

    def ui_lista(self):

        layout = QVBoxLayout()

        self.buscar = QLineEdit()
        self.buscar.setPlaceholderText(" Buscar alumno o materia...")
        self.buscar.textChanged.connect(self.buscar_calificacion)

        self.buscar.setStyleSheet("""
            QLineEdit{
                background:#0B1220;
                border:1px solid #1F2937;
                border-radius:10px;
                padding:10px;
                color:white;
            }
        """)

        layout.addWidget(self.buscar)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)

        self.tabla.setHorizontalHeaderLabels([
            "ID", "Alumno", "Materia",
            "Calificación", "Promedio", "Acciones"
        ])

        # FILAS MÁS ALTAS
        self.tabla.verticalHeader().setDefaultSectionSize(50)  # <-- altO de fila

        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        
        # ESTILO DE TABLA
        self.tabla.setStyleSheet("""
            QTableWidget {
                background-color: #0B1220;
                border: none;
                border-radius: 10px;
            }
            QTableWidget::item {
                padding: 10px;
                color: #E2E8F0;
            }
            QTableWidget::item:selected {
                background-color: #2563EB;
            }
            QHeaderView::section {
                background-color: #1E293B;
                padding: 12px;
                color: #94A3B8;
                font-weight: bold;
                border: none;
            }
        """)

        layout.addWidget(self.tabla)

        self.tabLista.setLayout(layout)

    def cargar_combobox(self):

        self.cbAlumno.clear()
        self.cbMateria.clear()

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT id,nombre,apellido FROM alumnos")

        for a in cursor.fetchall():
            self.cbAlumno.addItem(f"{a[1]} {a[2]}", a[0])

        cursor.execute("SELECT id,nombre FROM materias")

        for m in cursor.fetchall():
            self.cbMateria.addItem(m[1], m[0])

        conn.close()

    def promedio_alumno(self, alumno_id):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT AVG(calificacion) FROM calificaciones WHERE alumno_id=?",
            (alumno_id,)
        )

        promedio = cursor.fetchone()[0]
        conn.close()

        return round(promedio or 0, 2)

    def guardar_calificacion(self):

        if self.cbAlumno.count() == 0:
            QMessageBox.warning(self, "Aviso", "No hay alumnos.")
            return

        if self.cbMateria.count() == 0:
            QMessageBox.warning(self, "Aviso", "No hay materias.")
            return
        
        if self.calificacion.value() == 0:
            QMessageBox.warning(self, "Aviso", "Ingresa una calificación válida.")
            return

        alu_id = self.cbAlumno.currentData()
        mat_id = self.cbMateria.currentData()
        
        # Obtener parcial (1, 2, 3)
        parcial = self.cbParcial.currentIndex() + 1

        if alu_id is None or mat_id is None:
            QMessageBox.warning(self, "Aviso", "Selecciona alumno y materia.")
            return

        conn = conectar()
        cursor = conn.cursor()

        # Verificar duplicado (incluyendo parcial)
        if self.id_actual is None:
            cursor.execute("""
               SELECT id FROM calificaciones
                WHERE alumno_id = ? AND materia_id = ? AND parcial = ?
            """, (alu_id, mat_id, parcial))

            if cursor.fetchone():
                QMessageBox.warning(self, "Duplicado", "Ya existe calificación para este parcial.")
                conn.close()
                return

            cursor.execute("""
                INSERT INTO calificaciones (alumno_id, materia_id, parcial, calificacion)
                VALUES (?, ?, ?, ?)
            """, (alu_id, mat_id, parcial, self.calificacion.value()))
        else:
            cursor.execute("""
                UPDATE calificaciones
                SET alumno_id = ?, materia_id = ?, parcial = ?, calificacion = ?
                WHERE id = ?
            """, (alu_id, mat_id, parcial, self.calificacion.value(), self.id_actual))

        conn.commit()
        conn.close()

        self.id_actual = None
        self.limpiar()
        self.cargar_tabla()
        self.tabs.setCurrentIndex(1)

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
            INNER JOIN alumnos a ON c.alumno_id = a.id
            INNER JOIN materias m ON c.materia_id = m.id
            ORDER BY c.id DESC
        """)

        datos = cursor.fetchall()
        conn.close()

        self.tabla.setRowCount(len(datos))

        for fila, dato in enumerate(datos):

            promedio = self.promedio_alumno(dato[4])

            self.tabla.setItem(fila, 0, QTableWidgetItem(str(dato[0])))
            self.tabla.setItem(fila, 1, QTableWidgetItem(dato[1]))
            self.tabla.setItem(fila, 2, QTableWidgetItem(dato[2]))
            self.tabla.setItem(fila, 3, QTableWidgetItem(str(dato[3])))
            self.tabla.setItem(fila, 4, QTableWidgetItem(str(promedio)))

            btn_edit = QPushButton("✏️")
            btn_del = QPushButton("🗑")

            btn_edit.setStyleSheet("background:#3B82F6; padding:5px; border-radius:5px;")
            btn_del.setStyleSheet("background:#EF4444; padding:5px; border-radius:5px;")

            btn_edit.clicked.connect(
                lambda _, idc=dato[0]: self.cargar_para_editar(idc)
            )

            btn_del.clicked.connect(
                lambda _, idc=dato[0]: self.eliminar(idc)
            )

            cont = QWidget()
            h = QHBoxLayout(cont)
            h.setContentsMargins(0, 0, 0, 0)
            h.setSpacing(5)

            h.addWidget(btn_edit)
            h.addWidget(btn_del)

            self.tabla.setCellWidget(fila, 5, cont)

    def cargar_para_editar(self, id_calificacion):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT alumno_id, materia_id, calificacion
            FROM calificaciones
            WHERE id = ?
        """, (id_calificacion,))

        dato = cursor.fetchone()
        conn.close()

        if not dato:
            return

        self.id_actual = id_calificacion

        self.cbAlumno.setCurrentIndex(
            self.cbAlumno.findData(dato[0])
        )

        self.cbMateria.setCurrentIndex(
            self.cbMateria.findData(dato[1])
        )

        self.calificacion.setValue(float(dato[2]))

        self.tabs.setCurrentIndex(0)

    def eliminar(self, id_calificacion):

        respuesta = QMessageBox.question(
            self,
            "Confirmar",
            "¿Eliminar esta calificación?",
            QMessageBox.Yes | QMessageBox.No
        )

        if respuesta == QMessageBox.Yes:
            conn = conectar()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM calificaciones WHERE id = ?",
                (id_calificacion,)
            )

            conn.commit()
            conn.close()

            self.cargar_tabla()

    def buscar_calificacion(self):

        texto = self.buscar.text()

        if not texto:
            self.cargar_tabla()
            return

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
            INNER JOIN alumnos a ON c.alumno_id = a.id
            INNER JOIN materias m ON c.materia_id = m.id
            WHERE a.nombre LIKE ?
            OR a.apellido LIKE ?
            OR m.nombre LIKE ?
        """, (
            f"%{texto}%",
            f"%{texto}%",
            f"%{texto}%"
        ))

        datos = cursor.fetchall()
        conn.close()

        self.tabla.setRowCount(len(datos))

        for fila, dato in enumerate(datos):

            promedio = self.promedio_alumno(dato[4])

            self.tabla.setItem(fila, 0, QTableWidgetItem(str(dato[0])))
            self.tabla.setItem(fila, 1, QTableWidgetItem(dato[1]))
            self.tabla.setItem(fila, 2, QTableWidgetItem(dato[2]))
            self.tabla.setItem(fila, 3, QTableWidgetItem(str(dato[3])))
            self.tabla.setItem(fila, 4, QTableWidgetItem(str(promedio)))

    def limpiar(self):

        self.calificacion.setValue(0)
        self.id_actual = None