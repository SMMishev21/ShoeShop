from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
from datetime import datetime


def create_order_pdf(order, user):
    """Generate PDF for an order"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=1  # Center
    )

    elements.append(Paragraph(f"ПОРЪЧКА #{order['id']}", title_style))
    elements.append(Spacer(1, 0.5 * cm))

    # Order info
    info_style = styles['Normal']
    info_data = [
        ['Дата:', order['created_at']],
        ['Клиент:', user['email']],
        ['Адрес за доставка:', order['address']],
        ['Начин на плащане:', order['payment']],
        ['Статус:', order['status'].upper()]
    ]

    info_table = Table(info_data, colWidths=[5 * cm, 12 * cm])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#34495e')),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))

    elements.append(info_table)
    elements.append(Spacer(1, 1 * cm))

    # Products table header
    elements.append(Paragraph("<b>ПРОДУКТИ:</b>", styles['Heading2']))
    elements.append(Spacer(1, 0.3 * cm))

    # Products table
    products_data = [['Продукт', 'Описание', 'Цена', 'Брой', 'Сума']]

    for item in order['items']:
        products_data.append([
            item['product_name'],
            item['product_description'][:50] + '...' if len(item['product_description']) > 50 else item[
                'product_description'],
            f"{item['price']:.2f} лв",
            str(item['qty']),
            f"{item['subtotal']:.2f} лв"
        ])

    products_table = Table(products_data, colWidths=[4 * cm, 6 * cm, 2.5 * cm, 2 * cm, 2.5 * cm])
    products_table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

        # Body
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        # Grid
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))

    elements.append(products_table)
    elements.append(Spacer(1, 1 * cm))

    # Total
    total_data = [
        ['ОБЩА СУМА:', f"{order['total_price']:.2f} лв"]
    ]

    total_table = Table(total_data, colWidths=[14.5 * cm, 2.5 * cm])
    total_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#e74c3c')),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('LINEABOVE', (0, 0), (-1, 0), 2, colors.black),
    ]))

    elements.append(total_table)
    elements.append(Spacer(1, 2 * cm))

    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=1
    )
    elements.append(Paragraph("Благодарим Ви за поръчката!", footer_style))
    elements.append(Paragraph("ShoeShop © 2025", footer_style))

    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer