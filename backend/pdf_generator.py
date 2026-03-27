from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import io

def generate_health_report_pdf(user_data: dict, assessment_data: dict, blood_tests: list) -> bytes:
    """Generate comprehensive health report PDF"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2A9D8F'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2A9D8F'),
        spaceAfter=12,
        spaceBefore=20
    )
    
    # Title
    story.append(Paragraph("HealthGuard AI - Health Assessment Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Patient Information
    story.append(Paragraph("Patient Information", heading_style))
    patient_data = [
        ['Name:', user_data.get('name', 'N/A')],
        ['Age:', str(user_data.get('age', 'N/A'))],
        ['Sex:', user_data.get('sex', 'N/A').capitalize()],
        ['Report Date:', datetime.now().strftime('%B %d, %Y')]
    ]
    patient_table = Table(patient_data, colWidths=[2*inch, 4*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f9f8')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    story.append(patient_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Risk Assessment
    story.append(Paragraph("Risk Assessment Summary", heading_style))
    risk_level = assessment_data.get('risk_level', 'Unknown')
    risk_color = {'Low': '#10b981', 'Medium': '#f59e0b', 'High': '#ef4444'}.get(risk_level, '#6b7280')
    
    risk_data = [
        ['Overall Risk Level:', risk_level],
        ['Diabetes Score:', f"{assessment_data.get('diabetes_score', 0)}%"],
        ['Cholesterol Score:', f"{assessment_data.get('cholesterol_score', 0)}%"],
        ['Assessment Date:', datetime.fromisoformat(assessment_data.get('created_at')).strftime('%B %d, %Y')]
    ]
    risk_table = Table(risk_data, colWidths=[2.5*inch, 3.5*inch])
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f9f8')),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor(risk_color)),
        ('TEXTCOLOR', (1, 0), (1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    story.append(risk_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Blood Test Results
    if blood_tests:
        story.append(Paragraph("Blood Test History", heading_style))
        blood_test_data = [['Test Date', 'LDL', 'HDL', 'Triglycerides', 'HbA1c']]
        
        for test in blood_tests[:5]:  # Last 5 tests
            blood_test_data.append([
                datetime.fromisoformat(test.get('created_at')).strftime('%m/%d/%Y'),
                f"{test.get('ldl', 'N/A')} mg/dL",
                f"{test.get('hdl', 'N/A')} mg/dL",
                f"{test.get('triglycerides', 'N/A')} mg/dL",
                f"{test.get('hba1c', 'N/A')}%"
            ])
        
        blood_table = Table(blood_test_data, colWidths=[1.2*inch, 1.2*inch, 1.2*inch, 1.4*inch, 1*inch])
        blood_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2A9D8F')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
        ]))
        story.append(blood_table)
        story.append(Spacer(1, 0.2*inch))
    
    # Medical Disclaimer
    story.append(Spacer(1, 0.3*inch))
    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#6b7280'),
        alignment=TA_LEFT,
        borderWidth=1,
        borderColor=colors.HexColor('#e5e7eb'),
        borderPadding=10,
        backColor=colors.HexColor('#f9fafb')
    )
    disclaimer_text = """<b>IMPORTANT MEDICAL DISCLAIMER:</b> This report is generated by HealthGuard AI for informational and educational purposes only. 
    It is NOT intended to be a substitute for professional medical advice, diagnosis, or treatment. The risk assessments and recommendations 
    provided are based on self-reported data and machine learning algorithms and should not be considered as definitive medical diagnoses. 
    Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. 
    Never disregard professional medical advice or delay in seeking it because of information presented in this report. 
    If you think you may have a medical emergency, call your doctor or emergency services immediately."""
    story.append(Paragraph(disclaimer_text, disclaimer_style))
    
    # Footer
    story.append(Spacer(1, 0.2*inch))
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, alignment=TA_CENTER, textColor=colors.grey)
    story.append(Paragraph(f"Generated by HealthGuard AI | {datetime.now().strftime('%B %d, %Y %I:%M %p')}", footer_style))
    
    # Build PDF
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes
