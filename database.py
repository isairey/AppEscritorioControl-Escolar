import sqlite3
import os

# ==========================
# CARPETA DE DATOS EN APPDATA
# ==========================
DB_FOLDER = os.path.join(os.environ["APPDATA"], "TeacherDeskPro")
DB_NAME = os.path.join(DB_FOLDER, "escuela.db")


def conectar():
    os.makedirs(DB_FOLDER, exist_ok=True)
    return sqlite3.connect(DB_NAME)


def crear_bd():
    os.makedirs(DB_FOLDER, exist_ok=True)

    conn = conectar()
    cursor = conn.cursor()

    # =========================
    # USUARIOS
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE,
        password TEXT,
        rol TEXT
    )
    """)

    # =========================
    # ALUMNOS
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alumnos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        apellido TEXT,
        grado TEXT,
        grupo TEXT
    )
    """)

    # =========================
    # MATERIAS
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS materias(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT
    )
    """)

    # =========================
    # ASIGNACIÓN ALUMNO - MATERIA
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alumno_materia(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alumno_id INTEGER,
        materia_id INTEGER,
        UNIQUE(alumno_id, materia_id)
    )
    """)

    # =========================
    # CALIFICACIONES
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS calificaciones(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alumno_id INTEGER,
        materia_id INTEGER,
        parcial INTEGER,
        calificacion REAL,
        fecha TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =========================
    # ASISTENCIA
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS asistencia(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alumno_id INTEGER,
        materia_id INTEGER,
        fecha TEXT DEFAULT CURRENT_TIMESTAMP,
        estado TEXT
    )
    """)

    # =========================
    # USUARIO ADMIN POR DEFECTO
    # =========================
    cursor.execute("""
    INSERT OR IGNORE INTO usuarios
    (id, usuario, password, rol)
    VALUES
    (1,'admin','1234','Administrador')
    """)

    conn.commit()
    conn.close()