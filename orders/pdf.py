from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os

styles = getSampleStyleSheet()
style_normal = ParagraphStyle(
    "normal_custom",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=9,
    leading=11,
    alignment=TA_LEFT,
)
style_bold = ParagraphStyle(
    "bold_custom",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=10,
    leading=12,
    alignment=TA_LEFT,
)
style_center = ParagraphStyle(
    "center_custom",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=9,
    alignment=TA_CENTER,
)

def draw_paragraph(c, text, x, y, w, h, style=style_normal):
    """Renderiza texto multilínea dentro de un área."""
    p = Paragraph(str(text).replace("\n", "<br/>"), style)
    frame = Frame(x, y, w, h, showBoundary=0)
    frame.addFromList([p], c)

def build_pdf(data: dict) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    W, H = A4
    margin_x = 15 * mm
    y = H - 25 * mm

    # 🟦 LOGO + TÍTULO
    logo_path = os.path.join("static", "logo.png")
    if os.path.exists(logo_path):
        c.drawImage(logo_path, margin_x, H - 30 * mm, width=30 * mm, height=20 * mm, preserveAspectRatio=True)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(W / 2, H - 25 * mm, "ORDEN DE TRABAJO – PARTE DE MANTENIMIENTO")
    y -= 15 * mm

    # 🟨 1. DATOS GENERALES
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin_x, y, "1. Datos generales")
    y -= 8 * mm

    info = [
        ["Fecha", data.get("fecha", "")],
        ["Centro de costos", data.get("centro_costos", "")],
        ["Ubicación", data.get("ubicacion", "")],
        ["Tipo de mantenimiento", data.get("tipo_mantenimiento", "")],
        ["Prioridad", data.get("prioridad", "")],
    ]
    t = Table(info, colWidths=[45 * mm, 125 * mm])
    t.setStyle(TableStyle([
        ("BOX", (0,0), (-1,-1), 0.5, colors.black),
        ("INNERGRID", (0,0), (-1,-1), 0.25, colors.grey),
        ("BACKGROUND", (0,0), (0,-1), colors.whitesmoke),
        ("FONT", (0,0), (-1,-1), "Helvetica", 9),
    ]))
    t.wrapOn(c, W, H)
    h_table = len(info) * 8 * mm
    t.drawOn(c, margin_x, y - h_table)
    y -= h_table + 15 * mm

    # 🟧 2. TÍTULO DE LA TAREA
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin_x, y, "2. Título de la tarea")
    y -= 6 * mm
    tarea_text = data.get("tarea", "—")
    draw_paragraph(c, tarea_text, margin_x, y - 10 * mm, 180 * mm, 10 * mm)
    y -= 18 * mm

    # 3. Descripción de la tarea
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin_x, y, "3. Descripción de la tarea")
    y -= 6 * mm
    obs_text = data.get("observaciones", "—")
    draw_paragraph(c, obs_text, margin_x, y - 90 * mm, 180 * mm, 90 * mm)  # ← subí a 90mm
    y -= 100 * mm


    # 🟦 4. TABLEROS Y CIRCUITOS
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin_x, y, "4. Tablero(s) intervenido(s) y Circuitos")
    y -= 6 * mm
    tableros = data.get("tableros", [])
    if isinstance(tableros, list):
        tablero_text = ", ".join(tableros) if tableros else "—"
    else:
        tablero_text = tableros or "—"
    circuito_text = data.get("circuitos", "—")
    texto = f"<b>Tableros:</b> {tablero_text}<br/><b>Circuito(s):</b> {circuito_text}"
    draw_paragraph(c, texto, margin_x, y - 25 * mm, 180 * mm, 25 * mm)
    y -= 33 * mm

    # 🟨 5. HORARIOS Y TÉCNICOS
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin_x, y, "5. Horarios y técnicos")
    y -= 6 * mm
    horarios = [["Hora inicio", data.get("hora_inicio", ""), "Hora fin", data.get("hora_fin", "")]]
    th = Table(horarios, colWidths=[30 * mm, 55 * mm, 30 * mm, 55 * mm])
    th.setStyle(TableStyle([
        ("BOX", (0,0), (-1,-1), 0.5, colors.black),
        ("BACKGROUND", (0,0), (0,-1), colors.whitesmoke),
        ("BACKGROUND", (2,0), (2,-1), colors.whitesmoke),
        ("FONT", (0,0), (-1,-1), "Helvetica", 9),
    ]))
    th.wrapOn(c, W, H)
    th.drawOn(c, margin_x, y - 10 * mm)
    y -= 22 * mm

    # Legajos
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin_x, y, "Legajos:")
    legajos = data.get("legajos", [])
    texto_legajos = ", ".join(f"{lg.get('id','')} - {lg.get('nombre','')}" for lg in legajos) or "—"
    draw_paragraph(c, texto_legajos, margin_x, y - 16 * mm, 180 * mm, 16 * mm)
    y -= 28 * mm

    # 🟫 6. MATERIALES UTILIZADOS
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin_x, y, "6. Materiales utilizados")
    y -= 8 * mm
    mats = data.get("materiales", [])
    if mats:
        mat_data = [["Material", "Cantidad", "Unidad"]] + [
            [m.get("material",""), str(m.get("cant","")), m.get("unidad","")] for m in mats
        ]
        tm = Table(mat_data, colWidths=[100*mm, 40*mm, 40*mm])
        tm.setStyle(TableStyle([
            ("BOX", (0,0), (-1,-1), 0.5, colors.black),
            ("INNERGRID", (0,0), (-1,-1), 0.25, colors.grey),
            ("BACKGROUND", (0,0), (-1,0), colors.whitesmoke),
            ("FONT", (0,0), (-1,0), "Helvetica-Bold", 9),
            ("FONT", (0,1), (-1,-1), "Helvetica", 9),
        ]))
        tm.wrapOn(c, W, H)
        tm.drawOn(c, margin_x, y - (len(mat_data)*6*mm))
        y -= (len(mat_data)*6*mm + 10)
    else:
        draw_paragraph(c, "—", margin_x, y - 10*mm, 180*mm, 10*mm)
        y -= 20 * mm

    # 🖊️ PIE DE FIRMA
    y_firma = 40 * mm
    c.line(margin_x + 20 * mm, y_firma, margin_x + 80 * mm, y_firma)
    c.line(W - 80 * mm, y_firma, W - 20 * mm, y_firma)
    c.setFont("Helvetica", 9)
    c.drawCentredString(margin_x + 50 * mm, y_firma - 5, "Firma Técnico Responsable")
    c.drawCentredString(W - 50 * mm, y_firma - 5, "Firma Supervisor de Turno")

    c.showPage()
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
