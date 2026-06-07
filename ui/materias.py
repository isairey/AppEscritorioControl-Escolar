from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from database import conectar


class MateriasWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.id_actual = None
        self.materia_seleccionada = None

        # =========================
        # CONTENEDOR GENERAL
        # =========================
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(18)

        # =========================
        # HEADER PRO
        # =========================
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                stop:0 #1E293B, stop:1 #0F172A);
                border-radius: 18px;
                padding: 18px;
            }
        """)

        h = QVBoxLayout()

        titulo = QLabel("📚 Gestión de Materias Pro")
        titulo.setStyleSheet("""
            font-size:32px;
            font-weight:bold;
            color:white;
        """)

        subtitulo = QLabel("Administra materias y alumnos inscritos")
        subtitulo.setStyleSheet("""
            color:#94A3B8;
            font-size:14px;
        """)

        h.addWidget(titulo)
        h.addWidget(subtitulo)

        header.setLayout(h)
        layout.addWidget(header)

        # =========================
        # TABS
        # =========================
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane{
                border:none;
            }

            QTabBar::tab{
                background:#111827;
                color:#94A3B8;
                padding:12px;
                border-radius:10px;
                margin-right:6px;
            }

            QTabBar::tab:selected{
                background:#2563EB;
                color:white;
            }
        """)

        self.tabRegistro = QWidget()
        self.tabAsignar = QWidget()
        self.tabMaterias = QWidget()
        self.tabDetalle = QWidget()

        self.tabs.addTab(self.tabRegistro, "➕ Registrar")
        self.tabs.addTab(self.tabAsignar, "🎯 Asignar")
        self.tabs.addTab(self.tabMaterias, "📚 Materias CRUD")
        self.tabs.addTab(self.tabDetalle, "👨‍🎓 Detalle")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

        # UI
        self.ui_registro()
        self.ui_asignar()
        self.ui_materias()
        self.ui_detalle()

        self.cargar_materias()
        self.cargar_combos()

    # =========================
    # ESTILO TABLAS PRO
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

        # 🔥 filas más grandes (BOTONES YA NO SE APACHURRAN)
        table.verticalHeader().setDefaultSectionSize(48)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    # =========================
    # REGISTRO
    # =========================
    def ui_registro(self):

        layout = QVBoxLayout()

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background:#0B1220;
                border-radius:16px;
                padding:20px;
            }
        """)

        v = QVBoxLayout()

        self.nombre = QLineEdit()
        self.nombre.setPlaceholderText("Nombre de la materia")

        self.nombre.setStyleSheet("""
            QLineEdit {
                background:#111827;
                color:white;
                padding:12px;
                border-radius:10px;
                border:1px solid #1F2937;
            }
        """)

        self.btnGuardar = QPushButton("💾 Guardar Materia")
        self.btnGuardar.setStyleSheet("""
            QPushButton {
                background:#16A34A;
                color:white;
                padding:12px;
                border-radius:10px;
                font-weight:bold;
            }

            QPushButton:hover {
                background:#15803D;
            }
        """)

        self.btnGuardar.clicked.connect(self.guardar)

        v.addWidget(self.nombre)
        v.addWidget(self.btnGuardar)

        card.setLayout(v)

        layout.addWidget(card)
        layout.addStretch()

        self.tabRegistro.setLayout(layout)

    # =========================
    # ASIGNAR
    # =========================
    def ui_asignar(self):

        layout = QVBoxLayout()

        self.comboAlumno = QComboBox()
        self.comboMateria = QComboBox()

        for w in [self.comboAlumno, self.comboMateria]:
            w.setStyleSheet("""
                QComboBox {
                    background:#111827;
                    color:white;
                    padding:10px;
                    border-radius:10px;
                }
            """)

        self.btnAsignar = QPushButton("🎯 Asignar Materia")
        self.btnAsignar.setStyleSheet("""
            QPushButton {
                background:#2563EB;
                color:white;
                padding:12px;
                border-radius:10px;
                font-weight:bold;
            }
            QPushButton:hover {
                background:#1D4ED8;
            }
        """)

        self.btnAsignar.clicked.connect(self.asignar)

        layout.addWidget(QLabel("Alumno"))
        layout.addWidget(self.comboAlumno)
        layout.addWidget(QLabel("Materia"))
        layout.addWidget(self.comboMateria)
        layout.addWidget(self.btnAsignar)

        layout.addStretch()
        self.tabAsignar.setLayout(layout)

    # =========================
    # CRUD MATERIAS
    # =========================
    def ui_materias(self):

        layout = QVBoxLayout()

        self.tablaMaterias = QTableWidget()
        self.tablaMaterias.setColumnCount(3)
        self.tablaMaterias.setHorizontalHeaderLabels(["ID", "Materia", "Acciones"])

        self.estilo_tabla(self.tablaMaterias)

        layout.addWidget(self.tablaMaterias)
        self.tabMaterias.setLayout(layout)

    # =========================
    # DETALLE MATERIA
    # =========================
    def ui_detalle(self):

        layout = QVBoxLayout()

        self.lblMateria = QLabel("Selecciona una materia")
        self.lblMateria.setStyleSheet("""
            color:white;
            font-size:16px;
            font-weight:bold;
        """)

        self.tablaAlumnos = QTableWidget()
        self.tablaAlumnos.setColumnCount(2)
        self.tablaAlumnos.setHorizontalHeaderLabels(["Alumno", "Acción"])

        self.estilo_tabla(self.tablaAlumnos)

        layout.addWidget(self.lblMateria)
        layout.addWidget(self.tablaAlumnos)

        self.tabDetalle.setLayout(layout)

    # =========================
    # GUARDAR
    # =========================
    def guardar(self):

        conn = conectar()
        cursor = conn.cursor()

        if self.id_actual is None:
            cursor.execute("INSERT INTO materias(nombre) VALUES(?)",
                           (self.nombre.text(),))
        else:
            cursor.execute("UPDATE materias SET nombre=? WHERE id=?",
                           (self.nombre.text(), self.id_actual))

        conn.commit()
        conn.close()

        self.nombre.clear()
        self.id_actual = None

        self.cargar_materias()
        self.cargar_combos()

    # =========================
    # MATERIAS CRUD
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
            h.setSpacing(6)

            btnE = QPushButton("✏️")
            btnD = QPushButton("🗑")

            btnE.setStyleSheet("background:#2563EB;")
            btnD.setStyleSheet("background:#DC2626;")

            btnE.clicked.connect(lambda _, x=m: self.editar(x))
            btnD.clicked.connect(lambda _, id=m[0]: self.eliminar(id))

            h.addWidget(btnE)
            h.addWidget(btnD)

            cont.setLayout(h)
            self.tablaMaterias.setCellWidget(i, 2, cont)

    # =========================
    # EDITAR
    # =========================
    def editar(self, m):
        self.id_actual = m[0]
        self.nombre.setText(m[1])
        self.tabs.setCurrentIndex(0)

    # =========================
    # ELIMINAR
    # =========================
    def eliminar(self, id):

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM materias WHERE id=?", (id,))
        conn.commit()
        conn.close()

        self.cargar_materias()

    # =========================
    # ASIGNAR
    # =========================
    def asignar(self):

        alumno_id = self.comboAlumno.currentData()
        materia_id = self.comboMateria.currentData()

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR IGNORE INTO alumno_materia(alumno_id, materia_id)
            VALUES (?, ?)
        """, (alumno_id, materia_id))

        conn.commit()
        conn.close()

    # =========================
    # DETALLE
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
            btn.setStyleSheet("background:#DC2626;")

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
    # COMBOS
    # =========================
    def cargar_combos(self):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT id, nombre FROM alumnos")
        alumnos = cursor.fetchall()

        cursor.execute("SELECT id, nombre FROM materias")
        materias = cursor.fetchall()

        conn.close()

        self.comboAlumno.clear()
        self.comboMateria.clear()

        for a in alumnos:
            self.comboAlumno.addItem(a[1], a[0])

        for m in materias:
            self.comboMateria.addItem(m[1], m[0])