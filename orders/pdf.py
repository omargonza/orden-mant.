# orders/pdf.py
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image,
)
import io
import datetime
import os


def build_pdf(data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="Titulo",
            fontSize=16,
            alignment=1,  # centrado
            spaceAfter=14,
            leading=20,
            textColor=colors.HexColor("#1f1f1f"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="Campo",
            fontSize=10.5,
            leading=13,
            spaceAfter=4,
            fontName="Helvetica",
            textColor=colors.HexColor("#333333"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="Seccion",
            fontSize=12,
            leading=16,
            spaceAfter=8,
            fontName="Helvetica-Bold",
            textColor=colors.HexColor("#1f3b73"),
        )
    )

    elements = []

    # 🏷️ Encabezado (logo opcional)
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
    if os.path.exists(logo_path):
        img = Image(logo_path, width=3.5 * cm, height=3.5 * cm)
        elements.append(img)

    elements.append(
        Paragraph("<b>SECTOR MANTENIMIENTO ELECTRICO</b><br/>ORDEN DE TRABAJO", styles["Titulo"])
    )
    elements.append(Spacer(1, 12))

    # 🗓️ Datos principales
    datos = [
        ["Fecha:", data["fecha"].strftime("%d/%m/%Y"), "Ubicación:", data["ubicacion"]],
        ["Tablero:", data["tablero"], "Circuito:", data["circuito"]],
        [
            "Vehículo:",
            data["vehiculo"],
            "Kms:",
            f"{data['km_inicial']} - {data['km_final']}",
        ],
    ]
    tabla_datos = Table(datos, colWidths=[2.5 * cm, 6 * cm, 2.5 * cm, 6 * cm])
    tabla_datos.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    elements.append(tabla_datos)
    elements.append(Spacer(1, 10))

    # 🧰 Sección de tareas
    elements.append(Paragraph("TAREA PEDIDA", styles["Seccion"]))
    elements.append(Paragraph(data.get("tarea_pedida", "—"), styles["Campo"]))
    elements.append(Spacer(1, 6))

    elements.append(Paragraph("TAREA REALIZADA", styles["Seccion"]))
    elements.append(Paragraph(data.get("tarea_realizada", "—"), styles["Campo"]))
    elements.append(Spacer(1, 6))

    elements.append(Paragraph("TAREA PENDIENTE", styles["Seccion"]))
    elements.append(Paragraph(data.get("tarea_pendiente", "—"), styles["Campo"]))
    elements.append(Spacer(1, 10))

    # 💡 Luminarias
    if data.get("luminaria_equipos"):
        elements.append(Paragraph("LUMINARIAS / EQUIPOS", styles["Seccion"]))
        elements.append(Paragraph(data["luminaria_equipos"], styles["Campo"]))
        elements.append(Spacer(1, 10))

    # 👷 Técnicos
    if data.get("tecnicos"):
        elements.append(Paragraph("TÉCNICOS", styles["Seccion"]))
        tecnicos_texto = "<br/>".join(
            [f"{t['legajo']} – {t['nombre']}" for t in data["tecnicos"]]
        )
        elements.append(Paragraph(tecnicos_texto, styles["Campo"]))
        elements.append(Spacer(1, 10))

    # 🔩 Materiales
    if data.get("materiales"):
        elements.append(Paragraph("MATERIALES UTILIZADOS", styles["Seccion"]))
        filas = [["Material", "Cantidad", "Unidad"]] + [
            [m["material"], str(m["cant"]), m["unidad"]] for m in data["materiales"]
        ]
        tabla_mat = Table(filas, colWidths=[8 * cm, 3 * cm, 3 * cm])
        tabla_mat.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9.5),
                ]
            )
        )
        elements.append(tabla_mat)
        elements.append(Spacer(1, 18))

    # ✍️ Pie
    fecha_gen = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    pie = f"Generado automáticamente el {fecha_gen} — Yoquet Diseños"
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(pie, styles["Campo"]))

    # 🔚 Generación
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf, f"orden_trabajo_{data['fecha']}.pdf"
