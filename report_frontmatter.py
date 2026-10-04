import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from table_utils import format_table, set_cell_background, set_cell_margins

def create_report():
    doc = docx.Document()
    
    # Page setup - 1 inch margins all around
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        
    def add_p(text="", style='Normal', align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=6, line_spacing=1.15, bold=False, italic=False, font_size=12, color=(0,0,0)):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        if text:
            run = p.add_run(text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(font_size)
            run.font.bold = bold
            run.font.italic = italic
            run.font.color.rgb = RGBColor(*color)
        return p

    def add_h1(title, space_before=14, space_after=6):
        return add_p(title, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=space_before, space_after=space_after, bold=True, font_size=14, color=(17, 24, 39))

    def add_h2(title, space_before=10, space_after=4):
        return add_p(title, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=space_before, space_after=space_after, bold=True, font_size=12.5, color=(31, 41, 55))

    def add_h3(title, space_before=8, space_after=3):
        return add_p(title, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=space_before, space_after=space_after, bold=True, italic=True, font_size=12, color=(55, 65, 81))

    def add_bullet(text, bold_prefix="", space_after=4):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r1 = p.add_run(bold_prefix)
            r1.font.name = 'Times New Roman'
            r1.font.size = Pt(12)
            r1.font.bold = True
            r1.font.color.rgb = RGBColor(17, 24, 39)
        r2 = p.add_run(text)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(12)
        r2.font.color.rgb = RGBColor(31, 41, 55)
        return p

    def add_fig(img_path, caption, desc, width_in=5.8):
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(4)
            p_img.add_run().add_picture(img_path, width=Inches(width_in))
        
        p_cap = add_p(caption, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=4, bold=True, font_size=10.5, color=(31, 41, 55))
        p_desc = add_p(desc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=10, font_size=11, color=(55, 65, 81))
        return p_desc

    def add_tbl_caption(caption):
        return add_p(caption, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=4, bold=True, font_size=10.5, color=(31, 41, 55))

    # =========================================================================
    # FRONT MATTER: PAGE 1 - TITLE PAGE
    # =========================================================================
    add_p("CAMPUS COMPLAINT & MAINTENANCE MANAGEMENT SYSTEM", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=24, space_after=12, bold=True, font_size=18, color=(17, 24, 39))
    add_p("A Mini Project Report submitted as part of the academic requirements for the\n23CS4219 - Software Engineering Laboratory", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=16, italic=True, font_size=12, color=(55, 65, 81))
    
    add_p("BACHELOR OF TECHNOLOGY", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=14, space_after=4, bold=True, font_size=13, color=(17, 24, 39))
    add_p("IN", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=4, bold=True, font_size=12, color=(17, 24, 39))
    add_p("COMPUTER SCIENCE AND ENGINEERING", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=24, bold=True, font_size=13, color=(17, 24, 39))
    
    add_p("Submitted by", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=4, italic=True, font_size=12, color=(75, 85, 99))
    add_p("KARTHIKEYAN GULLIPALLI  ([ROLL NUMBER])", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=20, bold=True, font_size=13, color=(17, 24, 39))
    
    add_p("Under the guidance of", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=4, italic=True, font_size=12, color=(75, 85, 99))
    add_p("[GUIDE NAME]", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=32, bold=True, font_size=13, color=(17, 24, 39))
    
    add_p("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=16, space_after=3, bold=True, font_size=12.5, color=(17, 24, 39))
    add_p("ANIL NEERUKONDA INSTITUTE OF TECHNOLOGY AND SCIENCES", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=3, bold=True, font_size=12.5, color=(17, 24, 39))
    add_p("(UGC AUTONOMOUS)\n(Permanently Affiliated to AU, Approved by AICTE and Accredited by NBA & NAAC with 'A' Grade)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=4, italic=True, font_size=10.5, color=(75, 85, 99))
    add_p("Sangivalasa, Bheemili Mandal, Visakhapatnam Dist. (A.P)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=12, font_size=11, color=(55, 65, 81))
    add_p("2024 – 2028", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=0, bold=True, font_size=12, color=(17, 24, 39))
    
    doc.add_page_break()

    # =========================================================================
    # FRONT MATTER: PAGE 2 - CERTIFICATE
    # =========================================================================
    add_p("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=2, bold=True, font_size=13, color=(17, 24, 39))
    add_p("ANIL NEERUKONDA INSTITUTE OF TECHNOLOGY AND SCIENCES", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2, bold=True, font_size=13, color=(17, 24, 39))
    add_p("(UGC AUTONOMOUS)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2, bold=True, font_size=11, color=(55, 65, 81))
    add_p("(Affiliated to AU, Approved by AICTE and Accredited by NBA & NAAC with 'A' Grade)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2, italic=True, font_size=10.5, color=(75, 85, 99))
    add_p("Sangivalasa, Bheemili Mandal, Visakhapatnam Dist. (A.P)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=28, font_size=11, color=(55, 65, 81))
    
    add_p("CERTIFICATE", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=24, bold=True, font_size=15, color=(17, 24, 39))
    
    cert_text = (
        "This is to certify that the mini project entitled “CAMPUS COMPLAINT & MAINTENANCE MANAGEMENT SYSTEM” "
        "has been successfully completed by the students of the Department of Computer Science and Engineering "
        "during the academic year 2024–2025 as part of the requirements for the 23CS4219 - Software Engineering Laboratory."
    )
    add_p(cert_text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=70, font_size=12, line_spacing=1.35)
    
    # Signature block
    sig_table = doc.add_table(rows=2, cols=2)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_table.rows[0].cells[0].paragraphs[0].text = "Faculty Incharge"
    sig_table.rows[0].cells[1].paragraphs[0].text = "Head of the Department"
    sig_table.rows[1].cells[0].paragraphs[0].text = "[GUIDE NAME]"
    sig_table.rows[1].cells[1].paragraphs[0].text = "Prof. G. Srinivas"
    
    for row in sig_table.rows:
        for idx, cell in enumerate(row.cells):
            cell.width = Inches(3.1)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if idx == 1 else WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(12)
                r.font.bold = True
    sig_table.rows[0].cells[0].paragraphs[0].runs[0].font.bold = True
    sig_table.rows[0].cells[1].paragraphs[0].runs[0].font.bold = True
    
    doc.add_page_break()

    # =========================================================================
    # FRONT MATTER: PAGE 3 - DECLARATION
    # =========================================================================
    add_p("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=2, bold=True, font_size=13, color=(17, 24, 39))
    add_p("ANIL NEERUKONDA INSTITUTE OF TECHNOLOGY AND SCIENCES", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2, bold=True, font_size=13, color=(17, 24, 39))
    add_p("(UGC AUTONOMOUS)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2, bold=True, font_size=11, color=(55, 65, 81))
    add_p("(Affiliated to AU, Approved by AICTE and Accredited by NBA & NAAC with 'A' Grade)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2, italic=True, font_size=10.5, color=(75, 85, 99))
    add_p("Sangivalasa, Bheemili Mandal, Visakhapatnam Dist. (A.P)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=28, font_size=11, color=(55, 65, 81))
    
    add_p("DECLARATION", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=24, bold=True, font_size=15, color=(17, 24, 39))
    
    dec_text = (
        "I, Karthikeyan Gullipalli, of III year, I semester B.Tech., Section – A, in the Department of "
        "Computer Science and Engineering from ANITS, Visakhapatnam, hereby declare that the mini project work entitled "
        "“CAMPUS COMPLAINT & MAINTENANCE MANAGEMENT SYSTEM” is carried out by me and submitted in "
        "Software Engineering Laboratory-23CS4219, at Anil Neerukonda Institute of Technology & Sciences (A) "
        "during the academic year 2024-2025."
    )
    add_p(dec_text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=70, font_size=12, line_spacing=1.35)
    
    dec_table = doc.add_table(rows=1, cols=2)
    dec_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    dec_table.rows[0].cells[0].paragraphs[0].text = "Karthikeyan Gullipalli"
    dec_table.rows[0].cells[1].paragraphs[0].text = "[ROLL NUMBER]"
    for idx, cell in enumerate(dec_table.rows[0].cells):
        cell.width = Inches(3.1)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)
            r.font.bold = True
            
    doc.add_page_break()

    # =========================================================================
    # FRONT MATTER: PAGE 4 - ABSTRACT
    # =========================================================================
    add_p("Abstract", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=16, space_after=18, bold=True, font_size=16, color=(17, 24, 39))
    
    abs1 = (
        "Handling campus infrastructure and maintenance grievances through traditional manual registers or verbal "
        "intimation is highly inefficient, error-prone, and devoid of institutional accountability. Physical registers "
        "are vulnerable to damage, complaints are frequently misdirected or misplaced, maintenance technicians lack "
        "structured work orders, and complainants have zero visibility into repair progress. This mini project resolves "
        "these systemic bottlenecks by designing and implementing a full-stack, web-based Campus Complaint & Maintenance "
        "Management System (CCMS) that digitizes and automates the entire grievance handling lifecycle."
    )
    abs2 = (
        "The system incorporates strict role-based access control (RBAC) across four authenticated user roles: Student, "
        "Faculty, Maintenance Staff, and Administrator. Complainants (Students and Faculty) can lodge categorized grievances "
        "(e.g., Electrical, Plumbing, HVAC, Network, Classroom Furniture) mapped to exact campus buildings, floors, and rooms, "
        "specify urgency levels (Low, Medium, High, Critical), attach evidence images via file upload, track live repair statuses, "
        "and provide satisfaction ratings (1 to 5 stars) upon resolution. Administrators govern the triage workflow through "
        "an administrative dashboard, verifying valid submissions, rejecting frivolous tickets, allocating qualified maintenance "
        "technicians, and managing campus master data. Maintenance personnel operate a dedicated task queue where they accept "
        "assigned work orders, log diagnostic remarks, and mark issues as resolved with timestamped audit records."
    )
    abs3 = (
        "CCMS is architected following an industry-standard three-tier client-server model. The responsive presentation "
        "tier is engineered with React 18, Vite 5, Tailwind CSS, and Axios. The application tier is built with a Node.js "
        "and Express.js REST API featuring JSON Web Token (JWT) stateless authorization, bcryptjs password hashing, "
        "and express-validator sanitization. The data tier leverages a relational MySQL 8 database executing ACID-compliant "
        "parameterized queries across seven normalized tables. The software was engineered following rigorous SE principles, "
        "modeled using Data Flow Diagrams (DFD Levels 0, 1, 2) and comprehensive UML diagrams, and verified through structured "
        "unit, integration, and black-box test suites."
    )
    add_p(abs1, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=10, font_size=12, line_spacing=1.2)
    add_p(abs2, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=10, font_size=12, line_spacing=1.2)
    add_p(abs3, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=14, font_size=12, line_spacing=1.2)
    
    doc.add_page_break()

    # =========================================================================
    # FRONT MATTER: PAGES 5-8 - TOC, LIST OF FIGURES, LIST OF TABLES
    # =========================================================================
    add_p("Table of Contents", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=16, space_after=18, bold=True, font_size=16, color=(17, 24, 39))
    
    toc_items = [
        ("1. Introduction", "1"),
        ("   1.1 Background", "1"),
        ("   1.2 Problem Statement", "1"),
        ("   1.3 Motivation", "1"),
        ("   1.4 Objectives", "2"),
        ("2. Existing System", "2"),
        ("3. Proposed System", "3"),
        ("4. Requirements Specification", "4"),
        ("   4.1 Functional Requirements", "4"),
        ("   4.2 Non-Functional Requirements", "5"),
        ("5. Hardware and Software Requirements", "5"),
        ("   Hardware Requirements", "5"),
        ("   Software Requirements", "6"),
        ("6. Data Flow Diagram", "6"),
        ("   Level 0 DFD (Context Diagram)", "7"),
        ("   Level 1 DFD", "8"),
        ("   Level 2 DFD (Complaint Lodging & Validation)", "9"),
        ("7. System Architecture", "10"),
        ("   Layered System Architecture", "10"),
        ("   Relational Data Model & Entity-Relationship Schema", "11"),
        ("8. Module Description", "12"),
        ("   Module 1: Authentication & Authorization Module", "12"),
        ("   Module 2: Complaint Lodging & Management Module", "12"),
        ("   Module 3: Verification & Administrative Control Module", "13"),
        ("   Module 4: Maintenance Assignment & Resolution Module", "13"),
        ("   Module 5: Feedback & Status Auditing Module", "13"),
        ("   Module 6: Reference Data & System Configuration Module", "14"),
        ("   Summary of Modules and Implementing Files", "14"),
        ("   REST API Endpoints", "15"),
        ("9. System Analysis", "16"),
        ("   9.1 Use Case Diagram", "16"),
        ("   9.2 Use Case Descriptions", "17"),
        ("10. UML Design", "20"),
        ("   10.1 Class Diagram", "20"),
        ("   10.2 Sequence Diagrams", "21"),
        ("   10.3 Activity Diagram", "23"),
        ("   10.4 State Diagram", "24"),
        ("   10.5 Component Diagram", "25"),
        ("   10.6 Deployment Diagram", "26"),
        ("11. Testing", "27"),
        ("   11.1 Test Plan", "27"),
        ("   11.2 Unit Test Results", "28"),
        ("   11.3 Black-Box and System Test Cases", "29"),
        ("12. Results / Screenshots", "31"),
        ("13. Limitations", "36"),
        ("14. Conclusion", "36"),
        ("15. References", "37"),
        ("Appendix", "38"),
        ("   A. Additional Screenshots", "38"),
        ("   B. Sample Inputs and Outputs", "38"),
        ("   C. User Manual", "39")
    ]
    
    toc_table = doc.add_table(rows=len(toc_items), cols=2)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (title, page_no) in enumerate(toc_items):
        r = toc_table.rows[idx]
        r.cells[0].width = Inches(5.5)
        r.cells[1].width = Inches(0.8)
        p0 = r.cells[0].paragraphs[0]
        p1 = r.cells[1].paragraphs[0]
        p0.text = title
        p1.text = page_no
        p0.paragraph_format.space_before = Pt(1)
        p0.paragraph_format.space_after = Pt(1)
        p1.paragraph_format.space_before = Pt(1)
        p1.paragraph_format.space_after = Pt(1)
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        is_major = not title.startswith("   ")
        for run in p0.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11)
            run.font.bold = is_major
        for run in p1.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11)
            run.font.bold = is_major
            
    doc.add_page_break()

    # LIST OF FIGURES
    add_p("List of Figures", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=16, space_after=18, bold=True, font_size=16, color=(17, 24, 39))
    add_p("(All figures carry a unique number and descriptive title that are used consistently throughout the report.)", italic=True, font_size=10.5, color=(107, 114, 128))
    
    figures_list = [
        ("Figure 1: Level 0 DFD (Context Diagram) of the Campus Complaint Management System", "7"),
        ("Figure 2: Level 1 DFD showing the major processes and data stores", "8"),
        ("Figure 3: Level 2 DFD of Process 2.0 (Complaint Registration & Lodging)", "9"),
        ("Figure 4: Layered system architecture of the Campus Complaint Management System", "10"),
        ("Figure 5: Relational data model and entity-relationship schema", "11"),
        ("Figure 6: Use case diagram of the Campus Complaint Management System", "16"),
        ("Figure 7: Class diagram of the Campus Complaint Management System", "20"),
        ("Figure 8: Sequence diagram: Student submits a new complaint", "21"),
        ("Figure 9: Sequence diagram: Administrator verifies and assigns complaint to maintenance staff", "22"),
        ("Figure 10: Activity diagram of the complete complaint lifecycle workflow", "23"),
        ("Figure 11: State diagram of a complaint lifecycle", "24"),
        ("Figure 12: Component diagram of the Campus Complaint Management System", "25"),
        ("Figure 13: Deployment diagram of the Campus Complaint Management System", "26"),
        ("Figure 14: Login page showing role-based authentication and demo credentials", "31"),
        ("Figure 15: User registration page for student and faculty onboarding", "31"),
        ("Figure 16: Student dashboard with status summary cards and recent complaints", "32"),
        ("Figure 17: File a new complaint form with category, location, and priority selection", "32"),
        ("Figure 18: Student complaints tracking list with search and status badges", "33"),
        ("Figure 19: Student complaint detail view with audit trail and feedback form", "33"),
        ("Figure 20: Administrator dashboard with system-wide analytics and metric cards", "34"),
        ("Figure 21: Administrator complaints management table with filters and search", "34"),
        ("Figure 22: Administrator complaint detail view with verification and staff assignment", "35"),
        ("Figure 23: Administrator users management page with active status toggling", "35"),
        ("Figure 24: Administrator categories management page", "36"),
        ("Figure 25: Administrator locations management page", "36"),
        ("Figure 26: Administrator assignments tracking page", "36"),
        ("Figure 27: Maintenance staff dashboard with task counters", "37"),
        ("Figure 28: Maintenance staff assigned tasks table with progress actions", "37"),
        ("Figure 29: Maintenance task detail view with status update and work remarks form", "37")
    ]
    
    fig_table = doc.add_table(rows=len(figures_list), cols=2)
    fig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (title, page_no) in enumerate(figures_list):
        r = fig_table.rows[idx]
        r.cells[0].width = Inches(5.6)
        r.cells[1].width = Inches(0.7)
        p0 = r.cells[0].paragraphs[0]
        p1 = r.cells[1].paragraphs[0]
        p0.text = title
        p1.text = page_no
        p0.paragraph_format.space_before = Pt(1)
        p0.paragraph_format.space_after = Pt(1)
        p1.paragraph_format.space_before = Pt(1)
        p1.paragraph_format.space_after = Pt(1)
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        for run in p0.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10.5)
        for run in p1.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10.5)

    doc.add_page_break()

    # LIST OF TABLES
    add_p("List of Tables", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=16, space_after=18, bold=True, font_size=16, color=(17, 24, 39))
    
    tables_list = [
        ("Table 1: Non-Functional Requirements", "5"),
        ("Table 2: Hardware Requirements", "5"),
        ("Table 3: Software Requirements", "6"),
        ("Table 4: Summary of Modules and Implementing Files", "14"),
        ("Table 5: REST API Endpoints", "15"),
        ("Table 6: Use Case Description: User Registration and Login (UC01)", "17"),
        ("Table 7: Use Case Description: Submit Complaint (UC02)", "17"),
        ("Table 8: Use Case Description: Track Own Complaints (UC03)", "18"),
        ("Table 9: Use Case Description: Verify or Reject Complaint (UC06)", "18"),
        ("Table 10: Use Case Description: Assign Complaint to Staff (UC07)", "19"),
        ("Table 11: Use Case Description: Execute and Resolve Task (UC11 & UC12)", "19"),
        ("Table 12: Testing Techniques Applied", "27"),
        ("Table 13: Independent Paths of State Transition Validation", "27"),
        ("Table 14: Unit Test Cases and Results", "28"),
        ("Table 15: Black-Box and System Test Cases", "29"),
        ("Table 16: Sample Complaint Audit History Record", "38"),
        ("Table 17: Sample API Request and Response (Submit Complaint)", "39")
    ]
    
    tbl_list_table = doc.add_table(rows=len(tables_list), cols=2)
    tbl_list_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (title, page_no) in enumerate(tables_list):
        r = tbl_list_table.rows[idx]
        r.cells[0].width = Inches(5.6)
        r.cells[1].width = Inches(0.7)
        p0 = r.cells[0].paragraphs[0]
        p1 = r.cells[1].paragraphs[0]
        p0.text = title
        p1.text = page_no
        p0.paragraph_format.space_before = Pt(1)
        p0.paragraph_format.space_after = Pt(1)
        p1.paragraph_format.space_before = Pt(1)
        p1.paragraph_format.space_after = Pt(1)
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        for run in p0.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10.5)
        for run in p1.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10.5)

    doc.add_page_break()

    print("Front matter generated successfully. Now generating main chapters...")
    return doc

print("Main template script skeleton ready.")
