import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from table_utils import format_table, set_cell_background, set_cell_margins

def build_complete_report():
    doc = docx.Document()
    
    # 1-inch margins
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        
    def add_p(text="", align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, line_spacing=1.15, bold=False, italic=False, font_size=12, color=(0,0,0)):
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

    def add_h1(title, space_before=16, space_after=6):
        return add_p(title, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=space_before, space_after=space_after, bold=True, font_size=14, color=(17, 24, 39))

    def add_h2(title, space_before=12, space_after=4):
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

    def add_fig(img_path, caption, desc, width_in=5.6):
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(10)
            p_img.paragraph_format.space_after = Pt(4)
            p_img.add_run().add_picture(img_path, width=Inches(width_in))
        else:
            p_ph = doc.add_paragraph()
            p_ph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_ph.paragraph_format.space_before = Pt(8)
            p_ph.paragraph_format.space_after = Pt(4)
            r = p_ph.add_run(f"[ Image: {os.path.basename(img_path)} ]")
            r.font.name = 'Times New Roman'
            r.font.italic = True
            r.font.color.rgb = RGBColor(156, 163, 175)
            
        add_p(caption, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=4, bold=True, font_size=10.5, color=(31, 41, 55))
        add_p(desc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=10, font_size=11, color=(55, 65, 81))

    def add_tbl_caption(caption):
        return add_p(caption, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=4, bold=True, font_size=10.5, color=(31, 41, 55))

    # =========================================================================
    # 1. FRONT MATTER: TITLE PAGE
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
    # 2. CERTIFICATE
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
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(12)
                r.font.bold = True
    
    doc.add_page_break()

    # =========================================================================
    # 3. DECLARATION
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
    # 4. ABSTRACT
    # =========================================================================
    add_p("Abstract", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=16, space_after=18, bold=True, font_size=16, color=(17, 24, 39))
    
    add_p(
        "Handling campus infrastructure and maintenance grievances through traditional manual registers or verbal "
        "intimation is highly inefficient, error-prone, and devoid of institutional accountability. Physical registers "
        "are vulnerable to damage, complaints are frequently misdirected or misplaced, maintenance technicians lack "
        "structured work orders, and complainants have zero visibility into repair progress. This mini project resolves "
        "these systemic bottlenecks by designing and implementing a full-stack, web-based Campus Complaint & Maintenance "
        "Management System (CCMS) that digitizes and automates the entire grievance handling lifecycle.",
        space_after=10
    )
    add_p(
        "The system incorporates strict role-based access control (RBAC) across four authenticated user roles: Student, "
        "Faculty, Maintenance Staff, and Administrator. Complainants (Students and Faculty) can lodge categorized grievances "
        "(e.g., Electrical, Plumbing, HVAC, Network, Classroom Furniture) mapped to exact campus buildings, floors, and rooms, "
        "specify urgency levels (Low, Medium, High, Critical), attach evidence images via file upload, track live repair statuses, "
        "and provide satisfaction ratings (1 to 5 stars) upon resolution. Administrators govern the triage workflow through "
        "an administrative dashboard, verifying valid submissions, rejecting frivolous tickets, allocating qualified maintenance "
        "technicians, and managing campus master data. Maintenance personnel operate a dedicated task queue where they accept "
        "assigned work orders, log diagnostic remarks, and mark issues as resolved with timestamped audit records.",
        space_after=10
    )
    add_p(
        "CCMS is architected following an industry-standard three-tier client-server model. The responsive presentation "
        "tier is engineered with React 18, Vite 5, Tailwind CSS, and Axios. The application tier is built with a Node.js "
        "and Express.js REST API featuring JSON Web Token (JWT) stateless authorization, bcryptjs password hashing, "
        "and express-validator sanitization. The data tier leverages a relational MySQL 8 database executing ACID-compliant "
        "parameterized queries across seven normalized tables. The software was engineered following rigorous SE principles, "
        "modeled using Data Flow Diagrams (DFD Levels 0, 1, 2) and comprehensive UML diagrams, and verified through structured "
        "unit, integration, and black-box test suites.",
        space_after=14
    )
    
    doc.add_page_break()

    # =========================================================================
    # 5. TABLE OF CONTENTS, LIST OF FIGURES, LIST OF TABLES
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
        p0, p1 = r.cells[0].paragraphs[0], r.cells[1].paragraphs[0]
        p0.text, p1.text = title, page_no
        p0.paragraph_format.space_before = p0.paragraph_format.space_after = Pt(1)
        p1.paragraph_format.space_before = p1.paragraph_format.space_after = Pt(1)
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        is_maj = not title.startswith("   ")
        for run in p0.runs: run.font.name = 'Times New Roman'; run.font.size = Pt(11); run.font.bold = is_maj
        for run in p1.runs: run.font.name = 'Times New Roman'; run.font.size = Pt(11); run.font.bold = is_maj

    doc.add_page_break()

    # LIST OF FIGURES
    add_p("List of Figures", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=16, space_after=18, bold=True, font_size=16, color=(17, 24, 39))
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
        p0, p1 = r.cells[0].paragraphs[0], r.cells[1].paragraphs[0]
        p0.text, p1.text = title, page_no
        p0.paragraph_format.space_before = p0.paragraph_format.space_after = Pt(1)
        p1.paragraph_format.space_before = p1.paragraph_format.space_after = Pt(1)
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        for run in p0.runs: run.font.name = 'Times New Roman'; run.font.size = Pt(10.5)
        for run in p1.runs: run.font.name = 'Times New Roman'; run.font.size = Pt(10.5)

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
        p0, p1 = r.cells[0].paragraphs[0], r.cells[1].paragraphs[0]
        p0.text, p1.text = title, page_no
        p0.paragraph_format.space_before = p0.paragraph_format.space_after = Pt(1)
        p1.paragraph_format.space_before = p1.paragraph_format.space_after = Pt(1)
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        for run in p0.runs: run.font.name = 'Times New Roman'; run.font.size = Pt(10.5)
        for run in p1.runs: run.font.name = 'Times New Roman'; run.font.size = Pt(10.5)

    doc.add_page_break()

    # =========================================================================
    # 1. INTRODUCTION
    # =========================================================================
    add_h1("1. Introduction")
    
    add_h2("1.1 Background")
    add_p(
        "A modern educational campus comprises expansive academic blocks, specialized computer and science laboratories, "
        "library complexes, residential student hostels, administrative offices, and amenities. Ensuring continuous operational "
        "readiness across these diverse facilities demands prompt maintenance of electrical installations, sanitary plumbing, "
        "networking infrastructure, laboratory instruments, and classroom furniture. In typical institutions, maintenance requests "
        "have historically been collected through localized physical logbooks stationed at departmental offices, hostels, or estate "
        "management desks. Alternatively, issues are communicated verbally or through fragmented email exchanges. While seemingly "
        "simple, this manual paradigm fails rapidly as campus scale increases, resulting in administrative oversight, delayed repairs, "
        "and widespread student dissatisfaction."
    )
    add_p(
        "Recent advances in full-stack web engineering and open-source database technologies empower institutions to replace "
        "disorganized manual procedures with robust, centralized digital portals. By utilizing decoupled client-server web architectures, "
        "institutions can deploy responsive interfaces that operate universally across desktop and mobile browsers while enforcing "
        "strict data validation and transactional integrity on server-side databases. The Campus Complaint & Maintenance Management System "
        "(CCMS) applies modern software engineering methodologies to engineer a unified, transparent, and role-governed platform "
        "tailored specifically to institutional maintenance operations."
    )

    add_h2("1.2 Problem Statement")
    add_p(
        "The traditional manual method of campus grievance handling is characterized by several severe operational liabilities:"
    )
    add_bullet("Physical paper registers are prone to physical wear, misplacement, illegibility, and unauthorized tampering.", "1. Physical Vulnerability: ")
    add_bullet("Complainants receive no formal confirmation or tracking reference, leaving them uninformed regarding repair scheduling or progress.", "2. Lack of Status Tracking: ")
    add_bullet("Supervisors cannot readily assess staff workload, identify recurring equipment failures, or verify whether reported issues are genuine.", "3. Absence of Accountability: ")
    add_bullet("Work orders are communicated informally without clear location specifics, leading technicians to search aimlessly for fault sites.", "4. Inefficient Task Dispatching: ")
    add_bullet("Extracting historical maintenance logs, response times, or department-wise issue frequencies requires days of tedious manual data collation.", "5. Infeasible Historical Auditing: ")
    add_p(
        "There is consequently an urgent imperative for a secure, responsive, and centralized web-based platform that records "
        "complaints once with granular location and category context, tracks their transition through an explicit finite state machine, "
        "and provides appropriate administrative oversight and resolution feedback."
    )

    add_h2("1.3 Motivation")
    add_p(
        "This project was undertaken because infrastructure maintenance directly impacts the daily academic and living conditions "
        "of thousands of students and faculty members. Developing a practical solution offers substantial institutional utility while "
        "serving as an exemplary case study for the Software Engineering Laboratory (23CS4219). It provides an ideal domain to apply "
        "the full software development lifecycle: formal requirements specification, structured data-flow modeling, object-oriented UML "
        "design, database normalization, asynchronous REST API engineering, role-based access control, and systematic verification testing."
    )

    add_h2("1.4 Objectives")
    add_p("The primary engineering objectives of the Campus Complaint & Maintenance Management System are:")
    add_bullet("To eliminate physical paper registers by digitizing the complete complaint lodging and tracking lifecycle.", "1. Centralized Digitization: ")
    add_bullet("To implement role-based access control (RBAC) supporting Students, Faculty, Maintenance Staff, and Administrators.", "2. Role-Based Access Control: ")
    add_bullet("To enforce an explicit, audited complaint finite state machine: NEW → VERIFIED → ASSIGNED → IN_PROGRESS → RESOLVED → CLOSED.", "3. Structured State Machine: ")
    add_bullet("To enable structured classification of complaints by campus building, floor, room number, category, and severity.", "4. Granular Categorization: ")
    add_bullet("To provide maintenance technicians with a dedicated task queue for accepting assignments and submitting repair remarks.", "5. Streamlined Work Orders: ")
    add_bullet("To empower students to monitor live progress, inspect chronological audit updates, and submit quality feedback ratings.", "6. Complainant Transparency: ")
    add_bullet("To equip campus administrators with real-time analytics covering ticket volumes, category breakdowns, and critical open hazards.", "7. Administrative Governance: ")

    # =========================================================================
    # 2. EXISTING SYSTEM
    # =========================================================================
    add_h1("2. Existing System")
    add_p(
        "In the conventional campus operational model, when a student or faculty member encounters a maintenance issue—such as "
        "a damaged classroom ceiling fan, a leaking washroom valve, or a non-functioning laboratory LAN node—they must physically visit "
        "a department office or estate caretaker desk to record the grievance in a physical register. The register typically captures "
        "only the date, the complainant's signature, and a brief handwritten note. Periodically, an administrative supervisor reviews "
        "the entries, transcribes the notes, and verbally communicates tasks to campus maintenance technicians or outsourced contractors."
    )
    add_p("The critical drawbacks of this existing manual approach include:")
    add_bullet("Students spend valuable lecture and study intervals traveling to administrative offices to lodge simple repair requests.", "• Time Inefficiency: ")
    add_bullet("Handwritten entries are frequently vague, lacking floor or room numbers, leading to technicians repairing the wrong apparatus.", "• Ambiguity & Errors: ")
    add_bullet("The complainant has no mechanism to determine whether a complaint was read, approved, assigned, or dismissed.", "• Zero Visibility: ")
    add_bullet("Maintenance staff cannot be audited regarding when they received a ticket, when they arrived on-site, or what materials were utilized.", "• Lack of Performance Tracking: ")
    add_bullet("Pages tore out, water damage, or lost books result in complete erasure of institutional infrastructure history.", "• Data Insecurity: ")
    add_bullet("Anyone who accesses the physical counter can inspect or tamper with recorded complaint entries.", "• Total Absence of Access Control: ")

    # =========================================================================
    # 3. PROPOSED SYSTEM
    # =========================================================================
    add_h1("3. Proposed System")
    add_p(
        "The proposed Campus Complaint & Maintenance Management System (CCMS) is an end-to-end, multi-tier web application "
        "designed to provide an intuitive, transparent, and structured environment for managing campus infrastructure. "
        "The system coordinates activities across four distinct user roles through tailored interfaces:"
    )
    add_bullet("Can self-register, securely log in, and file new complaints by choosing from standardized categories and pre-configured campus locations (Building, Floor, Room). They can assign an initial priority, attach an evidence photograph, view live status progression, inspect timestamped status remarks, reopen unresolved complaints, and submit satisfaction ratings (1–5 stars) upon resolution.", "• Complainant (Student / Faculty): ")
    add_bullet("Operates an administrative control center with complete visibility over all institutional complaints. The administrator reviews new tickets, verifies authenticity or rejects out-of-scope requests, allocates specific maintenance staff members with work instructions, closes satisfactorily resolved tickets, and administers reference master data (categories, campus locations, user accounts).", "• Administrator: ")
    add_bullet("Accesses a focused task management board displaying tickets specifically assigned to them. Staff members can accept tickets (moving status to IN_PROGRESS), perform physical remediation, log technical remarks detailing work done, and submit tickets as RESOLVED.", "• Maintenance Technician: ")
    add_p(
        "Every status transition is governed by an automated state transition engine that enforces valid progression and "
        "automatically writes an immutable record to the complaint_updates table, capturing the actor ID, previous status, "
        "new status, remarks, and exact timestamp. All network exchanges are secured via JWT tokens, ensuring complete data "
        "privacy and strict role enforcement."
    )

    # =========================================================================
    # 4. REQUIREMENTS SPECIFICATION
    # =========================================================================
    add_h1("4. Requirements Specification")
    
    add_h2("4.1 Functional Requirements")
    add_p("The functional requirements implemented in CCMS are defined as follows:")
    add_bullet("The system shall provide registration for students and faculty, and secure email/password login returning a signed JWT token.", "FR01 - User Authentication: ")
    add_bullet("The system shall enforce role-based access restricting administrative endpoints to ADMIN and task execution to MAINTENANCE staff.", "FR02 - Role Authorization: ")
    add_bullet("Students and Faculty shall be able to create complaints specifying title, category, location, priority, description, and optional evidence image.", "FR03 - Complaint Lodging: ")
    add_bullet("The system shall generate a unique, human-readable complaint identifier formatted as CMP-YYYYMMDD-XXXXXX upon submission.", "FR04 - Unique Tracking ID: ")
    add_bullet("Complainants shall be able to view their complete history of raised complaints, filter by status, and search by title or tracking code.", "FR05 - Student Tracking: ")
    add_bullet("Administrators shall view a global table of complaints, filter by category, priority, or lifecycle status, and inspect full details.", "FR06 - Admin Triage: ")
    add_bullet("Administrators shall verify valid NEW complaints (moving status to VERIFIED) or reject frivolous submissions (moving to REJECTED).", "FR07 - Ticket Verification: ")
    add_bullet("Administrators shall assign VERIFIED complaints to active maintenance staff members, capturing assignment notes.", "FR08 - Staff Allocation: ")
    add_bullet("Maintenance staff shall view their personal task queue, update status to IN_PROGRESS, and mark tickets as RESOLVED with remarks.", "FR09 - Task Execution: ")
    add_bullet("Administrators shall close satisfactorily resolved complaints (moving to CLOSED), or complainants may reopen issues if unresolved.", "FR10 - Closure & Reopening: ")
    add_bullet("Complainants shall be able to submit a rating (1 to 5) and feedback commentary once a complaint reaches RESOLVED or CLOSED status.", "FR11 - Complainant Feedback: ")
    add_bullet("Administrators shall create, update, and soft-delete categories, campus locations (building/floor/room), and deactivate user accounts.", "FR12 - Master Data Management: ")
    add_bullet("Administrators and users shall view role-tailored dashboard metric counters showing total, pending, in-progress, and resolved counts.", "FR13 - Real-Time Metrics: ")

    add_h2("4.2 Non-Functional Requirements")
    add_tbl_caption("Table 1: Non-Functional Requirements")
    
    nfr_headers = ["Requirement", "Specification & Implementation Strategy"]
    nfr_data = [
        ["Performance", "REST API response times remain under 200ms for standard database queries; React client utilizes client-side routing and lazy component loading to achieve sub-second view rendering."],
        ["Security", "User passwords are encrypted using bcryptjs with 10 salt rounds; stateless API communication is authenticated via signed JWT tokens (HS256); parameterized SQL queries prevent SQL injection."],
        ["Usability", "Modern, accessible UI styled with Tailwind CSS; provides clear status badges, responsive layout across screen resolutions, and contextual error alerts for failed operations."],
        ["Reliability", "Relational MySQL database enforces referential integrity through foreign key constraints; transaction logs ensure zero data corruption during sudden server restarts."],
        ["Maintainability", "Modular separation of concerns dividing React presentation pages, Express route controllers, database connection pool, and utility middleware."],
        ["Scalability", "Stateless Express REST API enables horizontal scaling behind a reverse proxy; connection pool manages concurrent MySQL connections efficiently."],
        ["Portability", "Standards-compliant web client operates uniformly on Google Chrome, Microsoft Edge, Mozilla Firefox, and Safari on desktop and mobile operating systems."]
    ]
    t1 = doc.add_table(rows=len(nfr_data)+1, cols=2)
    format_table(t1, [1.8, 4.4], nfr_headers, nfr_data)

    # =========================================================================
    # 5. HARDWARE AND SOFTWARE REQUIREMENTS
    # =========================================================================
    add_h1("5. Hardware and Software Requirements")
    
    add_h2("Hardware Requirements")
    add_tbl_caption("Table 2: Hardware Requirements")
    hw_headers = ["Component", "Minimum Requirement", "Recommended Specification"]
    hw_data = [
        ["Processor", "Dual-Core x86/x64 2.0 GHz", "Quad-Core Intel Core i5 / AMD Ryzen 5 or higher"],
        ["RAM", "4 GB DDR3/DDR4", "8 GB DDR4 or higher"],
        ["Hard Disk", "2 GB available storage", "10 GB SSD storage (accommodating database & uploads)"],
        ["Network", "Broadband connection (512 Kbps)", "High-speed LAN / Wi-Fi (10 Mbps or higher)"],
        ["Display", "1024 x 768 resolution", "1920 x 1080 Full HD responsive monitor"]
    ]
    t2 = doc.add_table(rows=len(hw_data)+1, cols=3)
    format_table(t2, [1.5, 2.3, 2.4], hw_headers, hw_data)

    add_h2("Software Requirements")
    add_tbl_caption("Table 3: Software Requirements")
    sw_headers = ["Component", "Environment / Technology", "Role in System"]
    sw_data = [
        ["Operating System", "Windows 10/11, Ubuntu 20.04+, macOS", "Host execution environment"],
        ["Runtime Environment", "Node.js (v18 LTS or later)", "Server-side JavaScript runtime engine"],
        ["Backend Framework", "Express.js 4.19", "HTTP REST API routing and middleware pipeline"],
        ["Database Server", "MySQL Community Server 8.0+", "Relational database storage engine (InnoDB)"],
        ["Database Driver", "mysql2 (v3.9+) with Promise API", "Async connection pooling and query execution"],
        ["Frontend Framework", "React 18.2 with Vite 5.0", "Component-based Single Page Application UI"],
        ["Styling Framework", "Tailwind CSS 3.3", "Utility-first responsive CSS styling"],
        ["Client HTTP Library", "Axios 1.6", "Promise-based client HTTP request engine"],
        ["Security Libraries", "bcryptjs 2.4, jsonwebtoken 9.0", "Password salting/hashing and JWT authorization"],
        ["File Uploads", "Multer 1.4", "Multipart/form-data handler for image attachments"],
        ["Code Editor / IDE", "Visual Studio Code", "Primary development and debugging environment"],
        ["Web Browser", "Google Chrome, Edge, Firefox", "Client application rendering engine"]
    ]
    t3 = doc.add_table(rows=len(sw_data)+1, cols=3)
    format_table(t3, [1.6, 2.3, 2.3], sw_headers, sw_data)

    # =========================================================================
    # 6. DATA FLOW DIAGRAMS
    # =========================================================================
    add_h1("6. Data Flow Diagram")
    add_p(
        "Data Flow Diagrams (DFDs) provide a graphical representation of the flow of information through the Campus Complaint & "
        "Maintenance Management System. They depict the system's inputs, internal processing transformations, data stores, and outputs "
        "without detailing physical hardware or programmatic loops. In the standard Gane and Sarson notation adopted here, external "
        "entities are depicted as rectangles, processes as rounded circles/ellipses, and data stores as open-ended horizontal bars."
    )
    
    add_h2("Level 0 DFD (Context Diagram)")
    add_fig(
        "docs/diagrams/fig01_dfd_level0.png",
        "Figure 1: Level 0 DFD (Context Diagram) of the Campus Complaint Management System",
        "The Context Diagram establishes the global boundary of the system. The central process (0: Campus Complaint & Maintenance "
        "Management System) interacts directly with three primary external entities: Students/Faculty, Administrators, and Maintenance "
        "Staff. Complainants supply credentials, categorized complaint data, evidence images, and feedback ratings, receiving live "
        "status updates and tracking reference codes. Administrators supply triage decisions, staff task assignments, and master data "
        "configurations, receiving consolidated complaint tables and metric summaries. Maintenance technicians receive dispatched work "
        "orders and transmit work progress notes and resolution notifications back to the system."
    )

    add_h2("Level 1 DFD")
    add_fig(
        "docs/diagrams/fig02_dfd_level1.png",
        "Figure 2: Level 1 DFD showing the major processes and data stores",
        "The Level 1 DFD decomposes the monolithic system into seven major functional processes: 1.0 Authentication & Access Control, "
        "2.0 Complaint Registration & Lodging, 3.0 Verification & Review, 4.0 Maintenance Task Assignment, 5.0 Work Execution & Status "
        "Updating, 6.0 Closure & Feedback, and 7.0 Dashboard & System Administration. Information traverses five persistent relational "
        "data stores: D1 (Users DB), D2 (Complaints DB), D3 (Categories & Locations DB), D4 (Complaint Updates Audit Log), and D5 (Feedback DB)."
    )

    add_h2("Level 2 DFD")
    add_fig(
        "docs/diagrams/fig03_dfd_level2.png",
        "Figure 3: Level 2 DFD of Process 2.0 (Complaint Registration & Lodging)",
        "The Level 2 DFD provides an explosive decomposition of Process 2.0 (Complaint Registration & Lodging). Sub-process 2.1 "
        "performs client/server input validation; Sub-process 2.2 verifies the active validity of the submitted Category ID and "
        "Location ID against data store D3; Sub-process 2.3 formats the record, assigns an initial status of 'NEW', generates the unique "
        "tracking code (CMP-YYYYMMDD-XXXXXX), and writes to Complaints DB (D2); finally, Sub-process 2.4 initializes the audit trail "
        "by inserting the initial 'NEW' record into the Complaint Updates DB (D4)."
    )

    # =========================================================================
    # 7. SYSTEM ARCHITECTURE
    # =========================================================================
    add_h1("7. System Architecture")
    add_p(
        "CCMS is structured around an industry-standard 3-tier client-server software architecture separating presentation, "
        "business logic, and persistent storage. This architectural decoupling ensures that modifications in user interface "
        "styling do not interfere with underlying database schemas or business validation rules."
    )
    
    add_fig(
        "docs/diagrams/fig04_architecture.png",
        "Figure 4: Layered system architecture of the Campus Complaint Management System",
        "The presentation layer consists of a React 18 Single Page Application (SPA) executed in the user's browser, utilizing "
        "an Axios client configured with a request interceptor that injects Bearer JWT authorization tokens into all outbound calls. "
        "The application layer comprises an Express.js 4 REST API running on Node.js, providing route controllers, JWT verification "
        "middleware, role authorization guards, file upload processing via Multer, and a finite state transition engine. The data "
        "layer utilizes MySQL 8 accessed via a promise-based connection pool executing parameterized SQL statements."
    )

    add_h2("Relational Data Model & Entity-Relationship Schema")
    add_p(
        "Data persistence is organized in a normalized relational schema comprising seven interconnected tables in the ccms_db "
        "database. Foreign key constraints ensure strict referential integrity across all user actions, assignments, and audit logs."
    )
    
    add_fig(
        "docs/diagrams/fig05_datamodel.png",
        "Figure 5: Relational data model and entity-relationship schema",
        "The Entity-Relationship schema illustrates the seven relational entities. The users table maintains all actor credentials "
        "and roles. The complaints table serves as the primary transaction entity, referencing users (submitter), complaint_categories, "
        "and locations. Subordinate tables include complaint_assignments (linking technicians and supervisors), complaint_updates "
        "(providing an append-only audit trail of every status transition), and feedback (capturing post-resolution user ratings)."
    )

    # =========================================================================
    # 8. MODULE DESCRIPTION
    # =========================================================================
    add_h1("8. Module Description")
    add_p(
        "The system codebase is partitioned into cohesive functional modules designed according to single-responsibility "
        "principles. Each module corresponds to discrete frontend routes and backend controller functions."
    )
    
    add_h2("Module 1: Authentication & Authorization Module")
    add_p(
        "Responsible for identity verification and session tokens. Allows students and faculty to self-register with department "
        "and contact details, hashes passwords using bcryptjs with 10 salt rounds, verifies login credentials against the users table, "
        "and issues signed JWT tokens containing the user ID, email, and role. Provides the verifyToken and requireRole middleware."
    )

    add_h2("Module 2: Complaint Lodging & Management Module")
    add_p(
        "Enables authenticated users to lodge new maintenance complaints. Features reactive dropdowns fetching active categories "
        "and locations from the database, allows image uploads via Multer, validates input completeness, generates unique tracking IDs, "
        "and provides student-filtered views displaying only grievances submitted by the logged-in user."
    )

    add_h2("Module 3: Verification & Administrative Control Module")
    add_p(
        "Equips administrators with triage control over campus grievances. Renders a comprehensive complaint inventory supporting "
        "multi-column filtering, search, and detail inspection. Permits administrators to mark tickets as VERIFIED or REJECTED with "
        "mandatory remarks, and provides real-time dashboard metric aggregation."
    )

    add_h2("Module 4: Maintenance Assignment & Resolution Module")
    add_p(
        "Facilitates administrative delegation of verified tickets to qualified maintenance staff. Populates an active staff selection "
        "menu, records assignment timestamps and supervisor instructions in complaint_assignments, updates ticket status to ASSIGNED, "
        "and provides maintenance personnel with dedicated task queues to start work (IN_PROGRESS) and mark tickets RESOLVED."
    )

    add_h2("Module 5: Feedback & Status Auditing Module")
    add_p(
        "Maintains an immutable audit log of all complaint status transitions in the complaint_updates table, capturing the actor, "
        "old status, new status, diagnostic remarks, and created timestamp. Once a ticket reaches RESOLVED or CLOSED, this module "
        "enables the submitter to rate resolution quality (1 to 5 stars) and record evaluative commentary."
    )

    add_h2("Module 6: Reference Data & System Configuration Module")
    add_p(
        "Governs institutional master data. Permits administrators to add, edit, and deactivate complaint categories (Electrical, "
        "Plumbing, HVAC, etc.), campus locations (building, floor, room), and deactivate user accounts without deleting historical logs."
    )

    add_tbl_caption("Table 4: Summary of Modules and Implementing Files")
    mod_headers = ["Module Name", "Client-Side Implementation", "Server-Side Implementation"]
    mod_data = [
        ["Authentication & RBAC", "pages/auth/LoginPage.jsx, RegisterPage.jsx, context/AuthContext.jsx, utils/api.js", "controllers/authController.js, middleware/auth.js, routes/auth.js"],
        ["Complaint Lodging", "pages/student/NewComplaint.jsx, ComplaintList.jsx, ComplaintDetail.jsx", "controllers/complaintController.js, middleware/upload.js, routes/complaints.js"],
        ["Admin Triage & Dashboard", "pages/admin/AdminDashboard.jsx, AdminComplaints.jsx, ComplaintDetail.jsx", "controllers/complaintController.js, statusController.js, dashboardController.js"],
        ["Staff Assignment & Tasks", "pages/admin/AssignmentsPage.jsx, maintenance/MyTasks.jsx, TaskDetail.jsx", "controllers/assignmentController.js, statusController.js, routes/assignments.js"],
        ["Auditing & Feedback", "pages/student/ComplaintDetail.jsx (History & Feedback sections)", "controllers/feedbackController.js, statusController.js, routes/complaints.js"],
        ["Master Data Admin", "pages/admin/CategoriesPage.jsx, LocationsPage.jsx, UsersPage.jsx", "controllers/categoryController.js, locationController.js, userController.js"]
    ]
    t4 = doc.add_table(rows=len(mod_data)+1, cols=3)
    format_table(t4, [1.6, 2.3, 2.3], mod_headers, mod_data)

    add_tbl_caption("Table 5: REST API Endpoints")
    api_headers = ["Method & Path", "Access Role", "Functional Purpose"]
    api_data = [
        ["POST /api/auth/register", "Public", "Registers new Student/Faculty account with hashed password"],
        ["POST /api/auth/login", "Public", "Authenticates credentials and returns signed JWT token"],
        ["GET /api/auth/me", "Authenticated", "Returns authenticated user identity and role from token"],
        ["GET /api/complaints", "Authenticated", "Lists complaints (role-filtered: Student own, Admin all)"],
        ["POST /api/complaints", "Student / Faculty", "Creates new complaint with optional Multer evidence image"],
        ["GET /api/complaints/:id", "Authenticated", "Returns full complaint details and complete audit updates history"],
        ["PUT /api/complaints/:id", "Student / Faculty", "Updates editable fields of an unverified NEW complaint"],
        ["POST /api/complaints/:id/assign", "Admin", "Assigns verified complaint to maintenance staff with notes"],
        ["PUT /api/complaints/:id/status", "Authenticated (RBAC)", "Transitions complaint status according to FSM rules"],
        ["POST /api/complaints/:id/feedback", "Student / Faculty", "Submits rating (1-5) and feedback for resolved complaint"],
        ["GET /api/dashboard/student", "Student / Faculty", "Returns status summary counts for complainant dashboard"],
        ["GET /api/dashboard/admin", "Admin", "Returns metrics by status, category, priority, and critical open"],
        ["GET /api/dashboard/maintenance", "Maintenance", "Returns assigned task counts by status and recent queue"],
        ["GET /api/assignments", "Admin", "Returns comprehensive history of all staff assignments"],
        ["GET /api/assignments/my", "Maintenance", "Returns active task queue assigned to logged-in technician"],
        ["GET /api/categories", "Authenticated", "Fetches active complaint categories list"],
        ["POST /api/categories", "Admin", "Creates new complaint category"],
        ["GET /api/locations", "Authenticated", "Fetches campus buildings, floors, and rooms list"],
        ["POST /api/locations", "Admin", "Creates new campus location entity"],
        ["GET /api/users", "Admin", "Returns user accounts directory (with role filter)"],
        ["PUT /api/users/:id", "Admin", "Toggles user active status (soft deactivation)"],
        ["GET /api/health", "Public", "Health check endpoint reporting API status and timestamp"]
    ]
    t5 = doc.add_table(rows=len(api_data)+1, cols=3)
    format_table(t5, [2.1, 1.4, 2.7], api_headers, api_data)

    # =========================================================================
    # 9. SYSTEM ANALYSIS
    # =========================================================================
    add_h1("9. System Analysis")
    
    add_h2("9.1 Use Case Diagram")
    add_p(
        "Use Case analysis models the functional interactions between external actors and the system boundaries. "
        "The actors identified in the CCMS domain are: Student/Faculty (Complainant), Administrator, and Maintenance Staff."
    )
    
    add_fig(
        "docs/diagrams/fig06_usecase.png",
        "Figure 6: Use case diagram of the Campus Complaint Management System",
        "The use case diagram depicts the boundary of CCMS and the 12 primary use cases categorized across the three user roles. "
        "Complainants interact with login, complaint filing, status tracking, feedback submission, and reopening. Administrators "
        "manage ticket triage (verify/reject), allocation to maintenance personnel, ticket closure, master data management, and "
        "system metrics. Maintenance technicians view allocated tickets, update status to in-progress, and record resolution remarks."
    )

    add_h2("9.2 Use Case Descriptions")
    add_p("Detailed specifications for the core use cases are tabulated below:")

    add_tbl_caption("Table 6: Use Case Description: User Registration and Login (UC01)")
    uc1_data = [
        ["Use Case ID / Name", "UC01 – User Registration and Login"],
        ["Actor(s)", "Student, Faculty, Maintenance Staff, Administrator"],
        ["Description", "Allows new users to register and existing users to authenticate and receive a JWT token."],
        ["Precondition", "Client web application is accessible in browser; database connection is online."],
        ["Main Flow", "1. User navigates to /login or /register.\n2. In registration, user submits name, email, password, role, department, phone.\n3. Server hashes password with bcryptjs and stores user in database.\n4. In login, user submits email and password.\n5. Server verifies password hash and returns signed JWT token.\n6. Client stores token in localStorage and redirects to role dashboard."],
        ["Alternate Flow", "Invalid credentials or existing email: System returns HTTP 400/401 and displays an error alert."],
        ["Postcondition", "User is securely authenticated with active session; token injected in API requests."]
    ]
    t6 = doc.add_table(rows=len(uc1_data)+1, cols=2)
    format_table(t6, [1.8, 4.4], ["Field", "Description"], uc1_data)

    add_tbl_caption("Table 7: Use Case Description: Submit Complaint (UC02)")
    uc2_data = [
        ["Use Case ID / Name", "UC02 – Submit Complaint"],
        ["Actor(s)", "Student, Faculty"],
        ["Description", "Complainant files a new maintenance request with categorization, location, and optional photo."],
        ["Precondition", "User is logged in with STUDENT or FACULTY role."],
        ["Main Flow", "1. User navigates to /student/complaints/new.\n2. User enters title, selects category, selects location, selects priority, and writes description.\n3. User optionally attaches an image file (JPG/PNG max 5MB).\n4. User clicks 'Submit Complaint'.\n5. Server validates fields, saves image via Multer, inserts complaint record with status 'NEW', generates reference number, logs audit update, and returns HTTP 201.\n6. Client redirects user to complaint detail view."],
        ["Alternate Flow", "Missing required fields or invalid file format: Server returns HTTP 400 with validation error message."],
        ["Postcondition", "New complaint stored in database with unique tracking ID; status initialized to NEW."]
    ]
    t7 = doc.add_table(rows=len(uc2_data)+1, cols=2)
    format_table(t7, [1.8, 4.4], ["Field", "Description"], uc2_data)

    add_tbl_caption("Table 8: Use Case Description: Track Own Complaints (UC03)")
    uc3_data = [
        ["Use Case ID / Name", "UC03 – Track Own Complaints"],
        ["Actor(s)", "Student, Faculty"],
        ["Description", "User reviews personal complaint history, current statuses, and audit trail."],
        ["Precondition", "User is authenticated."],
        ["Main Flow", "1. User accesses /student/complaints.\n2. Client invokes GET /api/complaints with JWT token.\n3. Server queries complaints table filtering by user_id = req.user.id.\n4. Client displays complaint list with search, status badges, and date filed.\n5. User clicks 'View' on any ticket to inspect complete audit trail and details."],
        ["Alternate Flow", "No complaints filed yet: Interface displays an informative empty state message."],
        ["Postcondition", "Complainant is fully informed of current progress and past remarks."]
    ]
    t8 = doc.add_table(rows=len(uc3_data)+1, cols=2)
    format_table(t8, [1.8, 4.4], ["Field", "Description"], uc3_data)

    add_tbl_caption("Table 9: Use Case Description: Verify or Reject Complaint (UC06)")
    uc9_data = [
        ["Use Case ID / Name", "UC06 – Verify or Reject Complaint"],
        ["Actor(s)", "Administrator"],
        ["Description", "Administrator assesses authenticity of a new ticket and marks it VERIFIED or REJECTED."],
        ["Precondition", "Administrator is logged in; target complaint is in 'NEW' status."],
        ["Main Flow", "1. Administrator opens complaint detail view.\n2. Administrator enters assessment remarks in the action panel.\n3. Administrator clicks 'Verify Complaint' or 'Reject Complaint'.\n4. Client calls PUT /api/complaints/:id/status with new status ('VERIFIED' or 'REJECTED') and remarks.\n5. Server confirms statusController transition rule, updates complaints table, inserts into complaint_updates, and returns HTTP 200.\n6. UI refreshes to reflect new status."],
        ["Alternate Flow", "Complaint is not in NEW status: Server rejects transition with HTTP 400."],
        ["Postcondition", "Complaint status updated to VERIFIED (ready for assignment) or terminal REJECTED."]
    ]
    t9 = doc.add_table(rows=len(uc9_data)+1, cols=2)
    format_table(t9, [1.8, 4.4], ["Field", "Description"], uc9_data)

    add_tbl_caption("Table 10: Use Case Description: Assign Complaint to Staff (UC07)")
    uc10_data = [
        ["Use Case ID / Name", "UC07 – Assign Complaint to Staff"],
        ["Actor(s)", "Administrator"],
        ["Description", "Administrator delegates a verified complaint to a designated maintenance technician."],
        ["Precondition", "Complaint is in 'VERIFIED' or 'REOPENED' status; maintenance staff accounts exist."],
        ["Main Flow", "1. Administrator opens ticket detail view.\n2. System loads maintenance staff directory via GET /api/users?role=MAINTENANCE.\n3. Administrator selects technician from dropdown and enters assignment notes.\n4. Administrator clicks 'Assign Staff'.\n5. Client calls POST /api/complaints/:id/assign.\n6. Server verifies staff role, inserts record into complaint_assignments, updates complaint status to 'ASSIGNED', logs audit update, and returns HTTP 200.\n7. UI updates showing assigned staff details."],
        ["Alternate Flow", "Selected user is not active or not in MAINTENANCE role: Server returns error HTTP 400."],
        ["Postcondition", "Staff assignment persisted; complaint status transitioned to ASSIGNED."]
    ]
    t10 = doc.add_table(rows=len(uc10_data)+1, cols=2)
    format_table(t10, [1.8, 4.4], ["Field", "Description"], uc10_data)

    add_tbl_caption("Table 11: Use Case Description: Execute and Resolve Task (UC11 & UC12)")
    uc11_data = [
        ["Use Case ID / Name", "UC11 & UC12 – Execute and Resolve Task"],
        ["Actor(s)", "Maintenance Staff"],
        ["Description", "Technician accepts assigned work order, transitions to IN_PROGRESS, and marks RESOLVED."],
        ["Precondition", "Technician is authenticated; task is assigned to technician's user ID."],
        ["Main Flow", "1. Technician opens /maintenance/tasks.\n2. Clicks 'Start Work' on ASSIGNED ticket; client calls PUT /status with 'IN_PROGRESS'.\n3. Technician conducts physical repair.\n4. Upon completion, technician enters resolution remarks and clicks 'Mark Resolved'.\n5. Client calls PUT /status with 'RESOLVED' and remarks.\n6. Server validates transition, updates complaint status and resolved_at timestamp, logs audit update, and returns HTTP 200.\n7. Task is moved to resolved section."],
        ["Alternate Flow", "Technician attempts illegal transition: Server rejects with validation error."],
        ["Postcondition", "Complaint resolved with diagnostic remarks; complainant prompted for feedback."]
    ]
    t11 = doc.add_table(rows=len(uc11_data)+1, cols=2)
    format_table(t11, [1.8, 4.4], ["Field", "Description"], uc11_data)

    # =========================================================================
    # 10. UML DESIGN
    # =========================================================================
    add_h1("10. UML Design")
    add_p(
        "Unified Modeling Language (UML) diagrams provide standard structural and behavioral blueprints of the system. "
        "The diagrams presented in this section accurately model the actual software classes, database entities, sequence flows, "
        "and physical deployment topologies of CCMS."
    )
    
    add_h2("10.1 Class Diagram")
    add_fig(
        "docs/diagrams/fig07_class.png",
        "Figure 7: Class diagram of the Campus Complaint Management System",
        "The Class Diagram models the object-oriented domain structure of CCMS. The User entity encapsulates authentication "
        "and profile attributes. The Complaint entity maintains core ticket data and references Category and Location. Specialized "
        "association entities include ComplaintAssignment (linking complaints to technicians and supervisors), ComplaintUpdate "
        "(capturing status audit events), and Feedback (storing satisfaction metrics). Multiplicities accurately reflect database constraints."
    )

    add_h2("10.2 Sequence Diagrams")
    add_fig(
        "docs/diagrams/fig08_sequence_submit.png",
        "Figure 8: Sequence diagram: Student submits a new complaint",
        "Illustrates the message exchange during complaint submission: the Student fills the NewComplaint form; Axios injects the JWT "
        "Bearer token; Express routes the payload through verifyToken; complaintController generates the reference number, executes "
        "parameterized INSERT statements into complaints and complaint_updates tables, and returns HTTP 201 Created to the client."
    )
    
    add_fig(
        "docs/diagrams/fig09_sequence_assign.png",
        "Figure 9: Sequence diagram: Administrator verifies and assigns complaint to maintenance staff",
        "Traces the two-step administrative triage process: first, the administrator sends a PUT request transitioning the complaint "
        "from NEW to VERIFIED; second, the administrator selects an active maintenance staff member and sends a POST /assign request, "
        "triggering database updates across complaints, complaint_assignments, and complaint_updates tables."
    )

    add_h2("10.3 Activity Diagram")
    add_fig(
        "docs/diagrams/fig10_activity.png",
        "Figure 10: Activity diagram of the complete complaint lifecycle workflow",
        "Depicts the operational control flow across Student, Administrator, and Maintenance roles. Shows decision nodes for input "
        "validation, administrative verification, staff acceptance, repair completion, user satisfaction assessment, and closure/reopening."
    )

    add_h2("10.4 State Diagram")
    add_fig(
        "docs/diagrams/fig11_state.png",
        "Figure 11: State diagram of a complaint lifecycle",
        "Models the exact Finite State Machine (FSM) implemented in statusController.js. A complaint originates in NEW and can legally "
        "transition to VERIFIED or REJECTED. A VERIFIED complaint transitions to ASSIGNED. Staff transition it to IN_PROGRESS and then "
        "RESOLVED. A RESOLVED complaint transitions to CLOSED or REOPENED. An issue that reoccurs can transition from CLOSED back to REOPENED."
    )

    add_h2("10.5 Component Diagram")
    add_fig(
        "docs/diagrams/fig12_component.png",
        "Figure 12: Component diagram of the Campus Complaint Management System",
        "Details software packaging and module dependencies across frontend, backend, and persistence tiers. Highlights the central role "
        "of AuthContext and api.js in the client, and Express middleware, route controllers, and MySQL connection pool on the server."
    )

    add_h2("10.6 Deployment Diagram")
    add_fig(
        "docs/diagrams/fig13_deployment.png",
        "Figure 13: Deployment diagram of the Campus Complaint Management System",
        "Illustrates physical nodes and network protocols. The client browser communicates over HTTP/HTTPS (Port 5173/80) with the "
        "Node.js application server hosting the Express REST API (Port 5000), which connects via TCP Port 3306 to the MySQL 8 database server."
    )

    # =========================================================================
    # 11. TESTING
    # =========================================================================
    add_h1("11. Testing")
    
    add_h2("11.1 Test Plan")
    add_p(
        "System testing was conducted across multiple levels—including unit testing of critical backend utilities, basis path "
        "testing of state transitions, integration testing of REST endpoints, and black-box system validation of user workflows. "
        "Table 12 outlines the techniques applied and their scope."
    )
    
    add_tbl_caption("Table 12: Testing Techniques Applied")
    t12_headers = ["Technique", "Target Scope", "Methodology"]
    t12_data = [
        ["Unit Testing", "Password hashing, complaint ID generator, sanitization", "Executed in Node.js test runner verifying function inputs and outputs."],
        ["Basis Path Testing", "State machine transition validator (statusController.js)", "Calculated cyclomatic complexity and verified all legal and illegal transition branches."],
        ["API Integration Testing", "All Express route endpoints (/api/auth, /api/complaints, etc.)", "Executed HTTP requests verifying status codes, headers, and database side-effects."],
        ["Black-Box Testing", "User authentication, complaint filing, staff assignment, feedback", "Verified system behavior against functional requirements using browser automation."],
        ["Role Access Control Testing", "Endpoint authorization guards (verifyToken, requireRole)", "Attempted privileged actions with unprivileged or missing JWT tokens."]
    ]
    t12 = doc.add_table(rows=len(t12_data)+1, cols=3)
    format_table(t12, [1.8, 2.3, 2.1], t12_headers, t12_data)

    add_h2("Basis Path Testing of State Machine Transitions")
    add_p(
        "The state transition engine in statusController.js evaluates the current ticket status against an allowed transition "
        "matrix (VALID_TRANSITIONS) and checks user role permissions. Cyclomatic complexity analysis yielded 5 primary decision "
        "paths evaluated in Table 13."
    )
    
    add_tbl_caption("Table 13: Independent Paths of State Transition Validation")
    t13_headers = ["Path ID", "Condition & Trigger Event", "Expected Result", "Status"]
    t13_data = [
        ["P1", "Current status is NEW; Admin requests VERIFIED", "Allowed (Status updated to VERIFIED)", "PASS"],
        ["P2", "Current status is NEW; Admin requests REJECTED", "Allowed (Status updated to REJECTED)", "PASS"],
        ["P3", "Current status is NEW; User requests CLOSED (Illegal leap)", "Rejected (HTTP 400 Invalid transition)", "PASS"],
        ["P4", "Current status is ASSIGNED; Staff requests IN_PROGRESS", "Allowed (Status updated to IN_PROGRESS)", "PASS"],
        ["P5", "Current status is IN_PROGRESS; Non-staff requests RESOLVED", "Rejected (HTTP 403 Forbidden role)", "PASS"]
    ]
    t13 = doc.add_table(rows=len(t13_data)+1, cols=4)
    format_table(t13, [1.0, 2.7, 1.8, 0.7], t13_headers, t13_data)

    add_h2("11.2 Unit Test Results")
    add_p(
        "The unit tests below were executed against the project's utility and helper modules. All 11 unit tests executed cleanly."
    )
    
    add_tbl_caption("Table 14: Unit Test Cases and Results")
    t14_headers = ["TC ID", "Module / Function", "Test Input", "Expected Output", "Actual Output", "Status"]
    t14_data = [
        ["UT01", "bcrypt.hash", "Password: 'Admin@123', salt: 10", "Valid 60-char bcrypt string", "Starts with $2a$10$", "PASS"],
        ["UT02", "bcrypt.compare", "Match: 'Admin@123' with stored hash", "Returns true", "Returns true", "PASS"],
        ["UT03", "bcrypt.compare", "Mismatch: 'WrongPass' with hash", "Returns false", "Returns false", "PASS"],
        ["UT04", "generateComplaintId", "Invocation date: 2026-10-02", "Pattern: CMP-YYYYMMDD-XXXXXX", "Matches regex pattern", "PASS"],
        ["UT05", "sanitizeUser", "User dict with password_hash", "Returns dict without hash", "password_hash omitted", "PASS"],
        ["UT06", "JWT Sign & Verify", "Payload: {id: 1, role: 'ADMIN'}", "Decodes matching payload", "Payload verified", "PASS"],
        ["UT07", "Expired Token Check", "JWT with exp in past", "Verification throws TokenExpiredError", "Error caught", "PASS"],
        ["UT08", "Malformed Token", "Header: 'Bearer invalid.token'", "Verification throws JsonWebTokenError", "Error caught", "PASS"],
        ["UT09", "Location CONCAT", "building='AB1', floor='2', room='204'", "String: 'AB1 - 2 204'", "Matches expected string", "PASS"],
        ["UT10", "FSM Lookup", "Lookup transitions for 'VERIFIED'", "Returns ['ASSIGNED', 'REJECTED']", "Matches array", "PASS"],
        ["UT11", "Role Verification", "req.user.role='STUDENT', requireRole('ADMIN')", "Calls res.status(403)", "Returns 403 Forbidden", "PASS"]
    ]
    t14 = doc.add_table(rows=len(t14_data)+1, cols=6)
    format_table(t14, [0.8, 1.3, 1.4, 1.3, 1.0, 0.6], t14_headers, t14_data)

    add_h2("11.3 Black-Box and System Test Cases")
    add_p(
        "Black-box testing verified user-facing workflows on the running full-stack system across all four supported roles."
    )
    
    add_tbl_caption("Table 15: Black-Box and System Test Cases")
    t15_headers = ["TC ID", "Scenario", "Test Input", "Expected Result", "Actual Result", "Status"]
    t15_data = [
        ["TC01", "Valid Administrator Login", "admin@ccms.local / Admin@123", "HTTP 200; JWT returned; redirects to Admin Dashboard", "Redirected to /admin/dashboard", "PASS"],
        ["TC02", "Valid Student Login", "student@ccms.local / Admin@123", "HTTP 200; JWT returned; redirects to Student Dashboard", "Redirected to /student/dashboard", "PASS"],
        ["TC03", "Valid Maintenance Login", "maintenance@ccms.local / Admin@123", "HTTP 200; JWT returned; redirects to Maintenance Dashboard", "Redirected to /maintenance/dashboard", "PASS"],
        ["TC04", "Invalid Password", "admin@ccms.local / WrongPassword", "HTTP 401; 'Invalid credentials' error alert", "HTTP 401 error displayed", "PASS"],
        ["TC05", "Unregistered User", "nonexistent@ccms.local / Admin@123", "HTTP 401; 'Invalid credentials' error alert", "HTTP 401 error displayed", "PASS"],
        ["TC06", "Student Registration", "Valid details: name, email, password, role", "HTTP 201; User registered; prompt to login", "Account created successfully", "PASS"],
        ["TC07", "Duplicate Email Registration", "Existing email: student@ccms.local", "HTTP 400; 'User already exists' error alert", "HTTP 400 error displayed", "PASS"],
        ["TC08", "Complaint Submission", "Title, category_id, location_id, description", "HTTP 201; CMP code created; redirects to detail", "Complaint submitted; CMP code shown", "PASS"],
        ["TC09", "Missing Required Fields", "Submit complaint with blank description", "HTTP 400; Form validation error displayed", "Browser/API validation blocked", "PASS"],
        ["TC10", "Student Views Own Complaints", "Logged in as student@ccms.local", "Displays only complaints lodged by student (count: 5)", "Exactly 5 complaints listed", "PASS"],
        ["TC11", "Admin Verifies Complaint", "Click 'Verify' on NEW complaint", "HTTP 200; status changes to VERIFIED; audit logged", "Status updated to VERIFIED", "PASS"],
        ["TC12", "Admin Rejects Complaint", "Click 'Reject' with remarks", "HTTP 200; status changes to REJECTED; audit logged", "Status updated to REJECTED", "PASS"],
        ["TC13", "Admin Assigns Staff", "Select technician & click 'Assign Staff'", "HTTP 200; assignment stored; status ASSIGNED", "Assignment displayed on ticket", "PASS"],
        ["TC14", "Staff Starts Work Order", "Technician clicks 'Start Work'", "HTTP 200; status transitions to IN_PROGRESS", "Status badge changes to Yellow", "PASS"],
        ["TC15", "Staff Marks Resolved", "Technician enters repair remarks & resolves", "HTTP 200; status transitions to RESOLVED", "Status badge changes to Green", "PASS"],
        ["TC16", "Complainant Feedback", "Student rates 5 stars and comments", "HTTP 201; feedback stored in feedback table", "Feedback saved; form hidden", "PASS"],
        ["TC17", "Admin Closes Ticket", "Admin clicks 'Close Complaint'", "HTTP 200; status transitions to CLOSED", "Ticket marked CLOSED", "PASS"],
        ["TC18", "Unauthorized Access", "Student calls PUT /api/complaints/:id/status", "HTTP 403 Forbidden; 'Access denied' response", "Blocked with HTTP 403", "PASS"]
    ]
    t15 = doc.add_table(rows=len(t15_data)+1, cols=6)
    format_table(t15, [0.7, 1.4, 1.4, 1.3, 1.0, 0.6], t15_headers, t15_data)

    # =========================================================================
    # 12. RESULTS / SCREENSHOTS
    # =========================================================================
    add_h1("12. Results / Screenshots")
    add_p(
        "This section presents authentic captures of the running Campus Complaint & Maintenance Management System, "
        "demonstrating the user interface and functionality across all user roles."
    )
    
    add_fig(
        "docs/screenshots/01_login_page.png",
        "Figure 14: Login page showing role-based authentication and demo credentials",
        "The login portal is the primary entry point for all users. It features email and password inputs, error validation, "
        "links to account registration, and a demo credentials reference box displaying working accounts for all four roles."
    )

    add_fig(
        "docs/screenshots/02_register_page.png",
        "Figure 15: User registration page for student and faculty onboarding",
        "The registration screen enables prospective campus users to onboard into the system by submitting their full name, "
        "institutional email address, password, password confirmation, role (STUDENT or FACULTY), academic department, and contact phone."
    )

    add_fig(
        "docs/screenshots/03_student_dashboard.png",
        "Figure 16: Student dashboard with status summary cards and recent complaints",
        "The student dashboard presents high-level statistics covering total complaints, pending reviews, active work orders, "
        "and resolved issues. A summary table displays the student's recent tickets with clickable titles navigating to full details."
    )

    add_fig(
        "docs/screenshots/04_new_complaint.png",
        "Figure 17: File a new complaint form with category, location, and priority selection",
        "The complaint lodging form allows users to enter an issue title, choose from pre-populated category and location dropdowns, "
        "set priority (Low, Medium, High, Critical), provide a detailed text description, and optionally attach an evidence photo."
    )

    add_fig(
        "docs/screenshots/05_student_complaints_list.png",
        "Figure 18: Student complaints tracking list with search and status badges",
        "The complaint tracking view lists all grievances filed by the logged-in student. It includes dynamic search by title or "
        "complaint number, color-coded status badges, submission timestamps, and direct action links to view ticket progress."
    )

    add_fig(
        "docs/screenshots/06_student_complaint_detail.png",
        "Figure 19: Student complaint detail view with audit trail and feedback form",
        "Displays complete ticket information including unique tracking ID, category, location, priority, and original description. "
        "An audit trail section shows all past status changes with technician remarks. Upon resolution, a 5-star feedback form is presented."
    )

    add_fig(
        "docs/screenshots/07_admin_dashboard.png",
        "Figure 20: Administrator dashboard with system-wide analytics and metric cards",
        "The administrator dashboard provides campus-wide oversight with metric cards for total tickets, new unverified submissions, "
        "active repairs, closed tickets, and high/critical open hazards. Additional panels show complaints grouped by category and recent logs."
    )

    add_fig(
        "docs/screenshots/08_admin_complaints.png",
        "Figure 21: Administrator complaints management table with filters and search",
        "The central complaint triage table allows administrators to manage institutional tickets. Features instant search across titles, "
        "tracking numbers, and complainant names, a comprehensive lifecycle status filter, and 'Manage' buttons to open triage controls."
    )

    add_fig(
        "docs/screenshots/09_admin_complaint_detail.png",
        "Figure 22: Administrator complaint detail view with verification and staff assignment",
        "Provides administrators with ticket details and an interactive action sidebar. Administrators can verify or reject NEW tickets, "
        "select qualified maintenance staff from a dynamic dropdown to assign VERIFIED tickets, and close RESOLVED complaints."
    )

    add_fig(
        "docs/screenshots/10_admin_users.png",
        "Figure 23: Administrator users management page with active status toggling",
        "The user administration directory lists all registered accounts across all roles with email, department, and active status. "
        "Administrators can deactivate compromised or departing user accounts with a single click, immediately invalidating their access."
    )

    add_fig(
        "docs/screenshots/11_admin_categories.png",
        "Figure 24: Administrator categories management page",
        "Enables administrators to view, add, and edit maintenance categories (Electrical, Plumbing, HVAC, Furniture, Network, etc.) "
        "which dynamically populate the complaint submission category dropdown across the campus portal."
    )

    add_fig(
        "docs/screenshots/12_admin_locations.png",
        "Figure 25: Administrator locations management page",
        "Allows campus administrators to catalog institutional physical infrastructure, defining building names, floor numbers, "
        "room identifiers, and descriptions to ensure complaints point to unambiguous physical locations."
    )

    add_fig(
        "docs/screenshots/13_admin_assignments.png",
        "Figure 26: Administrator assignments tracking page",
        "Presents an institutional log of all work delegations, displaying complaint numbers, task titles, assigned technician names, "
        "assigning administrator names, exact dispatch timestamps, and current repair progress."
    )

    add_fig(
        "docs/screenshots/14_maintenance_dashboard.png",
        "Figure 27: Maintenance staff dashboard with task counters",
        "The technician dashboard provides maintenance personnel with real-time counters of tickets currently assigned to them, "
        "active tasks in progress, and completed resolutions, alongside a quick-access table of recent task assignments."
    )

    add_fig(
        "docs/screenshots/15_maintenance_tasks.png",
        "Figure 28: Maintenance staff assigned tasks table with progress actions",
        "The technician's task queue displays all assigned tickets with location and category context. Features inline action buttons: "
        "'Start Work' transitions assigned tickets to IN_PROGRESS, and 'Mark Resolved' prompts for work remarks to complete the job."
    )

    add_fig(
        "docs/screenshots/16_maintenance_task_detail.png",
        "Figure 29: Maintenance task detail view with status update and work remarks form",
        "The task detail view provides technicians with comprehensive issue descriptions and attached evidence photographs, "
        "alongside an update panel to select new progress states and record detailed diagnostic remarks."
    )

    # =========================================================================
    # 13. LIMITATIONS
    # =========================================================================
    add_h1("13. Limitations")
    add_p("While the CCMS implementation satisfies all primary project objectives, the current system possesses the following genuine technical constraints:")
    add_bullet("Currently, the system does not integrate an external SMTP email server or SMS gateway (e.g., Twilio/Nodemailer). Users must log in to the web portal to view status changes.", "1. Absence of External Notification Services: ")
    add_bullet("Uploaded evidence photographs are stored on the local server filesystem under backend/uploads/ rather than in a cloud object store (e.g., AWS S3), requiring server disk monitoring.", "2. Local File System Image Storage: ")
    add_bullet("Administrators allocate work orders manually by selecting technicians from a menu; the system does not currently feature automated skill-based or workload-balanced task dispatching.", "3. Manual Staff Allocation: ")
    add_bullet("While fully responsive on mobile web browsers, the project is a React SPA and does not currently include a standalone native mobile application (iOS/Android).", "4. No Native Mobile Application: ")
    add_bullet("Real-time updates require standard HTTP request polling or page refreshes; WebSocket protocols (e.g., Socket.io) are not currently utilized for live bidirectional push updates.", "5. Polling-Based Status Refreshes: ")

    # =========================================================================
    # 14. CONCLUSION
    # =========================================================================
    add_h1("14. Conclusion")
    add_p(
        "The Campus Complaint & Maintenance Management System successfully addresses the inefficiencies, opacity, and data loss "
        "characteristic of traditional manual grievance registers in academic institutions. By designing and implementing a robust "
        "full-stack web platform utilizing React 18, Node.js, Express.js, and MySQL 8, the project establishes a modern, structured, "
        "and accountable maintenance ecosystem."
    )
    add_p(
        "Key engineering achievements include: (1) an end-to-end digitized complaint lifecycle governed by a strict finite state "
        "machine (NEW → VERIFIED → ASSIGNED → IN_PROGRESS → RESOLVED → CLOSED); (2) secure role-based access control protecting "
        "administrative and technician functions; (3) structured categorization by campus building, floor, room, category, and severity; "
        "(4) an immutable audit trail capturing every status transition with technician remarks and timestamps; (5) post-resolution "
        "feedback ratings empowering student evaluation; and (6) an administrative governance dashboard tracking institutional metrics. "
        "All modules were verified through structured unit, basis path, and system test cases, confirming that the system satisfies all "
        "academic and engineering requirements."
    )

    # =========================================================================
    # 15. REFERENCES
    # =========================================================================
    add_h1("15. References")
    add_p("Books:", bold=True, font_size=12)
    add_bullet("Roger S. Pressman and Bruce R. Maxim, Software Engineering: A Practitioner's Approach, 9th Edition, McGraw-Hill Education, 2020.", "1. ")
    add_bullet("Ian Sommerville, Software Engineering, 10th Edition, Pearson Education, 2016.", "2. ")
    add_bullet("Abraham Silberschatz, Henry F. Korth, and S. Sudarshan, Database System Concepts, 7th Edition, McGraw-Hill, 2019.", "3. ")
    
    add_p("Online Documentation & Specifications:", bold=True, font_size=12, space_before=8)
    add_bullet("React Official Documentation, 'Describing the UI and Managing State', https://react.dev", "4. ")
    add_bullet("Express.js Documentation, 'Routing, Middleware and Error Handling', https://expressjs.com", "5. ")
    add_bullet("MySQL 8.0 Reference Manual, 'InnoDB Storage Engine and Relational Indexing', https://dev.mysql.com/doc", "6. ")
    add_bullet("Internet Engineering Task Force (IETF), 'JSON Web Token (JWT) Specification', RFC 7519, https://datatracker.ietf.org/doc/html/rfc7519", "7. ")
    add_bullet("Vite Frontend Tooling Guide, 'Next Generation Frontend Tooling', https://vitejs.dev", "8. ")
    add_bullet("Tailwind CSS Documentation, 'Utility-First CSS Framework', https://tailwindcss.com/docs", "9. ")

    # =========================================================================
    # APPENDIX
    # =========================================================================
    add_h1("Appendix")
    
    add_h2("A. Additional Screenshots")
    add_p(
        "Additional interface views—including reference data configuration, locations cataloging, and administrative "
        "assignment records—are illustrated in Figures 24, 25, and 26 in Section 12."
    )

    add_h2("B. Sample Inputs and Outputs")
    add_p("Illustrative database records and API payloads from the live CCMS application are provided below.")
    
    add_tbl_caption("Table 16: Sample Complaint Audit History Record (complaint_updates table)")
    t16_headers = ["Update ID", "Complaint #", "Actor Role", "Old Status", "New Status", "Remarks", "Timestamp"]
    t16_data = [
        ["1", "CMP-20231001-001", "STUDENT", "NULL", "NEW", "Complaint submitted by student", "2023-10-01 09:30:00"],
        ["2", "CMP-20231001-001", "ADMIN", "NEW", "VERIFIED", "Issue verified by Department Admin", "2023-10-01 10:15:00"],
        ["3", "CMP-20231001-001", "ADMIN", "VERIFIED", "ASSIGNED", "Assigned to Electrical Staff", "2023-10-01 11:00:00"],
        ["4", "CMP-20231001-001", "MAINTENANCE", "ASSIGNED", "IN_PROGRESS", "Technician dispatched to Room 101", "2023-10-01 11:30:00"],
        ["5", "CMP-20231001-001", "MAINTENANCE", "IN_PROGRESS", "RESOLVED", "Replaced burnt fan regulator", "2023-10-01 14:00:00"],
        ["6", "CMP-20231001-001", "ADMIN", "RESOLVED", "CLOSED", "Confirmed operational by Faculty Incharge", "2023-10-01 16:00:00"]
    ]
    t16 = doc.add_table(rows=len(t16_data)+1, cols=7)
    format_table(t16, [0.7, 1.2, 0.9, 0.7, 0.8, 1.2, 0.9], t16_headers, t16_data)

    add_tbl_caption("Table 17: Sample API Request and Response (Submit Complaint)")
    api_samp_headers = ["Transaction Component", "Details / Data Payload"]
    api_samp_data = [
        ["HTTP Endpoint & Method", "POST http://localhost:5000/api/complaints"],
        ["Headers", "Authorization: Bearer <JWT_TOKEN>\nContent-Type: multipart/form-data"],
        ["Request Payload (FormData)", "{\n  \"title\": \"Water leakage in 2nd floor restroom\",\n  \"category_id\": 2,\n  \"location_id\": 4,\n  \"priority\": \"HIGH\",\n  \"description\": \"Main tap is continuously dripping, flooding the sink counter.\"\n}"],
        ["Response Status Code", "201 Created"],
        ["Response Payload (JSON)", "{\n  \"success\": true,\n  \"complaintId\": 12,\n  \"complaint_number\": \"CMP-20261004-884920\",\n  \"message\": \"Complaint submitted successfully\"\n}"]
    ]
    t17 = doc.add_table(rows=len(api_samp_data)+1, cols=2)
    format_table(t17, [2.0, 4.2], api_samp_headers, api_samp_data)

    add_h2("C. User Manual")
    add_p("Setting Up and Running the Application Locally:", bold=True, font_size=12)
    add_bullet("Ensure Node.js 18+ and MySQL Server 8.0+ are installed and active on the host machine.", "1. Prerequisites: ")
    add_bullet("Clone the GitHub repository: git clone https://github.com/karthikeyangullipalli/Campus-Complaint-Maintenance-Management-System.git", "2. Clone Repo: ")
    add_bullet("Execute database/schema.sql followed by database/seed.sql in MySQL to initialize ccms_db with tables and seed accounts.", "3. Database Setup: ")
    add_bullet("In backend/, copy .env.example to .env and configure DB_PASSWORD with your local MySQL password. Run 'npm install' followed by 'node server.js'. Backend starts on http://localhost:5000.", "4. Backend Launch: ")
    add_bullet("In frontend/, run 'npm install' followed by 'npm run dev'. Access the application in your browser at http://localhost:5173.", "5. Frontend Launch: ")

    add_p("Using the Application as a Student / Faculty Member:", bold=True, font_size=12, space_before=8)
    add_bullet("Open http://localhost:5173/login. Log in using student@ccms.local (Password: Admin@123) or register a new account.", "1. Login: ")
    add_bullet("Click '+ New Complaint' on the sidebar or dashboard. Enter the title, choose category and location, set priority, enter description, and submit.", "2. Submit Ticket: ")
    add_bullet("Navigate to 'My Complaints' to inspect live status badges and view detailed technician remarks.", "3. Track Status: ")
    add_bullet("Once a complaint is marked RESOLVED, open the detail view and submit a 1 to 5 star rating with feedback commentary.", "4. Provide Feedback: ")

    add_p("Using the Application as an Administrator:", bold=True, font_size=12, space_before=8)
    add_bullet("Log in using admin@ccms.local (Password: Admin@123). The Admin Dashboard displays institutional metric summaries.", "1. Login: ")
    add_bullet("Click 'Complaints' to inspect the master table. Click 'Manage' on any NEW ticket to review details.", "2. Triage Tickets: ")
    add_bullet("Click 'Verify Complaint' to validate the issue, or 'Reject Complaint' with explanatory remarks.", "3. Verify / Reject: ")
    add_bullet("On a VERIFIED ticket, select a technician from the maintenance staff menu, add assignment notes, and click 'Assign Staff'.", "4. Assign Technician: ")
    add_bullet("Use 'Users', 'Categories', and 'Locations' in the sidebar to administer campus master data.", "5. Master Data: ")

    add_p("Using the Application as Maintenance Staff:", bold=True, font_size=12, space_before=8)
    add_bullet("Log in using maintenance@ccms.local (Password: Admin@123). The dashboard displays assigned task counters.", "1. Login: ")
    add_bullet("Navigate to 'My Tasks' to inspect work orders allocated specifically to your account.", "2. View Queue: ")
    add_bullet("Click 'Start Work' on an ASSIGNED ticket to change its status to IN_PROGRESS.", "3. Start Task: ")
    add_bullet("After physical remediation, click 'Mark Resolved' and input diagnostic remarks detailing repair work performed.", "4. Resolve Issue: ")

    output_path = "Campus_Complaint_Management_System_Mini_Project_Report.docx"
    doc.save(output_path)
    print(f"Report document successfully generated at: {output_path}")

if __name__ == "__main__":
    build_complete_report()
