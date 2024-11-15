import io
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

def crear_pdf_minuta(nombre_archivo, resumen, objetivos, compromisos, participantes, transcripcion):
    # Crear un buffer para almacenar el PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    elements = []
    styles = getSampleStyleSheet()

    # Título
    elements.append(Paragraph("Minuta de la Reunión", styles['Title']))
    elements.append(Spacer(1, 12))

    # Resumen
    elements.append(Paragraph("Resumen", styles['Heading2']))
    elements.append(Paragraph(resumen, styles['BodyText']))
    elements.append(Spacer(1, 12))

    # Participantes
    if participantes:
        elements.append(Paragraph("Participantes", styles['Heading2']))
        participantes_unicos = sorted(set(participantes))
        participants_text = ", ".join(participantes_unicos)
        elements.append(Paragraph(participants_text, styles['BodyText']))
        elements.append(Spacer(1, 12))

    # Objetivos
    if objetivos:
        elements.append(Paragraph("Objetivos", styles['Heading2']))
        objetivos_list = [[f"{i+1}. {obj}"] for i, obj in enumerate(objetivos)]
        table_objetivos = Table(objetivos_list)
        table_objetivos.setStyle(TableStyle([ 
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(table_objetivos)
        elements.append(Spacer(1, 12))

    # Compromisos
    if compromisos:
        elements.append(Paragraph("Compromisos", styles['Heading2']))
        compromisos_list = [[f"{i+1}. {comp}"] for i, comp in enumerate(compromisos)]
        table_compromisos = Table(compromisos_list)
        table_compromisos.setStyle(TableStyle([ 
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(table_compromisos)
        elements.append(Spacer(1, 12))
    
    # Transcripcion
    if transcripcion:
        elements.append(Paragraph("Transcripción", styles['Heading2']))
        elements.append(Paragraph(transcripcion, styles['BodyText']))
        elements.append(Spacer(1, 12))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()