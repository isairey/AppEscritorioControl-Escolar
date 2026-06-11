# 🎓 Sistema de Control Escolar

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge\&logo=python)
![PySide6](https://img.shields.io/badge/PySide6-GUI-green?style=for-the-badge)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue?style=for-the-badge)
![Desktop App](https://img.shields.io/badge/Desktop-Application-orange?style=for-the-badge)

### Sistema Integral de Gestión Escolar para Instituciones Educativas

Administra alumnos, materias, calificaciones y asistencias desde una interfaz moderna y fácil de usar.

</div>

---

# 📖 Descripción

El **Sistema de Control Escolar** es una aplicación de escritorio diseñada para facilitar la administración académica de instituciones educativas.

Permite registrar alumnos, gestionar materias, controlar asistencias, capturar calificaciones y generar consultas de información de manera rápida y organizada.

La aplicación está desarrollada con **Python**, utilizando **PySide6** para la interfaz gráfica y una base de datos relacional para almacenar toda la información académica.

---

# ✨ Características

## 👨‍🎓 Gestión de Alumnos

* Registro de alumnos.
* Edición de información.
* Eliminación de registros.
* Consulta rápida de estudiantes.

## 📚 Gestión de Materias

* Alta de materias.
* Modificación de materias.
* Eliminación de materias.
* Asignación de materias a estudiantes.

## 📝 Control de Calificaciones

* Registro de calificaciones.
* Actualización de notas.
* Eliminación de registros.
* Consulta de historial académico.
* Cálculo automático de promedios.

## 📅 Control de Asistencias

* Registro diario de asistencia.
* Control por fecha.
* Validación para evitar registros duplicados.
* Consulta histórica de asistencias.

## 🔎 Consultas Avanzadas

* Búsqueda de alumnos.
* Filtrado por materias.
* Consulta de calificaciones.
* Reportes académicos.

## 📊 Estadísticas Académicas

* Promedio general.
* Materias aprobadas.
* Materias reprobadas.
* Porcentaje de asistencia.

---

# 🖥️ Capturas del Sistema

### Inicio del Sistema

```text
Dashboard Principal
├── Alumnos
├── Materias
├── Calificaciones
├── Asistencias
└── Reportes
```

### Gestión Académica

```text
✔ Registro de alumnos
✔ Control de materias
✔ Captura de calificaciones
✔ Registro de asistencias
✔ Consultas rápidas
```

---

# 🛠️ Tecnologías Utilizadas

* Python 3.12
* PySide6
* SQLite / MySQL
* Qt Designer
* SQL
* Git

---

# 📂 Estructura del Proyecto

```text
AppEscritorioControl-Escolar/
│
├── main.py
│
├── database/
│   ├── conexion.py
│   └── database.db
│
├── views/
│   ├── alumnos.py
│   ├── materias.py
│   ├── calificaciones.py
│   └── asistencias.py
│
├── models/
│   ├── alumno.py
│   ├── materia.py
│   ├── calificacion.py
│   └── asistencia.py
│
├── assets/
│   ├── icons/
│   └── images/
│
└── README.md
```

---

# 📦 Instalación

## Clonar el repositorio

```bash
git clone https://github.com/isairey/AppEscritorioControl-Escolar.git

cd AppEscritorioControl-Escolar
```

## Crear entorno virtual

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# 🚀 Ejecución

Iniciar la aplicación:

```bash
python main.py
```

---

# 🗄️ Base de Datos

El sistema utiliza una base de datos para almacenar:

### Tabla Alumnos

```text
id_alumno
nombre
apellido
edad
correo
```

### Tabla Materias

```text
id_materia
nombre
descripcion
```

### Tabla Calificaciones

```text
id_calificacion
id_alumno
id_materia
calificacion
```

### Tabla Asistencias

```text
id_asistencia
id_alumno
id_materia
fecha
estado
```

---

# 🔒 Características de Seguridad

* Validación de datos.
* Prevención de registros duplicados.
* Integridad referencial.
* Manejo de errores.
* Protección contra datos inválidos.

---

# 🎯 Funcionalidades Futuras

* Exportación a PDF.
* Exportación a Excel.
* Sistema de usuarios.
* Roles y permisos.
* Reportes automáticos.
* Respaldo de base de datos.
* Gráficas estadísticas.
* Notificaciones académicas.

---

# 👨‍💻 Desarrollador



## Isai Reyes

**Desarrollador Full Stack | Python | Java | Spring Boot | React | Vue.js**

Especializado en:

* Desarrollo de Aplicaciones de Escritorio
* Bases de Datos
* Inteligencia Artificial
* Desarrollo Web
* Sistemas Administrativos
* Automatización de Procesos

GitHub:
https://github.com/isairey



---

# 🤝 Contribuciones

Las contribuciones son bienvenidas.

1. Realiza un Fork del proyecto.
2. Crea una nueva rama.

```bash
git checkout -b feature/nueva-funcionalidad
```

3. Realiza tus cambios.
4. Envía un Pull Request.

---

# 📄 Licencia

Este proyecto se distribuye bajo la licencia MIT.

---

<div align="center">

### ⭐ Gracias por utilizar el Sistema de Control Escolar ⭐

**Gestión Académica Inteligente para Instituciones Educativas**

</div>
