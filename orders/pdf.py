from io import BytesIO
from datetime import datetime, date
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Table,
    TableStyle,
    Spacer,
    Image,
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """
    Canvas personalizado para agregar número de página y pie validado.
    """
    def __init__(self, *args, tecnico="Desconocido", **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []
        self.tecnico = tecnico

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """
        Recorre todas las páginas para escribir el pie con número total.
        """
        total_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_footer(total_pages)
            super().showPage()
        super().save()

    def draw_footer(self, total_pages):
        """
        Dibuja el pie de validación y numeración.
        """
        width, height = A4
        self.saveState()

        # Línea divisoria gris
        self.setStrokeColor(colors.HexColor("#cccccc"))
        self.setLineWidth(0.7)
        self.line(40, 55, width - 40, 55)

        # Fecha de generación
        fecha_generacion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        texto = f"📄 Documento generado automáticamente el {fecha_generacion} por {self.tecnico}."
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#666666"))
        self.drawCentredString(width / 2.0, 43, texto)

        # Número de página (alineado a la derecha)
        page_number = f"Página {self._pageNumber} de {total_pages}"
        self.drawRightString(width - 40, 30, page_number)

        self.restoreState()


def build_pdf(data):
    buffer = BytesIO()

    # Técnico responsable
    tecnico = "Desconocido"
    if data.get("legajos") and data["legajos"][0].get("nombre"):
        tecnico = data["legajos"][0]["nombre"]

    # Configuración del documento
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=70,  # espacio para el pie
    )

    styles = getSampleStyleSheet()
    style_title = ParagraphStyle(
        name="Title",
        fontSize=14,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0a4a87"),
        spaceAfter=18,
    )
    style_section = ParagraphStyle(
        name="Section",
        fontSize=12,
        leading=14,
        textColor=colors.HexColor("#333333"),
        spaceAfter=6,
        spaceBefore=10,
    )
    style_normal = styles["Normal"]

    elements = []

    # --- LOGO (opcional) ---
    logo_path = "static/logo_ausol.png"
    try:
        import os
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=80, height=40)
            logo.hAlign = "LEFT"
            elements.append(logo)
            elements.append(Spacer(1, 6))
    except Exception as e:
        print("⚠️ No se pudo cargar el logo:", e)

    # --- TITULO ---
    elements.append(Paragraph("ORDEN DE TRABAJO – PARTE DE MANTENIMIENTO", style_title))
    elements.append(Spacer(1, 10))

    # --- DATOS GENERALES ---
    elements.append(Paragraph("<b>1. Datos generales</b>", style_section))
    tabla_datos = [
        ["Fecha", data.get("fecha", "")],
        ["Centro de costos", data.get("centro_costos", "")],
        ["Ubicación", data.get("ubicacion", "")],
        ["Tipo de mantenimiento", data.get("tipo_mantenimiento", "")],
        ["Prioridad", data.get("prioridad", "")],
    ]
    t1 = Table(tabla_datos, colWidths=[160, 340])
    t1.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ]
        )
    )
    elements.append(t1)
    elements.append(Spacer(1, 12))

    # --- TAREA ---
    elements.append(Paragraph("<b>2. Título de la tarea</b>", style_section))
    elements.append(Paragraph(data.get("tarea", ""), style_normal))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("<b>3. Descripción de la tarea</b>", style_section))
    observaciones = data.get("observaciones", "").replace("\n", "<br/>")
    elements.append(Paragraph(observaciones, style_normal))
    elements.append(Spacer(1, 10))

    # --- TABLEROS ---
    elements.append(Paragraph("<b>4. Tablero(s) intervenido(s) y Circuitos</b>", style_section))
    tableros = ", ".join(data.get("tableros", []))
    elements.append(Paragraph(f"<b>Tableros:</b> {tableros}", style_normal))
    elements.append(Paragraph(f"<b>Circuito(s):</b> {data.get('circuitos', '')}", style_normal))
    elements.append(Spacer(1, 10))

    # --- HORARIOS Y TECNICOS ---
    elements.append(Paragraph("<b>5. Horarios y técnicos</b>", style_section))
    elements.append(
        Paragraph(
            f"Hora inicio: {data.get('hora_inicio', '')} — Hora fin: {data.get('hora_fin', '')}",
            style_normal,
        )
    )

    if data.get("legajos"):
        legajos_txt = ", ".join(
            [f"{l.get('id', '')} - {l.get('nombre', '')}" for l in data["legajos"]]
        )
        elements.append(Paragraph(f"<b>Legajos:</b> {legajos_txt}", style_normal))
    elements.append(Spacer(1, 10))

    # --- MATERIALES ---
    elements.append(Paragraph("<b>6. Materiales utilizados</b>", style_section))
    if data.get("materiales"):
        tabla_materiales = [["Material", "Cantidad", "Unidad"]]
        for m in data["materiales"]:
            tabla_materiales.append(
                [m.get("material", ""), str(m.get("cant", "")), m.get("unidad", "")]
            )
        t2 = Table(tabla_materiales, colWidths=[300, 80, 80])
        t2.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0a4a87")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ]
            )
        )
        elements.append(t2)
    else:
        elements.append(Paragraph("—", style_normal))

    # --- GENERAR PDF ---
    doc.build(elements, canvasmaker=lambda *args, **kwargs: NumberedCanvas(*args, tecnico=tecnico, **kwargs))

    pdf_bytes = buffer.getvalue()
    buffer.close()

    # --- NOMBRE DINÁMICO DEL ARCHIVO ---
    tablero = ""
    if data.get("tableros"):
        tablero = str(data["tableros"][0]).replace(" ", "_")
    circuito = str(data.get("circuitos", "")).replace(" ", "_")
    fecha = data.get("fecha", str(date.today()))

    nombre_archivo = f"OT_{fecha}_{tablero}_{circuito or 'sinCircuito'}.pdf"
    nombre_archivo = nombre_archivo.replace("__", "_")

    return pdf_bytes, nombre_archivo
