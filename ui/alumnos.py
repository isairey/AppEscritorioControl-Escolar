from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from database import conectar


class AlumnosWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.id_actual = None

        # =========================
        # LAYOUT GENERAL
        # =========================

        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(18)

        # =========================
        # HEADER
        # =========================

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

        titulo = QLabel("👨‍🎓 Gestión de Alumnos")
        titulo.setStyleSheet("font-size:30px;font-weight:bold;color:white;")

        subtitulo = QLabel("Sistema escolar profesional")
        subtitulo.setStyleSheet("color:#94A3B8;font-size:14px;")

        h.addWidget(titulo)
        h.addWidget(subtitulo)

        header.setLayout(h)
        layout.addWidget(header)

        # =========================
        # TABS
        # =========================

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

        self.tabs.addTab(self.tabRegistro, "➕ Registro")
        self.tabs.addTab(self.tabLista, "📋 Lista")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

        # UI
        self.ui_registro()
        self.ui_lista()

        self.cargar_tabla()

    # =========================================================
    # REGISTRO
    # =========================================================

    def ui_registro(self):

        layout = QVBoxLayout()

        card = QFrame()
        card.setStyleSheet("""
            QFrame{
                background:#0B1220;
                border-radius:15px;
                padding:20px;
            }
        """)

        form = QGridLayout()

        self.nombre = QLineEdit()
        self.apellido = QLineEdit()
        self.grado = QLineEdit()
        self.grupo = QLineEdit()

        for w in [self.nombre, self.apellido, self.grado, self.grupo]:
            w.setStyleSheet("""
                QLineEdit{
                    background:#111827;
                    border:1px solid #1F2937;
                    border-radius:10px;
                    padding:10px;
                    color:white;
                }
                QLineEdit:focus{
                    border:1px solid #3B82F6;
                }
            """)

        self.nombre.setPlaceholderText("Nombre")
        self.apellido.setPlaceholderText("Apellido")
        self.grado.setPlaceholderText("Grado")
        self.grupo.setPlaceholderText("Grupo")

        form.addWidget(QLabel("Nombre"), 0, 0)
        form.addWidget(self.nombre, 1, 0)

        form.addWidget(QLabel("Apellido"), 0, 1)
        form.addWidget(self.apellido, 1, 1)

        form.addWidget(QLabel("Grado"), 2, 0)
        form.addWidget(self.grado, 3, 0)

        form.addWidget(QLabel("Grupo"), 2, 1)
        form.addWidget(self.grupo, 3, 1)

        self.btnGuardar = QPushButton("💾 Guardar")
        self.btnGuardar.setStyleSheet("""
            QPushButton{
                background:#16A34A;
                color:white;
                padding:12px;
                border-radius:10px;
                font-weight:bold;
            }
            QPushButton:hover{
                background:#15803D;
            }
        """)

        self.btnGuardar.clicked.connect(self.guardar_alumno)

        form.addWidget(self.btnGuardar, 4, 0, 1, 2)

        card.setLayout(form)
        layout.addWidget(card)
        layout.addStretch()

        self.tabRegistro.setLayout(layout)

    # =========================================================
    # TABLA PRO
    # =========================================================

    def ui_lista(self):

        layout = QVBoxLayout()
        layout.setSpacing(10)

        # BUSCADOR
        self.buscar = QLineEdit()
        self.buscar.setPlaceholderText("🔍 Buscar alumno...")

        self.buscar.setFixedHeight(40)

        self.buscar.setStyleSheet("""
            QLineEdit{
                background:#0B1220;
                border:1px solid #1F2937;
                border-radius:10px;
                padding-left:10px;
                color:white;
            }
        """)

        self.buscar.textChanged.connect(self.buscar_alumno)

        layout.addWidget(self.buscar)

        # TABLA
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)

        self.tabla.setHorizontalHeaderLabels([
            "ID", "Nombre", "Apellido", "Grado", "Grupo", "Acciones"
        ])

        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.tabla.verticalHeader().setVisible(False)

        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)

        self.tabla.setStyleSheet("""
            QTableWidget{
                background:#0B1220;
                border:none;
                border-radius:12px;
                color:white;
                gridline-color:#1F2937;
            }

            QHeaderView::section{
                background:#111827;
                color:#94A3B8;
                padding:8px;
                border:none;
                font-weight:bold;
            }
        """)

        layout.addWidget(self.tabla)

        self.tabLista.setLayout(layout)

    # =========================================================
    # GUARDAR (CREAR / EDITAR)
    # =========================================================

    def guardar_alumno(self):

        conn = conectar()
        cursor = conn.cursor()

        if self.id_actual is None:

            cursor.execute("""
                INSERT INTO alumnos(nombre, apellido, grado, grupo)
                VALUES (?, ?, ?, ?)
            """, (
                self.nombre.text(),
                self.apellido.text(),
                self.grado.text(),
                self.grupo.text()
            ))

        else:

            cursor.execute("""
                UPDATE alumnos
                SET nombre=?, apellido=?, grado=?, grupo=?
                WHERE id=?
            """, (
                self.nombre.text(),
                self.apellido.text(),
                self.grado.text(),
                self.grupo.text(),
                self.id_actual
            ))

        conn.commit()
        conn.close()

        self.limpiar()
        self.cargar_tabla()
        self.id_actual = None
        self.tabs.setCurrentIndex(1)  # ir a la pestaña de lista

    # =========================================================
    # CARGAR TABLA
    # =========================================================

    def cargar_tabla(self):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM alumnos")
        datos = cursor.fetchall()
        conn.close()

        self.tabla.setRowCount(len(datos))

        for fila, alumno in enumerate(datos):

            for col in range(5):
                self.tabla.setItem(
                    fila,
                    col,
                    QTableWidgetItem(str(alumno[col]))
                )

            # BOTONES
            btn_edit = QPushButton("✏️")
            btn_del = QPushButton("🗑")

            btn_edit.setStyleSheet("background:#2563EB;color:white;border-radius:6px;")
            btn_del.setStyleSheet("background:#DC2626;color:white;border-radius:6px;")

            btn_edit.clicked.connect(lambda _, a=alumno: self.cargar_para_editar(a))
            btn_del.clicked.connect(lambda _, id=alumno[0]: self.eliminar(id))

            cont = QWidget()
            h = QHBoxLayout()
            h.setContentsMargins(0, 0, 0, 0)
            h.setSpacing(5)

            h.addWidget(btn_edit)
            h.addWidget(btn_del)

            cont.setLayout(h)

            self.tabla.setCellWidget(fila, 5, cont)

    # =========================================================
    # EDITAR (NO DUPLICA)
    # =========================================================

    def cargar_para_editar(self, alumno):

        self.id_actual = alumno[0]

        self.nombre.setText(alumno[1])
        self.apellido.setText(alumno[2])
        self.grado.setText(alumno[3])
        self.grupo.setText(alumno[4])

        self.tabs.setCurrentIndex(0)

    # =========================================================
    # ELIMINAR
    # =========================================================

    def eliminar(self, id_alumno):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM alumnos WHERE id=?", (id_alumno,))

        conn.commit()
        conn.close()

        self.cargar_tabla()

    # =========================================================
    # BUSCAR
    # =========================================================

    def buscar_alumno(self):

        texto = self.buscar.text()

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM alumnos
            WHERE nombre LIKE ? OR apellido LIKE ?
        """, (f"%{texto}%", f"%{texto}%"))

        datos = cursor.fetchall()
        conn.close()

        self.tabla.setRowCount(len(datos))

        for fila, alumno in enumerate(datos):
            for col in range(5):
                self.tabla.setItem(
                    fila,
                    col,
                    QTableWidgetItem(str(alumno[col]))
                )

    # =========================================================
    # LIMPIAR
    # =========================================================

    def limpiar(self):
        self.nombre.clear()
        self.apellido.clear()
        self.grado.clear()
        self.grupo.clear()