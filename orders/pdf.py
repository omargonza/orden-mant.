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
    HRFlowable,
)
import io
import datetime
import os


def build_pdf(data):
    buffer = io.BytesIO()

    # 📄 Configuración del documento
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2 * cm,
    )

    # 🧩 Estilos tipográficos
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="Titulo",
            fontSize=15,
            alignment=1,  # centrado
            spaceAfter=12,
            leading=18,
            textColor=colors.HexColor("#003b73"),
            fontName="Helvetica-Bold",
        )
    )
    styles.add(
        ParagraphStyle(
            name="Campo",
            fontSize=10.5,
            leading=14,
            spaceAfter=4,
            fontName="Helvetica",
            textColor=colors.HexColor("#2e2e2e"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="Seccion",
            fontSize=12,
            leading=16,
            spaceAfter=6,
            fontName="Helvetica-Bold",
            textColor=colors.HexColor("#0d47a1"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="Pie",
            fontSize=8.5,
            leading=12,
            alignment=1,
            textColor=colors.HexColor("#555555"),
        )
    )

    elements = []

    # ===============================
    # 🏗️ ENCABEZADO CON LOGO Y DATOS
    # ===============================
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
    header_data = []

    if os.path.exists(logo_path):
        img = Image(logo_path, width=3.5 * cm, height=3.5 * cm)
        header_data.append([
            img,
            Paragraph(
                "<b>SECTOR MANTENIMIENTO ELÉCTRICO</b><br/>ORDEN DE TRABAJO",
                styles["Titulo"]
            )
        ])
    else:
        header_data.append([
            "",
            Paragraph(
                "<b>SECTOR MANTENIMIENTO ELÉCTRICO</b><br/>ORDEN DE TRABAJO",
                styles["Titulo"]
            )
        ])

    tabla_header = Table(header_data, colWidths=[4 * cm, 12 * cm])
    tabla_header.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 0), (1, 0), "CENTER"),
            ]
        )
    )
    elements.append(tabla_header)
    elements.append(Spacer(1, 4))

    # 🔵 Línea separadora azul
    elements.append(
        HRFlowable(width="100%", color=colors.HexColor("#0d47a1"), thickness=2, spaceBefore=4, spaceAfter=10)
    )

    # 🗓️ Fecha de emisión
    fecha_gen = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    elements.append(Paragraph(f"<b>Emitido:</b> {fecha_gen}", styles["Campo"]))
    elements.append(Spacer(1, 8))

    # ===============================
    # 📋 DATOS PRINCIPALES
    # ===============================
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
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9.5),
                ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
            ]
        )
    )
    elements.append(tabla_datos)
    elements.append(Spacer(1, 12))

    # ===============================
    # 🧰 SECCIONES DE TAREAS
    # ===============================
    for titulo, key in [
        ("TAREA PEDIDA", "tarea_pedida"),
        ("TAREA REALIZADA", "tarea_realizada"),
        ("TAREA PENDIENTE", "tarea_pendiente"),
    ]:
        elements.append(Paragraph(titulo, styles["Seccion"]))
        elements.append(Paragraph(data.get(key, "—"), styles["Campo"]))
        elements.append(Spacer(1, 6))

    # ===============================
    # 💡 LUMINARIAS / EQUIPOS
    # ===============================
    if data.get("luminaria_equipos"):
        elements.append(Paragraph("LUMINARIAS / EQUIPOS", styles["Seccion"]))
        elements.append(Paragraph(data["luminaria_equipos"], styles["Campo"]))
        elements.append(Spacer(1, 10))

    # ===============================
    # 👷 TÉCNICOS
    # ===============================
    if data.get("tecnicos"):
        elements.append(Paragraph("TÉCNICOS", styles["Seccion"]))
        tecnicos_texto = "<br/>".join(
            [f"{t['legajo']} – {t['nombre']}" for t in data["tecnicos"]]
        )
        elements.append(Paragraph(tecnicos_texto, styles["Campo"]))
        elements.append(Spacer(1, 10))

    # ===============================
    # 🔩 MATERIALES UTILIZADOS
    # ===============================
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
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e3f2fd")),
                    ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9.5),
                ]
            )
        )
        elements.append(tabla_mat)
        elements.append(Spacer(1, 18))

    # ===============================
    # 📜 PIE DE PÁGINA CON COPYRIGHT
    # ===============================
    fecha_impresion = datetime.datetime.now().strftime("%Y")
    pie_texto = f"© {fecha_impresion}  Sistema de Mantenimiento del Sector Eléctrico — Desarrollado por conurbaDEV"
    elements.append(Spacer(1, 14))
    elements.append(Paragraph(pie_texto, styles["Pie"]))

    # ===============================
    # 🔚 GENERACIÓN DEL PDF
    # ===============================
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    nombre_archivo = f"orden_trabajo_{data['fecha']}.pdf"
    return pdf, nombre_archivo
