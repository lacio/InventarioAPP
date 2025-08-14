import os
from uuid import UUID
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
import base64
from io import BytesIO

from . import schemas

PDF_DIR = "generated_pdfs"
LOGO_URL = os.getenv("PDF_LOGO_URL")

if not os.path.exists(PDF_DIR):
    os.makedirs(PDF_DIR)

def get_pdf_path(nota_id: UUID) -> str:
    return os.path.join(PDF_DIR, f"{nota_id}.pdf")

def generate_nota_pdf(nota: schemas.Nota):
    pdf_path = get_pdf_path(nota.id)
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Logo
    if LOGO_URL:
        try:
            # In a real app, consider caching the logo image
            img = Image(LOGO_URL, width=1.5*inch, height=0.5*inch)
            img.hAlign = 'LEFT'
            story.append(img)
        except Exception as e:
            print(f"Could not load logo from URL: {e}")

    story.append(Spacer(1, 0.25*inch))

    # Title
    story.append(Paragraph(f"Comprobante de Salida/Devolución", styles['h1']))
    story.append(Paragraph(f"Nota ID: {nota.id}", styles['h3']))
    story.append(Spacer(1, 0.2*inch))

    # Header Data
    header_data = [
        [f"Empresa Solicitante:", nota.empresa_solicitante],
        [f"Filial:", nota.filial],
        [f"Almacén:", nota.almacen],
        [f"Estado:", nota.estado],
        [f"Fecha:", nota.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")]
    ]
    header_table = Table(header_data, colWidths=[1.5*inch, 4*inch])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.2*inch))

    # Items Table
    items_data = [["Línea", "Producto", "Descripción", "Cantidad", "UM", "Observación"]]
    for item in nota.items:
        obs = f"SC: {item.sc_numero}" if item.intercompany else ""
        items_data.append([
            item.linea,
            item.producto,
            item.descripcion,
            item.cantidad_entregada,
            item.um,
            obs
        ])
    
    items_table = Table(items_data, colWidths=[0.5*inch, 1*inch, 2.5*inch, 0.7*inch, 0.5*inch, 1.3*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    story.append(items_table)
    story.append(Spacer(1, 0.3*inch))

    # Signatures and QR
    qr_img = None
    qr_data = f'{{"nota_id": "{nota.id}", "hash": "{nota.hash}"}}'
    qr = qrcode.make(qr_data)
    qr_buffer = BytesIO()
    qr.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)
    qr_img = Image(qr_buffer, width=1.2*inch, height=1.2*inch)

    solicitante_img = Image(BytesIO(base64.b64decode(nota.firmas.solicitante)), width=1.5*inch, height=0.7*inch) if nota.firmas else Paragraph("Sin firma", styles['Normal'])
    entrega_img = Image(BytesIO(base64.b64decode(nota.firmas.entrega)), width=1.5*inch, height=0.7*inch) if nota.firmas else Paragraph("Sin firma", styles['Normal'])

    footer_data = [
        [solicitante_img, entrega_img, qr_img],
        [Paragraph("Firma Solicitante", styles['Normal']), Paragraph("Firma Entrega", styles['Normal']), Paragraph("QR Verificación", styles['Normal'])]
    ]
    footer_table = Table(footer_data, colWidths=[2*inch, 2*inch, 1.5*inch])
    footer_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,1), (-1,1), 0),
    ]))
    story.append(footer_table)

    doc.build(story)
    return pdf_path
