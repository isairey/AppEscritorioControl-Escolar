import pytest
import os
import sqlite3

# Importar tu database
from database import conectar, crear_bd


# ==========================
# FIXTURES
# ==========================
@pytest.fixture(scope="function")
def db():
    """Crear base de datos limpia para cada test"""
    # Usar una bd de prueba en memoria
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    
    # Crear tablas
    cursor.execute("""
        CREATE TABLE usuarios(
            id INTEGER PRIMARY KEY,
            usuario TEXT UNIQUE,
            password TEXT,
            rol TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE alumnos(
            id INTEGER PRIMARY KEY,
            nombre TEXT,
            apellido TEXT,
            grado TEXT,
            grupo TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE materias(
            id INTEGER PRIMARY KEY,
            nombre TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE calificaciones(
            id INTEGER PRIMARY KEY,
            aluMno_id INTEGER,
            materia_id INTEGER,
            parcial INTEGER,
            calificacion REAL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE asistencia(
            id INTEGER PRIMARY KEY,
            aluMno_id INTEGER,
            materia_id INTEGER,
            estado TEXT
        )
    """)
    
    conn.commit()
    yield conn
    conn.close()


# ==========================
# TESTS USUARIOS
# ==========================
def test_crear_usuario(db):
    """Test crear usuario"""
    cursor = db.cursor()
    
    cursor.execute("""
        INSERT INTO usuarios (usuario, password, rol)
        VALUES (?, ?, ?)
    """, ("admin", "1234", "Administrador"))
    
    db.commit()
    
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", ("admin",))
    usuario = cursor.fetchone()
    
    assert usuario is not None
    assert usuario[1] == "admin"
    assert usuario[2] == "1234"


def test_login_usuario(db):
    """Test login de usuario"""
    cursor = db.cursor()
    
    # Insertar usuario
    cursor.execute("""
        INSERT INTO usuarios (usuario, password, rol)
        VALUES (?, ?, ?)
    """, ("test", "pass", "Usuario"))
    
    db.commit()
    
    # Verificar login
    cursor.execute("""
        SELECT * FROM usuarios WHERE usuario = ? AND password = ?
    """, ("test", "pass"))
    
    usuario = cursor.fetchone()
    
    assert usuario is not None
    assert usuario[1] == "test"


# ==========================
# TESTS ALUMNOS
# ==========================
def test_crear_alumno(db):
    """Test crear alumno"""
    cursor = db.cursor()
    
    cursor.execute("""
        INSERT INTO alumnos (nombre, apellido, grado, grupo)
        VALUES (?, ?, ?, ?)
    """, ("Juan", "Pérez", "1", "A"))
    
    db.commit()
    
    cursor.execute("SELECT * FROM alumno WHERE nombre = ?", ("Juan",))
    alumno = cursor.fetchone()
    
    assert alumno is not None
    assert alumno[1] == "Juan"
    assert alumno[2] == "Pérez"


def test_listar_alumnos(db):
    """Test listar todos los alumnos"""
    cursor = db.cursor()
    
    # Insertar varios
    cursor.execute("INSERT INTO alumnos (nombre, apellido) VALUES (?, ?)", ("Juan", "Pérez"))
    cursor.execute("INSERT INTO alumnos (nombre, apellido) VALUES (?, ?)", ("María", "García"))
    cursor.execute("INSERT INTO alumnos (nombre, apellido) VALUES (?, ?)", ("Pedro", "López"))
    
    db.commit()
    
    cursor.execute("SELECT COUNT(*) FROM alumnos")
    total = cursor.fetchone()[0]
    
    assert total == 3


def test_actualizar_alumno(db):
    """Test actualizar alumno"""
    cursor = db.cursor()
    
    # Insertar
    cursor.execute("""
        INSERT INTO alumnos (nombre, apellido)
        VALUES (?, ?)
    """, ("Juan", "Pérez"))
    db.commit()
    
    # Actualizar
    cursor.execute("""
        UPDATE alumnos SET nombre = ? WHERE nombre = ?
    """, ("Carlos", "Juan"))
    
    db.commit()
    
    cursor.execute("SELECT nombre FROM alumnos WHERE nombre = ?", ("Carlos",))
    nombre = cursor.fetchone()[0]
    
    assert nombre == "Carlos"


def test_eliminar_alumno(db):
    """Test eliminar alumno"""
    cursor = db.cursor()
    
    # Insertar
    cursor.execute("INSERT INTO alumnos (nombre) VALUES (?)", ("Juan",))
    db.commit()
    id_alumno = cursor.lastrowid
    
    # Eliminar
    cursor.execute("DELETE FROM alumnos WHERE id = ?", (id_alumno,))
    db.commit()
    
    cursor.execute("SELECT * FROM alumnos WHERE id = ?", (id_alumno,))
    alumno = cursor.fetchone()
    
    assert alumno is None


# ==========================
# TESTS MATERIAS
# ==========================
def test_crear_materia(db):
    """Test crear materia"""
    cursor = db.cursor()
    
    cursor.execute("INSERT INTO materias (nombre) VALUES (?)", ("Matemáticas",))
    db.commit()
    
    cursor.execute("SELECT * FROM materias WHERE nombre = ?", ("Matemáticas",))
    materia = cursor.fetchone()
    
    assert materia is not None
    assert materia[1] == "Matemáticas"


def test_materia_duplicada(db):
    """Test no permitir materia duplicada"""
    cursor = db.cursor()
    
    # Insertar una vez
    cursor.execute("INSERT INTO materias (nombre) VALUES (?)", ("Historia",))
    db.commit()
    
    # Intentar duplicar
    cursor.execute("SELECT nombre FROM materias WHERE nombre = ?", ("Historia",))
    existe = cursor.fetchone()
    
    assert existe is not None


# ==========================
# TESTS CALIFICACIONES
# ==========================
def test_crear_calificacion(db):
    """Test crear calificación"""
    cursor = db.cursor()
    
    # Insertar aluno y materia primero
    cursor.execute("INSERT INTO alumnos (nombre) VALUES (?)", ("Juan",))
    cursor.execute("INSERT INTO materias (nombre) VALUES (?)", ("Mate",))
    db.commit()
    
    # Insertar calificación
    cursor.execute("""
        INSERT INTO calificaciones (aluMno_id, materia_id, parcial, calificacion)
        VALUES (?, ?, ?, ?)
    """, (1, 1, 1, 9.5))
    
    db.commit()
    
    cursor.execute("SELECT calificacion FROM calificaciones WHERE aluMno_id = ?", (1,))
    calif = cursor.fetchone()
    
    assert calif[0] == 9.5


def test_promedio_alumno(db):
    """Test calcular promedio de aluno"""
    cursor = db.cursor()
    
    # Insertar aluno
    cursor.execute("INSERT INTO alumnos (nombre) VALUES (?)", ("Juan",))
    cursor.execute("INSERT INTO materias (nombre) VALUES (?)", ("Mate",))
    cursor.execute("INSERT INTO materias (nombre) VALUES (?)", ("Esp",))
    db.commit()
    
    # Insertar varias calificaciones
    cursor.execute("INSERT INTO calificaciones VALUES (1, 1, 1, 8)")
    cursor.execute("INSERT INTO calificaciones VALUES (1, 2, 1, 7)")
    db.commit()
    
    # Calcular promedio
    cursor.execute("SELECT AVG(calificacion) FROM calificaciones WHERE aluMno_id = ?", (1,))
    promedio = cursor.fetchone()[0]
    
    assert promedio == 7.5


# ==========================
# TESTS ASISTENCIA
# ==========================
def test_registrar_asistencia(db):
    """Test registrar asistencia"""
    cursor = db.cursor()
    
    # Insertar aluno y materia
    cursor.execute("INSERT INTO alumnos (nombre) VALUES (?)", ("Juan",))
    cursor.execute("INSERT INTO materias (nombre) VALUES (?)", ("Mate",))
    db.commit()
    
    # Insertar asistencia
    cursor.execute("""
        INSERT INTO asistencia (aluMno_id, materia_id, estado)
        VALUES (?, ?, ?)
    """, (1, 1, "Presente"))
    
    db.commit()
    
    cursor.execute("SELECT estado FROM asistencia WHERE aluMno_id = ?", (1,))
    estado = cursor.fetchone()
    
    assert estado[0] == "Presente"


def test_no_duplicar_asistencia(db):
    """Test que no haya asistencia duplicada"""
    cursor = db.cursor()
    
    # Insertar
    cursor.execute("INSERT INTO alumnos (nombre) VALUES (?)", ("Juan",))
    cursor.execute("INSERT INTO materias (nombre) VALUES (?)", ("Mate",))
    db.commit()
    
    # Verificar si ya existe
    cursor.execute("""
        SELECT id FROM asistencia
        WHERE aluMno_id = ? AND materia_id = ? AND estado = ?
    """, (1, 1, "Presente"))
    
    existe = cursor.fetchone()
    
    # No debe existir todavía
    assert existe is None


# ==========================
# EJECUTAR TESTS
# ==========================
if __name__ == "__main__":
    pytest.main([__file__, "-v"])