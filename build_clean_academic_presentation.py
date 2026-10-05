import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# ---------------------------------------------------------------------------
# COLOR PALETTE (Minimal, High-Contrast Academic Theme)
# ---------------------------------------------------------------------------
NAVY = RGBColor(15, 23, 42)          # #0F172A - Deep Slate/Navy (Primary Headers)
BLUE = RGBColor(37, 99, 235)         # #2563EB - Academic Blue (Accents, Nodes, Arrows)
DARK_TEXT = RGBColor(30, 41, 59)     # #1E293B - Deep Charcoal for High Readability
MUTED_TEXT = RGBColor(71, 85, 105)   # #475569 - Secondary Body Text
LIGHT_GRAY = RGBColor(241, 245, 249) # #F1F5F9 - Subtle Panel Fills (Used Sparingly)
BORDER_GRAY = RGBColor(203, 213, 225)# #CBD5E1 - 1pt Crisp Borders
WHITE = RGBColor(255, 255, 255)

# Semantic Colors (Used strictly for status/comparison)
RED_TEXT = RGBColor(185, 28, 28)     # #B91C1C
RED_BG = RGBColor(254, 242, 242)     # #FEF2F2
RED_BORDER = RGBColor(239, 68, 68)   # #EF4444

GREEN_TEXT = RGBColor(21, 128, 61)   # #15803D
GREEN_BG = RGBColor(240, 253, 244)   # #F0FDF4
GREEN_BORDER = RGBColor(34, 197, 94) # #22C55E

AMBER_TEXT = RGBColor(180, 83, 9)    # #B45309
AMBER_BG = RGBColor(254, 243, 199)   # #FEF3C7
AMBER_BORDER = RGBColor(245, 158, 11)# #F59E0B


# ---------------------------------------------------------------------------
# CORE HELPERS
# ---------------------------------------------------------------------------
def add_header(slide, section_label, title_text):
    """Clean academic slide header without decorative clutter."""
    # Eyebrow / Section category
    tb_eye = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.35))
    tf_eye = tb_eye.text_frame
    tf_eye.margin_left = tf_eye.margin_top = tf_eye.margin_right = tf_eye.margin_bottom = 0
    p_eye = tf_eye.paragraphs[0]
    p_eye.text = section_label.upper()
    p_eye.font.name = 'Arial'
    p_eye.font.size = Pt(18)
    p_eye.font.bold = True
    p_eye.font.color.rgb = BLUE

    # Slide Title
    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.733), Inches(0.55))
    tf_title = tb_title.text_frame
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = 'Arial'
    p_title.font.size = Pt(32)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY


def add_footer(slide, current_slide, total_slides=10):
    """Crisp minimal footer with project name and slide number."""
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.8), Inches(6.85), Inches(11.733), Inches(0.015)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = BORDER_GRAY
    line.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(0.8), Inches(6.92), Inches(9.0), Inches(0.35))
    tf = tb.text_frame
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "Campus Complaint & Maintenance Management System  |  Software Engineering Lab"
    p.font.name = 'Arial'
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = MUTED_TEXT

    tb_r = slide.shapes.add_textbox(Inches(10.0), Inches(6.92), Inches(2.533), Inches(0.35))
    tf_r = tb_r.text_frame
    tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0
    p_r = tf_r.paragraphs[0]
    p_r.alignment = PP_ALIGN.RIGHT
    p_r.text = f"Slide {current_slide} of {total_slides}"
    p_r.font.name = 'Arial'
    p_r.font.size = Pt(16)
    p_r.font.bold = True
    p_r.font.color.rgb = BLUE


def add_rect_box(slide, left, top, width, height, text, bg_color=WHITE, border_color=BORDER_GRAY, text_color=NAVY, font_size=18, bold=True):
    """Simple clean rectangular diagram box (no heavy rounded corners)."""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.5)
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = PP_ALIGN.CENTER
    p.font.name = 'Arial'
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = text_color
    return shape


def add_arrow_right(slide, left, top, width=0.35, height=0.22, color=BLUE):
    """Clean directional right arrow."""
    arrow = slide.shapes.add_shape(
        MSO_SHAPE.RIGHT_ARROW,
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = color
    arrow.line.fill.background()
    return arrow


def add_arrow_down(slide, left, top, width=0.22, height=0.35, color=BLUE):
    """Clean directional down arrow."""
    arrow = slide.shapes.add_shape(
        MSO_SHAPE.DOWN_ARROW,
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = color
    arrow.line.fill.background()
    return arrow


# ---------------------------------------------------------------------------
# MAIN SLIDE BUILDER
# ---------------------------------------------------------------------------
def build_all_slides():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1 — TITLE (Clean Academic Title Slide, No Card Clutter)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)

    # Left vertical accent line
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.3), Inches(0.12), Inches(4.8))
    bar.fill.solid(); bar.fill.fore_color.rgb = BLUE
    bar.line.fill.background()

    # Main Title Text Box
    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(11.3), Inches(4.9))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0

    p = tf1.paragraphs[0]
    p.text = "23CS4219 — SOFTWARE ENGINEERING LABORATORY"
    p.font.name = 'Arial'; p.font.size = Pt(20); p.font.bold = True; p.font.color.rgb = BLUE
    p.space_after = Pt(12)

    p = tf1.add_paragraph()
    p.text = "Campus Complaint & Maintenance\nManagement System"
    p.font.name = 'Arial'; p.font.size = Pt(36); p.font.bold = True; p.font.color.rgb = NAVY
    p.space_after = Pt(10)

    p = tf1.add_paragraph()
    p.text = "A Role-Based Full-Stack Web Application for Institutional Facility Grievance Tracking"
    p.font.name = 'Arial'; p.font.size = Pt(22); p.font.color.rgb = MUTED_TEXT
    p.space_after = Pt(26)

    # Subtle Visual Workflow Tag (Complaint -> Triage -> Resolution)
    p = tf1.add_paragraph()
    r = p.add_run(); r.text = "CORE WORKFLOW:  "; r.font.bold = True; r.font.size = Pt(18); r.font.color.rgb = NAVY
    r = p.add_run(); r.text = "Student Grievance Lodging  →  Administrative Triage  →  Technician Work Orders  →  Audited Resolution"; r.font.size = Pt(18); r.font.color.rgb = BLUE
    p.space_after = Pt(24)

    # Student & Institutional Metadata
    meta = [
        ("Student Name:", "Karthikeyan Gullipalli (Roll No: [ROLL NUMBER])"),
        ("Course & Dept:", "B.Tech CSE  |  Department of Computer Science and Engineering"),
        ("Institution:", "Anil Neerukonda Institute of Technology & Sciences (ANITS)"),
        ("Faculty Guide:", "[GUIDE NAME]  |  Academic Year: 2024–2025")
    ]
    for label, val in meta:
        p = tf1.add_paragraph()
        p.space_before = Pt(4)
        r1 = p.add_run(); r1.text = f"{label:16} "; r1.font.bold = True; r1.font.size = Pt(19); r1.font.color.rgb = NAVY
        r2 = p.add_run(); r2.text = val; r2.font.size = Pt(19); r2.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 2 — PROBLEM & MOTIVATION (Visual Vertical Comparison)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "1. Problem & Motivation", "Traditional Paper Process vs. Proposed CCMS System")
    add_footer(s2, 2)

    # LEFT: Traditional Process (Vertical Flow)
    tb_lh = s2.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(5.5), Inches(0.4))
    tb_lh.text_frame.margin_left = tb_lh.text_frame.margin_top = 0
    p = tb_lh.text_frame.paragraphs[0]; p.text = "Traditional Process (Manual)"
    p.font.name = 'Arial'; p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = RED_TEXT

    trad_steps = ["Paper Register", "Physical Counter", "Verbal Work Order", "No Tracking"]
    trad_top = 1.95
    for idx, step in enumerate(trad_steps):
        add_rect_box(s2, 0.8, trad_top + idx * 0.95, 4.8, 0.6, step, bg_color=RED_BG, border_color=RED_BORDER, text_color=RED_TEXT, font_size=19)
        if idx < len(trad_steps) - 1:
            add_arrow_down(s2, 3.1, trad_top + idx * 0.95 + 0.62, width=0.2, height=0.3, color=RED_BORDER)

    # RIGHT: Proposed Campus Complaint System (Vertical Flow)
    tb_rh = s2.shapes.add_textbox(Inches(6.8), Inches(1.4), Inches(5.7), Inches(0.4))
    tb_rh.text_frame.margin_left = tb_rh.text_frame.margin_top = 0
    p = tb_rh.text_frame.paragraphs[0]; p.text = "Proposed System (CCMS Web Portal)"
    p.font.name = 'Arial'; p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = GREEN_TEXT

    prop_steps = ["Web Portal (24/7 Access)", "Admin Verification", "Staff Assignment", "Status Tracking", "Resolution & Feedback"]
    prop_top = 1.95
    for idx, step in enumerate(prop_steps):
        add_rect_box(s2, 6.8, prop_top + idx * 0.74, 5.7, 0.52, step, bg_color=GREEN_BG, border_color=GREEN_BORDER, text_color=GREEN_TEXT, font_size=18)
        if idx < len(prop_steps) - 1:
            add_arrow_down(s2, 9.55, prop_top + idx * 0.74 + 0.53, width=0.18, height=0.2, color=GREEN_BORDER)

    # BOTTOM: Major Problems Solved (Clean horizontal banner)
    banner = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(5.85), Inches(11.733), Inches(0.75))
    banner.fill.solid(); banner.fill.fore_color.rgb = LIGHT_GRAY
    banner.line.color.rgb = BORDER_GRAY; banner.line.width = Pt(1.5)
    tf_b = banner.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.alignment = PP_ALIGN.CENTER
    r1 = p_b.add_run(); r1.text = "Core Bottlenecks Eliminated:   "; r1.font.bold = True; r1.font.size = Pt(20); r1.font.color.rgb = NAVY
    r2 = p_b.add_run(); r2.text = "No Tracking  →  No Accountability  →  No Centralized Records"; r2.font.bold = True; r2.font.size = Pt(20); r2.font.color.rgb = RED_TEXT

    # =========================================================================
    # SLIDE 3 — SOFTWARE ENGINEERING APPROACH (SDLC Flow + Traceability)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "2. Software Engineering Approach", "SDLC Progression & Requirements Traceability")
    add_footer(s3, 3)

    # TOP: Clean SDLC Flow (Requirements -> Design -> Implementation -> Security -> Testing -> Maintenance)
    sdlc_y = 1.45
    sdlc_steps = [
        ("Requirements", 0.8, 1.7),
        ("Design", 2.8, 1.7),
        ("Implementation", 4.8, 1.7),
        ("Security", 6.8, 1.7),
        ("Testing", 8.8, 1.7),
        ("Maintenance", 10.8, 1.733)
    ]
    for idx, (st_name, sx, sw) in enumerate(sdlc_steps):
        add_rect_box(s3, sx, sdlc_y, sw, 0.65, st_name, bg_color=NAVY, border_color=NAVY, text_color=WHITE, font_size=19)
        if idx < len(sdlc_steps) - 1:
            add_arrow_right(s3, sx + sw + 0.05, sdlc_y + 0.2, width=0.2, height=0.22, color=BLUE)

    # SECTION TITLE: Requirement-to-Implementation Mapping
    tb_map_title = s3.shapes.add_textbox(Inches(0.8), Inches(2.4), Inches(11.733), Inches(0.4))
    tb_map_title.text_frame.margin_left = tb_map_title.text_frame.margin_top = 0
    p = tb_map_title.text_frame.paragraphs[0]; p.text = "Requirement → Implementation Traceability Mapping"
    p.font.name = 'Arial'; p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = NAVY

    # MAPPINGS (Clean 2-Column Table / List Layout)
    req_mappings = [
        ("Secure Access", "Stateless JWT authentication + bcryptjs hashing + verifyToken middleware"),
        ("Complaint Lodging", "Dynamic React form + campus category & room mapping + Multer photo upload"),
        ("Admin Control", "Centralized administrative dashboard with status filters + staff assignment"),
        ("Audited Lifecycle", "Strict server-side Finite State Machine validator + immutable complaint_updates log"),
        ("Technician Execution", "Dedicated work order queue with real-time status progression (IN_PROGRESS → RESOLVED)"),
        ("Quality Feedback", "Post-resolution 1 to 5 star rating submission + reopening mechanism for recurring issues")
    ]
    
    tb_map = s3.shapes.add_textbox(Inches(0.8), Inches(2.9), Inches(11.733), Inches(3.7))
    tf_map = tb_map.text_frame
    tf_map.word_wrap = True
    tf_map.margin_left = tf_map.margin_top = 0

    for idx, (req, impl) in enumerate(req_mappings):
        p = tf_map.paragraphs[0] if idx == 0 else tf_map.add_paragraph()
        if idx > 0: p.space_before = Pt(10)
        r1 = p.add_run(); r1.text = f"• {req:25} "; r1.font.bold = True; r1.font.size = Pt(20); r1.font.color.rgb = BLUE
        r_arr = p.add_run(); r_arr.text = "→   "; r_arr.font.bold = True; r_arr.font.size = Pt(20); r_arr.font.color.rgb = NAVY
        r2 = p.add_run(); r2.text = impl; r2.font.size = Pt(20); r2.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 4 — SYSTEM ARCHITECTURE (Visual Tier Flow + Side Auth + 3 Concepts)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "3. System Architecture", "Decoupled 3-Tier Layered Architecture with Stateless API Security")
    add_footer(s4, 4)

    # LEFT: Clear Vertical Architecture Diagram
    arch_left = 0.8
    arch_w = 6.2
    
    # Layer 1: Users
    add_rect_box(s4, arch_left, 1.45, arch_w, 0.58, "Student  •  Faculty  •  Admin  •  Maintenance Staff", bg_color=WHITE, border_color=NAVY, text_color=NAVY, font_size=18)
    add_arrow_down(s4, arch_left + arch_w/2 - 0.1, 2.05, width=0.2, height=0.25, color=BLUE)

    # Layer 2: Frontend
    add_rect_box(s4, arch_left, 2.32, arch_w, 0.72, "React 18 + Vite Frontend (SPA)\nComponent Hierarchy • Tailwind CSS • Axios Client", bg_color=WHITE, border_color=BLUE, text_color=NAVY, font_size=18)
    add_arrow_down(s4, arch_left + arch_w/2 - 0.1, 3.06, width=0.2, height=0.25, color=BLUE)

    # Layer 3: REST API Server
    add_rect_box(s4, arch_left, 3.33, arch_w, 0.72, "Node.js + Express REST API\nAuthentication • Validation • Multer Upload • State Machine", bg_color=WHITE, border_color=BLUE, text_color=NAVY, font_size=18)
    add_arrow_down(s4, arch_left + arch_w/2 - 0.1, 4.07, width=0.2, height=0.25, color=BLUE)

    # Layer 4: MySQL Database
    add_rect_box(s4, arch_left, 4.34, arch_w, 0.72, "MySQL 8 Relational Database (ccms_db)\n7 Normalized 3NF Tables • InnoDB Engine • Connection Pool", bg_color=NAVY, border_color=NAVY, text_color=WHITE, font_size=18)

    # SIDE FLOW: JWT Authentication (Side flow pointing to API)
    jwt_box = add_rect_box(s4, 4.8, 3.33, 2.1, 0.72, "JWT Auth Sideflow\nverifyToken Guard", bg_color=LIGHT_GRAY, border_color=BLUE, text_color=BLUE, font_size=16)

    # RIGHT: Core Architectural Decisions (Clean & Concise, No Paragraphs)
    tb_arch_txt = s4.shapes.add_textbox(Inches(7.3), Inches(1.45), Inches(5.233), Inches(4.5))
    tf_at = tb_arch_txt.text_frame
    tf_at.word_wrap = True
    tf_at.margin_left = tf_at.margin_top = 0

    p = tf_at.paragraphs[0]; p.text = "Key Architectural Principles"
    p.font.name = 'Arial'; p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = NAVY
    p.space_after = Pt(16)

    arch_concepts = [
        ("Separation of Concerns", "Presentation layer is strictly decoupled from storage. The client never accesses MySQL directly; all operations are governed by validated REST endpoints."),
        ("Stateless JWT Authorization", "Eliminates server session storage. Each request carries a signed HS256 Bearer token, enabling horizontal scaling and high concurrency."),
        ("Relational Integrity & ACID", "Normalized schema with foreign key constraints, atomic transactions, and parameterized SQL queries eliminating SQL injection risks.")
    ]
    for title, desc in arch_concepts:
        p = tf_at.add_paragraph()
        p.space_before = Pt(14)
        r1 = p.add_run(); r1.text = f"• {title}\n"; r1.font.bold = True; r1.font.size = Pt(21); r1.font.color.rgb = BLUE
        r2 = p.add_run(); r2.text = desc; r2.font.size = Pt(19); r2.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 5 — COMPLAINT WORKFLOW (Large FSM Flow + 3 Roles Underneath)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "4. Complaint Workflow & Lifecycle", "Finite State Machine Enforcing Audited Status Progression")
    add_footer(s5, 5)

    # MAIN VISUAL: Large Horizontal FSM Flow
    fsm_y = 1.6
    fsm_nodes = [
        ("NEW", 0.8, 1.4),
        ("VERIFIED", 2.7, 1.6),
        ("ASSIGNED", 4.8, 1.6),
        ("IN PROGRESS", 6.9, 1.8),
        ("RESOLVED", 9.2, 1.6),
        ("CLOSED", 11.3, 1.233)
    ]
    for idx, (name, x, w) in enumerate(fsm_nodes):
        add_rect_box(s5, x, fsm_y, w, 0.7, name, bg_color=NAVY, border_color=NAVY, text_color=WHITE, font_size=19)
        if idx < len(fsm_nodes) - 1:
            add_arrow_right(s5, x + w + 0.08, fsm_y + 0.22, width=0.24, height=0.22, color=BLUE)

    # EXCEPTION BRANCHES (REJECTED and REOPENED)
    add_rect_box(s5, 2.7, 2.65, 2.2, 0.55, "REJECTED (Invalid)", bg_color=RED_BG, border_color=RED_BORDER, text_color=RED_TEXT, font_size=17)
    add_arrow_down(s5, 3.7, 2.32, width=0.18, height=0.3, color=RED_BORDER)

    add_rect_box(s5, 10.3, 2.65, 2.233, 0.55, "REOPENED (Persistent)", bg_color=AMBER_BG, border_color=AMBER_BORDER, text_color=AMBER_TEXT, font_size=17)
    add_arrow_down(s5, 11.3, 2.32, width=0.18, height=0.3, color=AMBER_BORDER)

    # THREE ROLES UNDERNEATH (Submit -> Track -> Rate, etc.)
    role_y = 3.65
    role_h = 2.8
    col_w = 3.71

    roles = [
        ("Student / Faculty", "Submit  →  Track  →  Rate", [
            "Lodges complaint with campus building & room.",
            "Attaches optional photographic evidence.",
            "Monitors real-time status progression.",
            "Submits 1–5 star rating upon resolution."
        ], BLUE),
        ("Administrator", "Verify  →  Assign  →  Close", [
            "Reviews complaint details and authenticity.",
            "Accepts (VERIFIED) or dismisses (REJECTED).",
            "Assigns task to active technician.",
            "Reviews repair notes & confirms closure."
        ], NAVY),
        ("Maintenance Staff", "Accept  →  Work  →  Resolve", [
            "Accesses assigned work orders queue.",
            "Begins physical remediation (IN PROGRESS).",
            "Logs diagnostic & repair remarks.",
            "Marks complaint successfully RESOLVED."
        ], GREEN_TEXT)
    ]
    for idx, (r_name, r_flow, r_bullets, r_col) in enumerate(roles):
        rx = 0.8 + idx * (col_w + 0.3)
        # Clean white panel
        panel = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(rx), Inches(role_y), Inches(col_w), Inches(role_h))
        panel.fill.solid(); panel.fill.fore_color.rgb = LIGHT_GRAY
        panel.line.color.rgb = BORDER_GRAY; panel.line.width = Pt(1.5)

        tb_r = s5.shapes.add_textbox(Inches(rx + 0.2), Inches(role_y + 0.15), Inches(col_w - 0.4), Inches(role_h - 0.3))
        tf_r = tb_r.text_frame; tf_r.word_wrap = True; tf_r.margin_left = tf_r.margin_top = 0
        
        p = tf_r.paragraphs[0]; p.text = r_name
        p.font.name = 'Arial'; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = r_col
        
        p2 = tf_r.add_paragraph(); p2.space_before = Pt(4)
        p2.text = r_flow; p2.font.name = 'Arial'; p2.font.size = Pt(19); p2.font.bold = True; p2.font.color.rgb = NAVY

        for b in r_bullets:
            p_b = tf_r.add_paragraph(); p_b.space_before = Pt(5)
            p_b.text = "• " + b; p_b.font.name = 'Arial'; p_b.font.size = Pt(18); p_b.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 6 — MAJOR MODULES & TECHNOLOGY STACK (Two Clean Distinct Areas)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "5. Major Modules & Technology Stack", "Functional System Modules & Production Software Stack")
    add_footer(s6, 6)

    # LEFT AREA: SYSTEM MODULES (Vertical Flow)
    tb_mh = s6.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(5.5), Inches(0.4))
    tb_mh.text_frame.margin_left = tb_mh.text_frame.margin_top = 0
    p = tb_mh.text_frame.paragraphs[0]; p.text = "System Functional Modules"
    p.font.name = 'Arial'; p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = NAVY

    mod_steps = [
        ("Authentication & RBAC", "Registration, login, JWT token issuance, and role access guards"),
        ("Complaint Lodging", "Dynamic React form, category/room selection, Multer file upload"),
        ("Admin Control Center", "Campus-wide triage, status filters, staff assignment interface"),
        ("Maintenance Work Orders", "Technician task queue, work commencement, resolution remarks"),
        ("Audit History & Feedback", "Append-only status history in complaint_updates + student rating")
    ]
    mod_top = 1.95
    for idx, (m_name, m_sub) in enumerate(mod_steps):
        add_rect_box(s6, 0.8, mod_top + idx * 0.95, 5.5, 0.62, f"{m_name}\n({m_sub})", bg_color=WHITE, border_color=BLUE, text_color=NAVY, font_size=17, bold=True)
        if idx < len(mod_steps) - 1:
            add_arrow_down(s6, 3.45, mod_top + idx * 0.95 + 0.64, width=0.2, height=0.28, color=BLUE)

    # RIGHT AREA: TECHNOLOGY STACK (Clean Categorized Groups)
    tb_th = s6.shapes.add_textbox(Inches(6.8), Inches(1.4), Inches(5.7), Inches(0.4))
    tb_th.text_frame.margin_left = tb_th.text_frame.margin_top = 0
    p = tb_th.text_frame.paragraphs[0]; p.text = "Production Technology Stack"
    p.font.name = 'Arial'; p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = NAVY

    stack_groups = [
        ("Frontend Tier", "React 18  •  Vite 5  •  Tailwind CSS  •  Axios  •  React Router"),
        ("Backend Tier", "Node.js 18 LTS  •  Express 4.19  •  express-validator  •  Multer"),
        ("Database & Storage", "MySQL 8.0  •  mysql2 Connection Pool  •  InnoDB Engine (7 Tables)"),
        ("Security & Testing", "JSON Web Tokens (JWT HS256)  •  bcryptjs (10 rounds)  •  Playwright")
    ]
    stack_top = 1.95
    for idx, (cat_name, tech_list) in enumerate(stack_groups):
        panel = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(stack_top + idx * 1.18), Inches(5.733), Inches(0.95))
        panel.fill.solid(); panel.fill.fore_color.rgb = LIGHT_GRAY
        panel.line.color.rgb = BORDER_GRAY; panel.line.width = Pt(1.5)

        tb_p = s6.shapes.add_textbox(Inches(7.0), Inches(stack_top + idx * 1.18 + 0.1), Inches(5.333), Inches(0.75))
        tf_p = tb_p.text_frame; tf_p.word_wrap = True; tf_p.margin_left = tf_p.margin_top = 0
        p = tf_p.paragraphs[0]; p.text = cat_name
        p.font.name = 'Arial'; p.font.size = Pt(21); p.font.bold = True; p.font.color.rgb = NAVY
        p2 = tf_p.add_paragraph(); p2.space_before = Pt(4)
        p2.text = tech_list; p2.font.name = 'Arial'; p2.font.size = Pt(19); p2.font.color.rgb = BLUE

    # =========================================================================
    # SLIDE 7 — DATABASE DESIGN (Simplified ER Diagram + 3 Concepts)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "6. Database Design", "Simplified Entity-Relationship Architecture & Data Integrity")
    add_footer(s7, 7)

    # SIMPLIFIED ER DIAGRAM
    # Row 1: Users -> Complaints (Central) <- Categories / Locations
    add_rect_box(s7, 0.8, 1.5, 3.3, 1.15, "USERS\nid (PK) • name • email\nrole • department", bg_color=WHITE, border_color=NAVY, text_color=NAVY, font_size=18)
    
    add_arrow_right(s7, 4.25, 1.95, width=0.35, height=0.22, color=BLUE)

    add_rect_box(s7, 4.8, 1.5, 3.733, 1.15, "COMPLAINTS (Core Entity)\nid (PK) • complaint_number • user_id (FK)\ncategory_id (FK) • location_id (FK) • status", bg_color=NAVY, border_color=NAVY, text_color=WHITE, font_size=18)

    add_arrow_right(s7, 8.7, 1.95, width=0.35, height=0.22, color=BLUE)

    add_rect_box(s7, 9.233, 1.5, 3.3, 1.15, "LOCATIONS & CATEGORIES\nbuilding • floor • room\ncategory_name", bg_color=WHITE, border_color=NAVY, text_color=NAVY, font_size=18)

    # Row 2: Complaints connects to Assignments, Updates, Feedback
    add_arrow_down(s7, 2.4, 2.75, width=0.22, height=0.3, color=BLUE)
    add_rect_box(s7, 0.8, 3.15, 3.3, 1.15, "COMPLAINT_ASSIGNMENTS\nstaff_id (FK) • assigned_by (FK)\nassigned_at • notes", bg_color=WHITE, border_color=BLUE, text_color=BLUE, font_size=18)

    add_arrow_down(s7, 6.55, 2.75, width=0.22, height=0.3, color=BLUE)
    add_rect_box(s7, 4.8, 3.15, 3.733, 1.15, "COMPLAINT_UPDATES (Audit Log)\nold_status • new_status\nremarks • updated_by (FK) • created_at", bg_color=WHITE, border_color=BLUE, text_color=BLUE, font_size=18)

    add_arrow_down(s7, 10.7, 2.75, width=0.22, height=0.3, color=BLUE)
    add_rect_box(s7, 9.233, 3.15, 3.3, 1.15, "FEEDBACK\ncomplaint_id (FK) • user_id (FK)\nrating (1–5) • comments", bg_color=WHITE, border_color=BLUE, text_color=BLUE, font_size=18)

    # BOTTOM: Three Database Concepts (3NF, Referential Integrity, Immutable Audit Trail)
    b_top = 4.65
    b_h = 1.95
    col_w = 3.71
    db_concepts = [
        ("3NF Normalization", "Redundancy eliminated across all tables. Campus buildings, rooms, and issue categories are maintained as independent master entities.", NAVY),
        ("Referential Integrity", "Foreign key constraints with ON UPDATE / ON DELETE rules guarantee that tickets and history always map to valid users and rooms.", BLUE),
        ("Immutable Audit Trail", "The complaint_updates table operates as an append-only transaction log, recording every status transition with operator IDs and timestamps.", GREEN_TEXT)
    ]
    for idx, (title, desc, color) in enumerate(db_concepts):
        bx = 0.8 + idx * (col_w + 0.3)
        panel = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(bx), Inches(b_top), Inches(col_w), Inches(b_h))
        panel.fill.solid(); panel.fill.fore_color.rgb = LIGHT_GRAY
        panel.line.color.rgb = BORDER_GRAY; panel.line.width = Pt(1.5)

        tb = s7.shapes.add_textbox(Inches(bx + 0.2), Inches(b_top + 0.12), Inches(col_w - 0.4), Inches(b_h - 0.24))
        tf = tb.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]; p.text = title
        p.font.name = 'Arial'; p.font.size = Pt(21); p.font.bold = True; p.font.color.rgb = color
        p2 = tf.add_paragraph(); p2.space_before = Pt(6)
        p2.text = desc; p2.font.name = 'Arial'; p2.font.size = Pt(18); p2.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 8 — APPLICATION SCREENSHOTS (Large Screenshots + Clear Callouts)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "7. Application Screenshots", "Authentic User Interfaces from the Running CCMS Application")
    add_footer(s8, 8)

    # Two Large Screenshots Side-by-Side
    img_w = 5.6
    img_h = 3.5
    img_y = 1.45

    # Screen 1: Admin Dashboard
    if os.path.exists("docs/screenshots/07_admin_dashboard.png"):
        s8.shapes.add_picture("docs/screenshots/07_admin_dashboard.png", Inches(0.8), Inches(img_y), width=Inches(img_w))
    
    tb_c1 = s8.shapes.add_textbox(Inches(0.8), Inches(img_y + img_h + 0.15), Inches(img_w), Inches(1.5))
    tf_c1 = tb_c1.text_frame; tf_c1.word_wrap = True; tf_c1.margin_left = tf_c1.margin_top = 0
    p = tf_c1.paragraphs[0]; p.text = "1. Administrator Control Center"
    p.font.name = 'Arial'; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = NAVY
    p2 = tf_c1.add_paragraph(); p2.space_before = Pt(4)
    p2.text = "• Real-Time Campus KPIs: Total, open, resolved, and critical ticket counts.\n• Interactive Triage: Instant search, category filters, and verify/reject controls."
    p2.font.name = 'Arial'; p2.font.size = Pt(19); p2.font.color.rgb = DARK_TEXT

    # Screen 2: Technician Work Orders
    if os.path.exists("docs/screenshots/15_maintenance_tasks.png"):
        s8.shapes.add_picture("docs/screenshots/15_maintenance_tasks.png", Inches(6.933), Inches(img_y), width=Inches(img_w))

    tb_c2 = s8.shapes.add_textbox(Inches(6.933), Inches(img_y + img_h + 0.15), Inches(img_w), Inches(1.5))
    tf_c2 = tb_c2.text_frame; tf_c2.word_wrap = True; tf_c2.margin_left = tf_c2.margin_top = 0
    p = tf_c2.paragraphs[0]; p.text = "2. Technician Work Order Queue"
    p.font.name = 'Arial'; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = GREEN_TEXT
    p2 = tf_c2.add_paragraph(); p2.space_before = Pt(4)
    p2.text = "• Room-Level Dispatching: Displays exact campus building, floor, room, and urgency.\n• Work Execution: Single-click 'Start Work' and diagnostic resolution remarks submission."
    p2.font.name = 'Arial'; p2.font.size = Pt(19); p2.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 9 — TESTING & VERIFICATION (Testing Evidence + Clean Results Table)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "8. Testing & Quality Verification", "Rigorous Multi-Level Verification with 100% Pass Rate")
    add_footer(s9, 9)

    # LEFT: Testing Categories & Basis Path Analysis
    tb_th = s9.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(5.0), Inches(5.2))
    tf_th = tb_th.text_frame; tf_th.word_wrap = True; tf_th.margin_left = tf_th.margin_top = 0
    
    p = tf_th.paragraphs[0]; p.text = "Testing Methodology"
    p.font.name = 'Arial'; p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = NAVY
    p.space_after = Pt(12)

    tests_data = [
        ("Unit Testing", "Validated bcrypt password salting, token signing/verification, and unique CMP-ID generators."),
        ("Basis Path Testing", "Mapped Cyclomatic Complexity V(G) = 11 for statusController.js; validated all legal and illegal transition paths."),
        ("Role Access Testing", "Verified that student tokens cannot access administrative or technician endpoints (HTTP 403 Forbidden)."),
        ("System Integration", "Automated browser validation via Playwright confirming end-to-end user journeys.")
    ]
    for t_name, t_desc in tests_data:
        p = tf_th.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run(); r1.text = f"• {t_name}:\n"; r1.font.bold = True; r1.font.size = Pt(20); r1.font.color.rgb = BLUE
        r2 = p.add_run(); r2.text = t_desc; r2.font.size = Pt(19); r2.font.color.rgb = DARK_TEXT

    p_b = tf_th.add_paragraph(); p_b.space_before = Pt(16)
    r_b = p_b.add_run(); r_b.text = "✓ 30 / 30 Executed Test Cases PASSED (100%)"; r_b.font.bold = True; r_b.font.size = Pt(20); r_b.font.color.rgb = GREEN_TEXT

    # RIGHT: Executed Test Results Table
    t_shape = s9.shapes.add_table(7, 4, Inches(6.0), Inches(1.45), Inches(6.533), Inches(5.1))
    tbl = t_shape.table
    tbl.columns[0].width = Inches(1.0)
    tbl.columns[1].width = Inches(2.1)
    tbl.columns[2].width = Inches(2.433)
    tbl.columns[3].width = Inches(1.0)

    test_headers = ["Test ID", "Scenario Evaluated", "Observed Result", "Status"]
    for c_idx, h_text in enumerate(test_headers):
        cell = tbl.cell(0, c_idx)
        cell.fill.solid(); cell.fill.fore_color.rgb = NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h_text; p.font.name = 'Arial'; p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    test_rows = [
        ["TC-01", "Administrator Authentication", "HTTP 200; JWT issued; Admin access", "PASS"],
        ["TC-02", "Student User Authentication", "HTTP 200; JWT issued; Student view", "PASS"],
        ["TC-03", "Complaint Lodging with Photo", "HTTP 201; CMP-ID generated in DB", "PASS"],
        ["TC-04", "Illegal Transition (NEW→CLOSED)", "HTTP 400 Bad Request; FSM guarded", "PASS"],
        ["TC-05", "Technician Work Assignment", "HTTP 200; Dispatched to staff queue", "PASS"],
        ["TC-06", "Unauthorized Endpoint Access", "HTTP 403 Forbidden; Access blocked", "PASS"]
    ]
    for r_idx, row_data in enumerate(test_rows):
        for c_idx, val in enumerate(row_data):
            cell = tbl.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 0 else LIGHT_GRAY
            p = cell.text_frame.paragraphs[0]
            p.text = val; p.font.name = 'Arial'; p.font.size = Pt(18)
            if c_idx == 0:
                p.font.bold = True; p.font.color.rgb = NAVY; p.alignment = PP_ALIGN.CENTER
            elif c_idx == 3:
                p.font.bold = True; p.font.color.rgb = GREEN_TEXT; p.alignment = PP_ALIGN.CENTER
            else:
                p.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 10 — CONCLUSION, LIMITATIONS & FUTURE SCOPE
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "9. Conclusion & Future Scope", "System Achievements, Practical Limitations & Future Roadmap")
    add_footer(s10, 10)

    # 3 Clean Open Columns
    col_w = 3.71
    col_y = 1.45
    col_h = 4.45

    # Column 1: Achievements
    panel1 = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(col_y), Inches(col_w), Inches(col_h))
    panel1.fill.solid(); panel1.fill.fore_color.rgb = GREEN_BG
    panel1.line.color.rgb = GREEN_BORDER; panel1.line.width = Pt(1.5)

    tb1 = s10.shapes.add_textbox(Inches(1.0), Inches(col_y + 0.15), Inches(col_w - 0.4), Inches(col_h - 0.3))
    tf1 = tb1.text_frame; tf1.word_wrap = True; tf1.margin_left = tf1.margin_top = 0
    p = tf1.paragraphs[0]; p.text = "What CCMS Achieved"
    p.font.name = 'Arial'; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = GREEN_TEXT
    achievements = [
        "Eliminated error-prone manual logbooks with a 24/7 web-based grievance portal.",
        "Enforced strict role-based access across Student, Faculty, Staff, and Admin.",
        "Implemented an audited Finite State Machine preventing illegal status jumps.",
        "Established an immutable audit log ensuring complete administrative transparency."
    ]
    for ach in achievements:
        p = tf1.add_paragraph(); p.space_before = Pt(8)
        p.text = "✓ " + ach; p.font.size = Pt(19); p.font.color.rgb = DARK_TEXT

    # Column 2: Current Limitations
    panel2 = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.81), Inches(col_y), Inches(col_w), Inches(col_h))
    panel2.fill.solid(); panel2.fill.fore_color.rgb = AMBER_BG
    panel2.line.color.rgb = AMBER_BORDER; panel2.line.width = Pt(1.5)

    tb2 = s10.shapes.add_textbox(Inches(5.01), Inches(col_y + 0.15), Inches(col_w - 0.4), Inches(col_h - 0.3))
    tf2 = tb2.text_frame; tf2.word_wrap = True; tf2.margin_left = tf2.margin_top = 0
    p = tf2.paragraphs[0]; p.text = "Current Limitations"
    p.font.name = 'Arial'; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = AMBER_TEXT
    limitations = [
        "Notification delivery relies on active web sessions (no external SMS/Email gateway).",
        "Evidence images stored on local server filesystem rather than cloud object storage.",
        "Technician assignment requires manual administrative allocation."
    ]
    for lim in limitations:
        p = tf2.add_paragraph(); p.space_before = Pt(8)
        p.text = "• " + lim; p.font.size = Pt(19); p.font.color.rgb = DARK_TEXT

    # Column 3: Future Roadmap
    panel3 = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.82), Inches(col_y), Inches(col_w), Inches(col_h))
    panel3.fill.solid(); panel3.fill.fore_color.rgb = LIGHT_GRAY
    panel3.line.color.rgb = BLUE; panel3.line.width = Pt(1.5)

    tb3 = s10.shapes.add_textbox(Inches(9.02), Inches(col_y + 0.15), Inches(col_w - 0.4), Inches(col_h - 0.3))
    tf3 = tb3.text_frame; tf3.word_wrap = True; tf3.margin_left = tf3.margin_top = 0
    p = tf3.paragraphs[0]; p.text = "Future Roadmap"
    p.font.name = 'Arial'; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = BLUE
    future = [
        "Integration of Nodemailer (SMTP) and Twilio (SMS) for automated push alerts.",
        "Migration of evidence storage to Amazon S3 / Cloudinary cloud buckets.",
        "Development of cross-platform mobile app using React Native.",
        "Automated technician dispatching based on active workload and trade skills."
    ]
    for fut in future:
        p = tf3.add_paragraph(); p.space_before = Pt(8)
        p.text = "→ " + fut; p.font.size = Pt(19); p.font.color.rgb = DARK_TEXT

    # BOTTOM BANNER: Thank You & Viva Q&A
    tb_thank = s10.shapes.add_textbox(Inches(0.8), Inches(6.08), Inches(11.733), Inches(0.65))
    tf_thank = tb_thank.text_frame; tf_thank.margin_left = tf_thank.margin_top = 0
    p_thank = tf_thank.paragraphs[0]
    p_thank.alignment = PP_ALIGN.CENTER
    p_thank.text = "Thank You  |  Questions & Answers"
    p_thank.font.name = 'Arial'; p_thank.font.size = Pt(26); p_thank.font.bold = True; p_thank.font.color.rgb = NAVY

    # Save presentation
    output_path = "Campus_Complaint_Management_System_Mini_Project_Presentation.pptx"
    prs.save(output_path)
    print(f"Clean Academic Presentation successfully generated at: {output_path}")


if __name__ == "__main__":
    build_all_slides()
