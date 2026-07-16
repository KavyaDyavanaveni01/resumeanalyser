import os
from io import BytesIO

from flask import Flask, request, jsonify, send_file

from resume_parser import extract_text
from analyzer import analyze_resume

from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib import colors
from reportlab.lib.units import inch


app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "temp")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =====================================
# HOME ROUTE (Required for Vercel)
# =====================================

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "success",
        "message": "SkillGraph AI Backend is Running Successfully",
        "available_endpoints": [
            "/api/parse",
            "/api/generate-pdf"
        ]
    })


# =====================================
# PARSE RESUME API
# =====================================

@app.route("/api/parse", methods=["POST"])
def parse_resume():

    if "file" not in request.files:
        return jsonify({
            "success": False,
            "error": "No file uploaded."
        }), 400

    file = request.files["file"]
    career_goal = request.form.get("career_goal", "").strip()

    if file.filename == "":
        return jsonify({
            "success": False,
            "error": "Please select a resume file."
        }), 400

    if not career_goal:
        return jsonify({
            "success": False,
            "error": "Career goal is required."
        }), 400

    temp_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    try:

        # Save uploaded file
        file.save(temp_path)

        # Extract resume text
        resume_text = extract_text(temp_path)

        if not resume_text.strip():
            return jsonify({
                "success": False,
                "error": "Unable to extract text from resume."
            }), 400

        # Analyze resume
        analysis = analyze_resume(
            resume_text,
            career_goal
        )

        # Include preview of parsed text
        analysis["parsed_text"] = (
            resume_text[:1000] + "..."
            if len(resume_text) > 1000
            else resume_text
        )

        analysis["success"] = True

        return jsonify(analysis), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

    finally:

        if os.path.exists(temp_path):
            os.remove(temp_path)
            # =====================================
# GENERATE PDF API
# =====================================

@app.route("/api/generate-pdf", methods=["POST"])
def generate_pdf():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "No JSON data received."
        }), 400

    try:

        pdf_buffer = build_pdf(data)

        return send_file(
            pdf_buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="SkillGraph_AI_Report.pdf"
        )

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# =====================================
# PDF BUILDER
# =====================================

def build_pdf(data):

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

    styles = getSampleStyleSheet()

    primary_color = colors.HexColor("#1A365D")
    secondary_color = colors.HexColor("#2B6CB0")
    accent_color = colors.HexColor("#319795")
    text_color = colors.HexColor("#2D3748")
    bg_light = colors.HexColor("#F7FAFC")

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=24,
        textColor=primary_color,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        "SubtitleStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        textColor=accent_color,
        spaceAfter=25
    )

    h1_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        textColor=primary_color,
        spaceBefore=18,
        spaceAfter=8,
        borderColor=accent_color,
        borderWidth=0.5,
        borderPadding=4
    )

    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        textColor=text_color,
        leading=13,
        spaceAfter=8
    )

    header_style = ParagraphStyle(
        "HeaderStyle",
        parent=body_style,
        fontName="Helvetica-Bold",
        textColor=colors.white
    )

    # ==========================
    # TITLE
    # ==========================

    story.append(
        Paragraph(
            "SKILLGRAPH AI",
            title_style
        )
    )

    story.append(
        Paragraph(
            "RESUME SKILL GAP & CAREER ROADMAP ANALYSIS REPORT",
            subtitle_style
        )
    )

    story.append(Spacer(1, 15))

    # ==========================
    # PROFILE SUMMARY
    # ==========================

    profile_data = [

        [
            Paragraph("<b>Candidate Name</b>", body_style),
            Paragraph(data.get("full_name", ""), body_style)
        ],

        [
            Paragraph("<b>Email</b>", body_style),
            Paragraph(data.get("email", ""), body_style)
        ],

        [
            Paragraph("<b>Career Goal</b>", body_style),
            Paragraph(data.get("career_goal", ""), body_style)
        ],

        [
            Paragraph("<b>Match Percentage</b>", body_style),
            Paragraph(
                f"{data.get('match_percentage',0)}%",
                body_style
            )
        ]

    ]

    profile_table = Table(
        profile_data,
        colWidths=[2 * inch, 4.5 * inch]
    )

    profile_table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, -1), bg_light),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 8)

        ])

    )

    story.append(profile_table)

    story.append(Spacer(1, 20))
        # =====================================
    # SKILLS GAP ANALYSIS
    # =====================================

    story.append(Paragraph("Skills Gap Analysis", h1_style))

    story.append(
        Paragraph(
            f"We analyzed your resume for the career goal <b>{data.get('career_goal','')}</b>.",
            body_style
        )
    )

    story.append(Spacer(1, 10))

    extracted_skills = ", ".join(
        data.get("extracted_skills", [])
    ) or "No skills detected"

    missing_skills = ", ".join(
        data.get("missing_skills", [])
    ) or "No missing skills"

    skills_table = Table(

        [

            [
                Paragraph("<b>Matched Skills</b>", body_style),
                Paragraph(extracted_skills, body_style)
            ],

            [
                Paragraph("<b>Missing Skills</b>", body_style),
                Paragraph(missing_skills, body_style)
            ]

        ],

        colWidths=[2 * inch, 4.5 * inch]

    )

    skills_table.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#EDF2F7")),
            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
            ("PADDING", (0,0), (-1,-1), 8)

        ])

    )

    story.append(skills_table)

    story.append(Spacer(1,20))


    # =====================================
    # LEARNING ROADMAP
    # =====================================

    story.append(
        Paragraph(
            "Personalized Learning Roadmap",
            h1_style
        )
    )

    roadmap = data.get("learning_roadmap", [])

    if roadmap:

        roadmap_table = [

            [

                Paragraph("<b>Milestone</b>", header_style),
                Paragraph("<b>Skill</b>", header_style),
                Paragraph("<b>Description</b>", header_style)

            ]

        ]

        for item in roadmap:

            roadmap_table.append([

                Paragraph(
                    item.get("milestone",""),
                    body_style
                ),

                Paragraph(
                    item.get("skill",""),
                    body_style
                ),

                Paragraph(
                    item.get("description",""),
                    body_style
                )

            ])

        table = Table(

            roadmap_table,

            colWidths=[1.4*inch,1.5*inch,3.6*inch]

        )

        table.setStyle(

            TableStyle([

                ("BACKGROUND",(0,0),(-1,0),primary_color),
                ("TEXTCOLOR",(0,0),(-1,0),colors.white),
                ("GRID",(0,0),(-1,-1),0.5,colors.grey),
                ("PADDING",(0,0),(-1,-1),6),
                ("VALIGN",(0,0),(-1,-1),"TOP")

            ])

        )

        story.append(table)

    else:

        story.append(

            Paragraph(

                "Congratulations! No additional learning roadmap is required.",

                body_style

            )

        )

    story.append(Spacer(1,20))


    # =====================================
    # CERTIFICATIONS
    # =====================================

    story.append(

        Paragraph(

            "Recommended Certifications",

            h1_style

        )

    )

    certifications = data.get("certifications", [])

    if certifications:

        cert_table = [

            [

                Paragraph("<b>Skill</b>", header_style),

                Paragraph("<b>Certification</b>", header_style)

            ]

        ]

        for cert in certifications:

            cert_table.append([

                Paragraph(

                    cert.get("skill",""),

                    body_style

                ),

                Paragraph(

                    cert.get("certification",""),

                    body_style

                )

            ])

        table = Table(

            cert_table,

            colWidths=[2.2*inch,4.3*inch]

        )

        table.setStyle(

            TableStyle([

                ("BACKGROUND",(0,0),(-1,0),secondary_color),
                ("TEXTCOLOR",(0,0),(-1,0),colors.white),
                ("GRID",(0,0),(-1,-1),0.5,colors.grey),
                ("PADDING",(0,0),(-1,-1),6),
                ("VALIGN",(0,0),(-1,-1),"TOP")

            ])

        )

        story.append(table)

    else:

        story.append(

            Paragraph(

                "No certifications available.",

                body_style

            )

        )

    story.append(Spacer(1,20))


    # =====================================
    # FOOTER
    # =====================================

    story.append(

        Paragraph(

            "<b>Generated by SkillGraph AI</b>",

            body_style

        )

    )

    story.append(

        Paragraph(

            "Thank you for using SkillGraph AI. Keep learning and keep growing!",

            body_style

        )

    )


    # =====================================
    # BUILD PDF
    # =====================================

    doc.build(story)

    buffer.seek(0)

    return buffer


# =====================================
# MAIN
# =====================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )