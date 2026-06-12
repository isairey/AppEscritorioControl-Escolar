from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from database import conectar


class MateriasWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.id_actual = None
        self.materia_seleccionada = None

        # Estilo global
        self.setStyleSheet("""
            QWidget {
                background-color: #0B0F1A;
                color: #E2E8F0;
                font-family: 'Segoe UI', 'Inter', sans-serif;
            }
            QLabel {
                color: #CBD5E1;
                background: transparent;
            }
            QLineEdit, QComboBox {
                background-color: #1E293B;
                border: 2px solid #334155;
                border-radius: 10px;
                padding: 12px 16px;
                color: white;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #3B82F6;
            }
            QLineEdit::placeholder { color: #64748B; }
            QPushButton {
                border: none;
                border-radius: 10px;
                padding: 12px 24px;
                font-weight: 600;
                font-size: 14px;
            }
            QTabBar::tab {
                background: transparent;
                color: #64748B;
                padding: 12px 20px;
                border: none;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                color: #3B82F6;
                background: rgba(59, 130, 246, 0.1);
                border-radius: 8px;
            }
            QTabBar::tab:hover:!selected {
                color: #94A3B8;
                background: rgba(148, 163, 184, 0.1);
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(24)

        # HEADER COLOR SOLIDO
        header = QFrame()
        header.setObjectName("header")
        header.setFixedHeight(120)
        header.setStyleSheet("""
            QFrame#header {
                background-color: #1E293B;
                border-radius: 20px;
                border-radius:15px;
                padding:18px;
            }
        """)

        h = QHBoxLayout()
        h.setContentsMargins(30, 0, 30, 0)
        h.setSpacing(20)

        # Icono grande
        icon_label = QLabel("")
        icon_label.setStyleSheet("font-size: 48px; background: transparent;")

        # Textos
        text_col = QVBoxLayout()
        text_col.setSpacing(4)

        titulo = QLabel("Gestión de Materias")
        titulo.setStyleSheet("""
            font-size: 28px; 
            font-weight: 700; 
            color: #F8FAFC; 
            letter-spacing: -0.5px;
            background: transparent;
        """)

        subtitulo = QLabel("Administra tus materias, asigna alumnos y controla inscripciones")
        subtitulo.setStyleSheet("""
            font-size: 13px; 
            color: #64748B;
            background: transparent;
        """)

        text_col.addWidget(titulo)
        text_col.addWidget(subtitulo)

        h.addWidget(icon_label)
        h.addLayout(text_col)
        h.addStretch()

        header.setLayout(h)
        layout.addWidget(header)

        # TABS ESTILIZADOS
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        self.tabRegistro = QWidget()
        self.tabAsignar = QWidget()
        self.tabMaterias = QWidget()
        self.tabDetalle = QWidget()

        self.tabs.addTab(self.tabRegistro, " Registrar")
        self.tabs.addTab(self.tabAsignar, " Asignar")
        self.tabs.addTab(self.tabMaterias, " Materias")
        self.tabs.addTab(self.tabDetalle, " Detalle")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self.ui_registro()
        self.ui_asignar()
        self.ui_materias()
        self.ui_detalle()

        self.cargar_materias()
        self.cargar_combos()

    # =========================
    # TABLA ESTILO PRO
    # =========================
    def estilo_tabla(self, table):
        table.setStyleSheet("""
            QTableWidget {
                background:#0B1220;
                color:white;
                border:none;
                gridline-color:#1F2937;
                font-size:14px;
            }

            QHeaderView::section {
                background:#111827;
                color:#94A3B8;
                padding:10px;
                border:none;
                font-weight:bold;
            }

            QTableWidget::item {
                padding:10px;
            }

            QPushButton {
                padding:6px;
                border-radius:8px;
                color:white;
                font-weight:bold;
            }
        """)

        table.verticalHeader().setVisible(False)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.verticalHeader().setDefaultSectionSize(48)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    # =========================
    # REGISTRO
       # =========================
    def ui_registro(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        self.nombre = QLineEdit()
        self.nombre.setPlaceholderText("Nombre de la materia")
        self.nombre.setFixedHeight(45)
        self.nombre.setStyleSheet("""
            QLineEdit {
                background-color: #1E293B;
                border: 2px solid #334155;
                border-radius: 10px;
                padding: 12px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3B82F6;
            }
            QLineEdit::placeholder {
                color: #64748B;
            }
        """)

        self.btnGuardar = QPushButton(" Guardar Materia")
        self.btnGuardar.setFixedHeight(45)
        self.btnGuardar.setCursor(Qt.PointingHandCursor)
        self.btnGuardar.setStyleSheet("""
            QPushButton {
                background-color: #22C55E;
                border: none;
                border-radius: 10px;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #16A34A;
            }
            QPushButton:pressed {
                background-color: #15803D;
            }
        """)

        self.mensaje = QLabel("")
        self.mensaje.setAlignment(Qt.AlignCenter)
        self.mensaje.setStyleSheet("font-size: 12px;")

        layout.addWidget(self.nombre)
        layout.addWidget(self.btnGuardar)
        layout.addWidget(self.mensaje)
        layout.addStretch()

        self.tabRegistro.setLayout(layout)

        # =========================
        # EVENTO
        # =========================
        self.btnGuardar.clicked.connect(self.guardar)
        self.nombre.returnPressed.connect(self.guardar)

    # =========================
    # ASIGNAR
    # =========================
    def ui_asignar(self):
        layout = QVBoxLayout()

        card = QFrame()
        card.setStyleSheet("background:#0B1220;border-radius:15px;padding:25px;")

        form = QGridLayout()
        form.setSpacing(15)

        self.comboAlumno = QComboBox()
        self.comboMateria = QComboBox()

        for w in [self.comboAlumno, self.comboMateria]:
            w.setStyleSheet("""
                QComboBox {
                    background-color: #111827;
                    border: 1px solid #1F2937;
                    border-radius: 10px;
                    padding: 12px;
                    color: white;
                }
                QComboBox:hover {
                    border-color: #3B82F6;
                }
                QComboBox::drop-down {
                    border: none;
                    width: 30px;
                }
            """)

        form.addWidget(QLabel("Alumno"), 0, 0)
        form.addWidget(self.comboAlumno, 1, 0)

        form.addWidget(QLabel("Materia"), 0, 1)
        form.addWidget(self.comboMateria, 1, 1)

        self.btnAsignar = QPushButton(" Asignar Alumno a Materia")
        self.btnAsignar.clicked.connect(self.asignar)

        self.btnAsignar.setStyleSheet("""
            QPushButton {
                background-color: #16A34A;
                color: white;
                padding: 14px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #15803D;
            }
        """)

        form.addWidget(self.btnAsignar, 2, 0, 1, 2)

        card.setLayout(form)
        layout.addWidget(card)
        layout.addStretch()

        self.tabAsignar.setLayout(layout)

    # =========================
    # MATERIAS CRUD
    # =========================
    def ui_materias(self):
        layout = QVBoxLayout()

        self.tablaMaterias = QTableWidget()
        self.tablaMaterias.setColumnCount(3)
        self.tablaMaterias.setHorizontalHeaderLabels(["ID", "Materia", "Acciones"])

        self.tablaMaterias.cellClicked.connect(self.ver_alumnos)

        self.estilo_tabla(self.tablaMaterias)

        layout.addWidget(self.tablaMaterias)
        self.tabMaterias.setLayout(layout)

    # =========================
    # DETALLE
    # =========================
    def ui_detalle(self):
        layout = QVBoxLayout()

        self.lblMateria = QLabel("Selecciona una materia")
        self.lblMateria.setStyleSheet("color:white;font-size:16px;font-weight:bold;")

        self.tablaAlumnos = QTableWidget()
        self.tablaAlumnos.setColumnCount(2)
        self.tablaAlumnos.setHorizontalHeaderLabels(["Alumno", "Acción"])

        self.estilo_tabla(self.tablaAlumnos)

        layout.addWidget(self.lblMateria)
        layout.addWidget(self.tablaAlumnos)

        self.tabDetalle.setLayout(layout)

    # =========================
    # GUARDAR
    def guardar(self):
        nombre = self.nombre.text().strip()

        # VALIDACIÓN: Nombre vacío
        if not nombre:
            self.mensaje.setText("Ingresa el nombre de la materia")
            self.mensaje.setStyleSheet("color: #EF4444; font-size: 12px;")
            return

        conn = conectar()
        cursor = conn.cursor()

        # VALIDACIÓN: Verificar duplicado
        cursor.execute("SELECT id FROM materias WHERE nombre = ?", (nombre,))
        existe = cursor.fetchone()

        if existe and self.id_actual != existe[0]:
            self.mensaje.setText("Esta materia ya existe")
            self.mensaje.setStyleSheet("color: #EF4444; font-size: 12px;")
            conn.close()
            return

        # INSERTAR O ACTUALIZAR
        if self.id_actual is None:
            cursor.execute("INSERT INTO materias(nombre) VALUES(?)", (nombre,))
        else:
            cursor.execute("UPDATE materias SET nombre=? WHERE id=?", 
                           (nombre, self.id_actual))

        conn.commit()
        conn.close()

        # LIMPIAR
        self.nombre.clear()
        self.id_actual = None
        self.mensaje.clear()

        # CARGAR
        self.cargar_materias()
        self.cargar_combos()
        self.tabs.setCurrentIndex(2)

    # =========================
    # MATERIAS
    # =========================
    def cargar_materias(self):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM materias")
        datos = cursor.fetchall()
        conn.close()

        self.tablaMaterias.setRowCount(len(datos))

        for i, m in enumerate(datos):

            self.tablaMaterias.setItem(i, 0, QTableWidgetItem(str(m[0])))
            self.tablaMaterias.setItem(i, 1, QTableWidgetItem(m[1]))

            cont = QWidget()
            h = QHBoxLayout()
            h.setContentsMargins(0, 0, 0, 0)

            btnE = QPushButton("✏️")
            btnD = QPushButton("🗑")

            btnE.clicked.connect(lambda _, x=m: self.editar(x))
            btnD.clicked.connect(lambda _, id=m[0]: self.eliminar(id))

            h.addWidget(btnE)
            h.addWidget(btnD)

            cont.setLayout(h)
            self.tablaMaterias.setCellWidget(i, 2, cont)

    # =========================
    # CLICK MATERIA → ALUMNOS
    # =========================
    def ver_alumnos(self, row, col):

        self.materia_seleccionada = int(self.tablaMaterias.item(row, 0).text())
        nombre = self.tablaMaterias.item(row, 1).text()

        self.lblMateria.setText(f"📘 {nombre}")

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT a.nombre, am.id
            FROM alumno_materia am
            JOIN alumnos a ON a.id = am.alumno_id
            WHERE am.materia_id=?
        """, (self.materia_seleccionada,))

        datos = cursor.fetchall()
        conn.close()

        self.tablaAlumnos.setRowCount(len(datos))

        for i, r in enumerate(datos):
            self.tablaAlumnos.setItem(i, 0, QTableWidgetItem(r[0]))

            btn = QPushButton("🗑")
            btn.clicked.connect(lambda _, x=r[1]: self.eliminar_inscripcion(x))

            self.tablaAlumnos.setCellWidget(i, 1, btn)

        self.tabs.setCurrentIndex(3)

    # =========================
    # ELIMINAR INSCRIPCIÓN
    # =========================
    def eliminar_inscripcion(self, id_asig):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM alumno_materia WHERE id=?", (id_asig,))

        conn.commit()
        conn.close()

        if self.materia_seleccionada:
            self.ver_alumnos(self.materia_seleccionada, self.lblMateria.text())

    # =========================
    # ELIMINAR MATERIA
    # =========================
    def eliminar(self, id):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM materias WHERE id=?", (id,))
        conn.commit()
        conn.close()
        self.cargar_materias()

    # =========================
    # EDITAR
    # =========================
    def editar(self, m):
        self.id_actual = m[0]
        self.nombre.setText(m[1])
        self.tabs.setCurrentIndex(0)

    # =========================
    # ASIGNAR
    # =========================
    def asignar(self):
        # VALIDACIONES
        if self.comboAlumno.count() == 0:
            QMessageBox.warning(self, "Aviso", "No hay alumnos.")
            return

        if self.comboMateria.count() == 0:
            QMessageBox.warning(self, "Aviso", "No hay materias.")
            return

        alu_id = self.comboAlumno.currentData()
        mat_id = self.comboMateria.currentData()

        if alu_id is None or mat_id is None:
            QMessageBox.warning(self, "Aviso", "Selecciona alumno y materia.")
            return

        conn = conectar()
        cursor = conn.cursor()

        # VERIFICAR DUPLICADO
        cursor.execute("""
            SELECT id FROM alumno_materia
            WHERE alumno_id = ? AND materia_id = ?
        """, (alu_id, mat_id))

        if cursor.fetchone():
            QMessageBox.warning(
                self,
                "Duplicado",
                "Este alumno ya está asignado a esta materia."
            )
            conn.close()
            return

        # INSERTAR
        cursor.execute("""
            INSERT INTO alumno_materia (alumno_id, materia_id)
            VALUES (?, ?)
        """, (alu_id, mat_id))

        conn.commit()
        conn.close()

        QMessageBox.information(
            self,
            "Éxito",
            "Alumno asignado a la materia correctamente."
        )

        self.comboAlumno.setCurrentIndex(0)
        self.comboMateria.setCurrentIndex(0)
    # =========================
    # COMBOS
    def cargar_combos(self):
        conn = conectar()
        cursor = conn.cursor()

        # ALUMNOS - mostrar nombre completo
        cursor.execute("SELECT id, nombre, apellido FROM alumnos ORDER BY nombre")
        alumnos = cursor.fetchall()

        # MATERIAS
        cursor.execute("SELECT id, nombre FROM materias ORDER BY nombre")
        materias = cursor.fetchall()

        conn.close()

        self.comboAlumno.clear()
        self.comboMateria.clear()

        # Nombre completo
        for a in alumnos:
            self.comboAlumno.addItem(f"{a[1]} {a[2]}", a[0])

        for m in materias:
            self.comboMateria.addItem(m[1], m[0])