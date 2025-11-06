# core/orders/pdf.py
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.units import mm
from datetime import datetime

def build_pdf(data: dict):
    """
    Genera el PDF (exacto para producción en Render) con ReportLab.
    Retorna (pdf_bytes, nombre_archivo).
    """

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=18*mm,
        rightMargin=18*mm,
        topMargin=18*mm,
        bottomMargin=18*mm,
        title="Orden de Trabajo",
        author="Sistema de Mantenimiento",
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="H1", fontSize=16, leading=18, spaceAfter=8, textColor=colors.HexColor("#222222"),))
    styles.add(ParagraphStyle(name="H2", fontSize=11, leading=14, spaceBefore=10, spaceAfter=4, textColor=colors.HexColor("#444"),))
    styles.add(ParagraphStyle(name="Body", fontSize=10, leading=13))
    styles.add(ParagraphStyle(name="Small", fontSize=9, leading=12, textColor=colors.HexColor("#666")))
    styles.add(ParagraphStyle(name="Label", fontSize=9, leading=12, textColor=colors.HexColor("#777")))

    elems = []

    # -------- Título (TABLERO + CIRCUITO + FECHA) ----------
    fecha_dt = data["fecha"]
    if isinstance(fecha_dt, str):
        try:
            fecha_dt = datetime.strptime(fecha_dt, "%Y-%m-%d").date()
        except Exception:
            # fallback dd/mm/YYYY
            fecha_dt = datetime.strptime(fecha_dt, "%d/%m/%Y").date()

    titulo = f"Orden de Trabajo – {data['tablero']} – {data['circuito']} – {fecha_dt.strftime('%d/%m/%Y')}"
    elems.append(Paragraph(titulo, styles["H1"]))
    elems.append(Spacer(1, 4))

    # -------- Bloque 1: Datos generales ----------
    info_table = [
        ["Ubicación", data["ubicacion"], "Vehículo", data["vehiculo"]],
        ["Tablero", data["tablero"], "Circuito", data["circuito"]],
        ["Fecha", fecha_dt.strftime("%d/%m/%Y"), "KMs (ini/fin)", f"{data['km_inicial']} / {data['km_final']}"],
    ]
    t = Table(info_table, colWidths=[28*mm, 60*mm, 28*mm, 45*mm])
    t.setStyle(TableStyle([
        ("FONTNAME", (0,0), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("LEADING", (0,0), (-1,-1), 11),
        ("BACKGROUND", (0,0), (-1,0), colors.whitesmoke),
        ("TEXTCOLOR", (0,0), (-1,0), colors.HexColor("#333333")),
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("INNERGRID", (0,0), (-1,-1), 0.25, colors.HexColor("#DDDDDD")),
        ("BOX", (0,0), (-1,-1), 0.6, colors.HexColor("#BBBBBB")),
        ("BACKGROUND", (0,0), (-1,-1), colors.white),
    ]))
    elems.append(t)
    elems.append(Spacer(1, 8))

    # -------- Técnicos ----------
    elems.append(Paragraph("Técnicos", styles["H2"]))
    tecnicos_lines = ", ".join([f"{t['legajo']} - {t['nombre']}" for t in data.get("tecnicos", [])]) or "—"
    elems.append(Paragraph(tecnicos_lines, styles["Body"]))
    elems.append(Spacer(1, 6))

    # -------- Tarea pedida ----------
    elems.append(Paragraph("Tarea pedida", styles["H2"]))
    elems.append(Paragraph(data.get("tarea_pedida", "") or "—", styles["Body"]))
    elems.append(Spacer(1, 6))

    # -------- Observaciones (solo título de sección) ----------
    elems.append(Paragraph("Observaciones", styles["H2"]))

    # -------- Tarea realizada ----------
    elems.append(Paragraph("<b>Tarea realizada</b>", styles["Label"]))
    elems.append(Paragraph(data.get("tarea_realizada", "") or "—", styles["Body"]))
    elems.append(Spacer(1, 4))

    # -------- Tarea pendiente ----------
    elems.append(Paragraph("<b>Tarea pendiente</b>", styles["Label"]))
    elems.append(Paragraph(data.get("tarea_pendiente", "") or "—", styles["Body"]))
    elems.append(Spacer(1, 4))

    # -------- Luminaria / Equipos encendidos ----------
    elems.append(Paragraph("<b>Luminaria / Equipos encendidos</b>", styles["Label"]))
    elems.append(Paragraph(data.get("luminaria_equipos", "") or "—", styles["Body"]))
    elems.append(Spacer(1, 8))

    # -------- Materiales ----------
    mats = data.get("materiales") or []
    elems.append(Paragraph("Materiales", styles["H2"]))
    if mats:
        rows = [["Material", "Cant", "Unidad"]]
        for m in mats:
            rows.append([m.get("material",""), str(m.get("cant","")), m.get("unidad","")])
        mt = Table(rows, colWidths=[100*mm, 25*mm, 25*mm])
        mt.setStyle(TableStyle([
            ("FONTNAME", (0,0), (-1,-1), "Helvetica"),
            ("FONTSIZE", (0,0), (-1,-1), 9),
            ("LEADING", (0,0), (-1,-1), 11),
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#F1F1F1")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.HexColor("#333333")),
            ("ALIGN", (1,1), (2,-1), "CENTER"),
            ("ALIGN", (0,0), (0,-1), "LEFT"),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("GRID", (0,0), (-1,-1), 0.25, colors.HexColor("#DDDDDD")),
            ("BOX", (0,0), (-1,-1), 0.6, colors.HexColor("#BBBBBB")),
        ]))
        elems.append(mt)
    else:
        elems.append(Paragraph("—", styles["Body"]))

    # -------- Footer / info mínima --------
    elems.append(Spacer(1, 8))
    elems.append(Paragraph("Documento generado automáticamente por el sistema de mantenimiento.", styles["Small"]))

    # Compilar
    doc.build(elems)

    pdf_bytes = buffer.getvalue()
    buffer.close()

    # Nombre de archivo: OT_{TABLERO}_{CIRCUITO}_{YYYYMMDD}.pdf
    nombre_archivo = f"OT_{data['tablero'].replace(' ','_')}_{data['circuito'].replace(' ','_')}_{fecha_dt.strftime('%Y%m%d')}.pdf"
    return pdf_bytes, nombre_archivo
