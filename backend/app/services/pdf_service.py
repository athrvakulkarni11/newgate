from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from io import BytesIO
from typing import List

class PDFService:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            spaceBefore=12,
            spaceAfter=12,
            leading=14
        ))

    def generate_pdf(self, title: str, content: str, sources: List[str]) -> BytesIO:
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        story = []
        
        # Add title
        story.append(Paragraph(title, self.styles['Title']))
        story.append(Spacer(1, 0.5*inch))
        
        # Add content sections
        sections = content.split('\n\n')
        for section in sections:
            if section.strip():
                story.append(Paragraph(section, self.styles['CustomBody']))
        
        # Add sources
        if sources:
            story.append(Spacer(1, 0.5*inch))
            story.append(Paragraph("Sources:", self.styles['Heading2']))
            for source in sources:
                story.append(Paragraph(source, self.styles['CustomBody']))
        
        doc.build(story)
        buffer.seek(0)
        return buffer 