import os
from flask import Flask, request, jsonify, send_file
from resume_parser import extract_text
from analyzer import analyze_resume
from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'temp')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/parse', methods=['POST'])
def parse_resume():
    """
    Parses a resume and performs skill gap analysis.
    Expected Form Data:
    - file: The PDF/DOCX file
    - career_goal: The target job title
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    career_goal = request.form.get('career_goal', '').strip()
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    if not career_goal:
        return jsonify({"error": "No career goal provided"}), 400
    
    # Save file temporarily
    filename = file.filename
    temp_path = os.path.join(UPLOAD_FOLDER, filename)
    try:
        file.save(temp_path)
        
        # 1. Extract Text
        text = extract_text(temp_path)
        
        # 2. Analyze Skills Gap
        analysis = analyze_resume(text, career_goal)
        analysis['parsed_text'] = text[:1000] + "..." if len(text) > 1000 else text # Limit cached text in response
        
        return jsonify(analysis)
    
    except Exception as e:
        return jsonify({"error": f"Error parsing resume: {str(e)}"}), 500
    
    finally:
        # Cleanup temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.route('/api/generate-pdf', methods=['POST'])
def generate_pdf():
    """
    Generates a PDF report using ReportLab from JSON analysis details.
    """
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        pdf_buffer = build_pdf(data)
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='SkillGraph_AI_Report.pdf'
        )
    except Exception as e:
        return jsonify({"error": f"Failed to generate PDF: {str(e)}"}), 500

def build_pdf(data):
    """
    ReportLab PDF Generation.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    story = []
    
    # Custom styles
    styles = getSampleStyleSheet()
    
    # Curated modern primary color palette
    primary_color = colors.HexColor("#1A365D")  # Deep Slate Navy
    secondary_color = colors.HexColor("#2B6CB0") # Modern Indigo
    accent_color = colors.HexColor("#319795")    # Teal Accent
    text_color = colors.HexColor("#2D3748")      # Charcoal Body Text
    bg_light = colors.HexColor("#F7FAFC")        # Warm Off-White
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        textColor=primary_color,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=accent_color,
        spaceAfter=25
    )
    
    h1_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        textColor=primary_color,
        spaceBefore=18,
        spaceAfter=8,
        borderColor=accent_color,
        borderWidth=0.5,
        borderRadius=2,
        borderPadding=4
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=text_color,
        spaceAfter=8,
        leading=13
    )

    header_text_style = ParagraphStyle(
        'HeaderText',
        parent=body_style,
        textColor=colors.white,
        fontName='Helvetica-Bold'
    )

    # 1. Header Header
    story.append(Paragraph("SKILLGRAPH AI", title_style))
    story.append(Paragraph("RESUME SKILL GAP & CAREER ROADMAP ANALYSIS REPORT", subtitle_style))
    
    # 2. User Profile Summary
    profile_data = [
        [Paragraph("<b>Candidate Name:</b>", body_style), Paragraph(data.get("full_name", ""), body_style)],
        [Paragraph("<b>Email Address:</b>", body_style), Paragraph(data.get("email", ""), body_style)],
        [Paragraph("<b>Target Career Goal:</b>", body_style), Paragraph(data.get("career_goal", ""), body_style)],
        [Paragraph("<b>Career Match Score:</b>", body_style), Paragraph(f"<b>{data.get('match_percentage', 0.0)}%</b>", body_style)]
    ]
    t = Table(profile_data, colWidths=[2.0*inch, 4.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_light),
        ('PADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))
    
    # 3. Skills Extracted vs Gaps
    story.append(Paragraph("Skills Gap Analysis", h1_style))
    story.append(Paragraph(f"We scanned your resume and identified skills matching or missing for the role of <b>{data.get('career_goal')}</b>.", body_style))
    story.append(Spacer(1, 8))
    
    found_skills_str = ", ".join(data.get("extracted_skills", [])) if data.get("extracted_skills") else "None detected"
    missing_skills_str = ", ".join(data.get("missing_skills", [])) if data.get("missing_skills") else "None! You possess a complete skillset."
    
    skills_data = [
        [Paragraph("<b>Matched Skills</b>", body_style), Paragraph(found_skills_str, body_style)],
        [Paragraph("<b>Missing Skills (Gap)</b>", body_style), Paragraph(missing_skills_str, body_style)]
    ]
    t_skills = Table(skills_data, colWidths=[2.0*inch, 4.5*inch])
    t_skills.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#EDF2F7")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
    ]))
    story.append(t_skills)
    story.append(Spacer(1, 15))
    
    # 4. Roadmap
    story.append(Paragraph("Personalized Learning Roadmap", h1_style))
    roadmap_list = data.get("learning_roadmap", [])
    if not roadmap_list:
        story.append(Paragraph("Congratulations! You possess all required skills for this career goal.", body_style))
    else:
        story.append(Paragraph("Follow this structured roadmap to bridge your missing skills:", body_style))
        story.append(Spacer(1, 8))
        
        roadmap_data = [[
            Paragraph("Milestone", header_text_style), 
            Paragraph("Skill", header_text_style), 
            Paragraph("Learning Objectives", header_text_style)
        ]]
        for item in roadmap_list:
            roadmap_data.append([
                Paragraph(item.get("milestone", ""), body_style),
                Paragraph(item.get("skill", ""), body_style),
                Paragraph(item.get("description", ""), body_style)
            ])
        t_roadmap = Table(roadmap_data, colWidths=[1.3*inch, 1.4*inch, 3.8*inch])
        t_roadmap.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), primary_color),
            ('PADDING', (0,0), (-1,-1), 6),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ]))
        story.append(t_roadmap)
        
    story.append(Spacer(1, 15))
    
    # 5. Certifications
    story.append(Paragraph("Recommended Certifications", h1_style))
    certs_list = data.get("certifications", [])
    if not certs_list:
        story.append(Paragraph("No certifications recommended at this stage.", body_style))
    else:
        story.append(Paragraph("Industry certifications recommended to validate your skills:", body_style))
        story.append(Spacer(1, 8))
        
        certs_data = [[
            Paragraph("Target Skill", header_text_style), 
            Paragraph("Recommended Certification Program", header_text_style)
        ]]
        for item in certs_list:
            certs_data.append([
                Paragraph(item.get("skill", ""), body_style),
                Paragraph(item.get("certification", ""), body_style)
            ])
        t_certs = Table(certs_data, colWidths=[2.2*inch, 4.3*inch])
        t_certs.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), secondary_color),
            ('PADDING', (0,0), (-1,-1), 6),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ]))
        story.append(t_certs)

    doc.build(story)
    buffer.seek(0)
    return buffer

if __name__ == '__main__':
    app.run(port=5000, debug=True)
