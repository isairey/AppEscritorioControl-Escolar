from PySide6.QtWidgets import *
from database import conectar

from reportlab.pdfgen import canvas

import pandas as pd


class ReportesWidget(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        titulo = QLabel(
            "Generación de Reportes"
        )

        titulo.setStyleSheet("""
        font-size:24px;
        font-weight:bold;
        """)

        self.btnPDF = QPushButton(
            "Generar PDF Alumnos"
        )

        self.btnExcel = QPushButton(
            "Exportar Excel"
        )

        layout.addWidget(titulo)
        layout.addWidget(self.btnPDF)
        layout.addWidget(self.btnExcel)

        layout.addStretch()

        self.setLayout(layout)

        self.btnPDF.clicked.connect(
            self.generar_pdf
        )

        self.btnExcel.clicked.connect(
            self.generar_excel
        )

    def generar_pdf(self):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM alumnos
        """)

        alumnos = cursor.fetchall()

        conn.close()

        pdf = canvas.Canvas(
            "Reporte_Alumnos.pdf"
        )

        pdf.setFont(
            "Helvetica-Bold",
            16
        )

        pdf.drawString(
            50,
            800,
            "Reporte de Alumnos"
        )

        y = 760

        pdf.setFont(
            "Helvetica",
            11
        )

        for alumno in alumnos:

            texto = (
                f"{alumno[1]} "
                f"{alumno[2]} "
                f"- {alumno[3]} "
                f"{alumno[4]}"
            )

            pdf.drawString(
                50,
                y,
                texto
            )

            y -= 20

            if y < 50:
                pdf.showPage()
                y = 800

        pdf.save()

        QMessageBox.information(
            self,
            "PDF",
            "Reporte generado"
        )

    def generar_excel(self):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM alumnos
        """)

        alumnos = cursor.fetchall()

        conn.close()

        df = pd.DataFrame(
            alumnos,
            columns=[
                "ID",
                "Nombre",
                "Apellido",
                "Grado",
                "Grupo"
            ]
        )

        df.to_excel(
            "Alumnos.xlsx",
            index=False
        )

        QMessageBox.information(
            self,
            "Excel",
            "Archivo exportado"
        )