from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import textwrap

def generate_pdf(report: str, sources: list[str]) -> BytesIO:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Set up initial positions
    y = height - 50
    margin = 50
    line_height = 15
    
    # Add title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, y, "Research Report")
    y -= line_height * 2
    
    # Add report content
    c.setFont("Helvetica", 12)
    
    # Wrap text to fit page width
    wrapper = textwrap.TextWrapper(width=80)
    lines = wrapper.wrap(report)
    
    for line in lines:
        if y < margin:  # Check if we need a new page
            c.showPage()
            y = height - margin
            c.setFont("Helvetica", 12)
        
        c.drawString(margin, y, line)
        y -= line_height
    
    # Add sources
    y -= line_height * 2
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Sources:")
    y -= line_height
    
    c.setFont("Helvetica", 10)
    for source in sources:
        if y < margin:  # Check if we need a new page
            c.showPage()
            y = height - margin
            c.setFont("Helvetica", 10)
            
        c.drawString(margin, y, source)
        y -= line_height
    
    c.save()
    buffer.seek(0)
    return buffer 