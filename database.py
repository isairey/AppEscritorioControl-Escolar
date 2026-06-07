import sqlite3
import os

DB_FOLDER = "data"
DB_NAME = os.path.join(DB_FOLDER, "escuela.db")


def conectar():
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
    # 🔥 ASIGNACIÓN ALUMNO - MATERIA (FALTABA)
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alumno_materia(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alumno_id INTEGER,
        materia_id INTEGER,
        FOREIGN KEY(alumno_id) REFERENCES alumnos(id),
        FOREIGN KEY(materia_id) REFERENCES materias(id)
    )
    """)

    # =========================
    # CALIFICACIONES (MEJORADA)
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS calificaciones(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alumno_id INTEGER,
        materia_id INTEGER,
        calificacion REAL,
        fecha TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(alumno_id) REFERENCES alumnos(id),
        FOREIGN KEY(materia_id) REFERENCES materias(id)
    )
    """)

    # =========================
    # ASISTENCIA (MEJORADA)
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS asistencia(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alumno_id INTEGER,
        materia_id INTEGER,
        fecha TEXT DEFAULT CURRENT_TIMESTAMP,
        estado TEXT,  -- presente / falta / retardo
        FOREIGN KEY(alumno_id) REFERENCES alumnos(id),
        FOREIGN KEY(materia_id) REFERENCES materias(id)
    )
    """)



    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alumno_materia(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alumno_id INTEGER,
    materia_id INTEGER,
    UNIQUE(alumno_id, materia_id)
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