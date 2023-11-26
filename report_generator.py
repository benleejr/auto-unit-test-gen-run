from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf_report(data, filename):
    # Create a PDF document
    pdf_doc = SimpleDocTemplate(filename, pagesize=letter)
    
    # Create a list to hold the document elements
    elements = []
    
    max_table_width = 468
    row_height = 30

    # Add data and styles to the elements list
    for i, table_data in enumerate(data):
        # Extract the title, headings, and table entries
        table_title = table_data[0]
        table_headings = table_data[1]
        table_entries = table_data[2:]
        
        # Create the table and set style
        table = Table([table_headings] + table_entries, colWidths=None, splitByRow=True)
        style = TableStyle([('WORDWRAP', (0, 0), (-1, -1), True),
                            ('BACKGROUND', (0, 0), (-1, 0), colors.cyan),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                            ('ALIGN', (0, 0), (-2, -2), 'CENTER'),
                            ('ALIGN', (0, -1), (-1, -1), 'LEFT'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black),
                            ('SPAN', (0, -1), (-1, -1)),
                            ('ROWHEIGHT', (0, 0), (-1, -1), row_height),
                            ])
        table.setStyle(style)
        table.width = max_table_width
        
        # Add the table title and the table to the elements list
        elements.extend([Paragraph(table_title, getSampleStyleSheet()['Heading2']), table])
    
    # Build PDF document
    pdf_doc.build(elements)