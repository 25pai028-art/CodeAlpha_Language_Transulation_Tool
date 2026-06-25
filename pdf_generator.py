from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime

def generate_pdf(original, translated, source_lang="en", target_lang="en", sentiment_before="Neutral", sentiment_after="Neutral"):
    
    filename = "translation_report.pdf"
    
    doc = SimpleDocTemplate(
        filename,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#764ba2'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold',
        borderPadding=5,
        backColor=colors.HexColor('#f0f4ff')
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=10,
        leading=14
    )
    
    label_style = ParagraphStyle(
        'Label',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#666666'),
        fontName='Helvetica-Bold',
        spaceAfter=4
    )
    
    content = []
    
    # Header
    content.append(Paragraph("🌍 Language Translation Report", title_style))
    content.append(Paragraph(f"<i>Professional Translation Document</i>", subtitle_style))
    content.append(Spacer(1, 0.3*inch))
    
    # Metadata Table
    timestamp = datetime.now().strftime("%d %b, %Y at %I:%M %p")
    metadata_data = [
        ['Generated:', timestamp],
        ['Source Language:', source_lang.upper()],
        ['Target Language:', target_lang.upper()]
    ]
    
    metadata_table = Table(metadata_data, colWidths=[2*inch, 4*inch])
    metadata_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (0, -1), 10),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (1, 0), (1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e0e0e0'))
    ]))
    
    content.append(metadata_table)
    content.append(Spacer(1, 0.3*inch))
    
    # Original Text Section
    content.append(Paragraph("📖 Original Text", heading_style))
    original_para = Paragraph(
        f"<font face='Times-Roman' size=11>{original}</font>",
        body_style
    )
    content.append(original_para)
    content.append(Spacer(1, 0.2*inch))
    
    # Translated Text Section
    content.append(Paragraph("🌐 Translated Text", heading_style))
    translated_para = Paragraph(
        f"<font face='Times-Roman' size=11>{translated}</font>",
        body_style
    )
    content.append(translated_para)
    content.append(Spacer(1, 0.25*inch))
    
    # Sentiment Analysis
    content.append(Paragraph("😊 Sentiment Analysis", heading_style))
    
    sentiment_data = [
        ['Metric', 'Original', 'Translated', 'Status'],
        ['Sentiment', sentiment_before, sentiment_after, '✓' if sentiment_before == sentiment_after else '⚠']
    ]
    
    sentiment_table = Table(sentiment_data, colWidths=[1.3*inch, 1.3*inch, 1.3*inch, 0.8*inch])
    sentiment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#764ba2')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#f0f4ff')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#667eea')),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, 1), 10),
        ('TOPPADDING', (0, 1), (-1, 1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, 1), 8)
    ]))
    
    content.append(sentiment_table)
    content.append(Spacer(1, 0.4*inch))
    
    # Footer
    content.append(Paragraph(
        "<i style='color: #999; font-size: 9pt;'>This document was automatically generated by AI Language Translator | Confidential</i>",
        ParagraphStyle('Footer', parent=styles['Normal'], alignment=TA_CENTER, fontSize=9, textColor=colors.grey)
    ))
    
    doc.build(content)
    
    return filename