import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# ---------------------------------------------------------------------------
# COLOR PALETTE (Strict Academic Palette - White Canvas & High Contrast)
# ---------------------------------------------------------------------------
NAVY = RGBColor(15, 23, 42)          # #0F172A - Deep Slate Navy (Primary Titles & Headers)
BLUE = RGBColor(37, 99, 235)         # #2563EB - Academic Blue (Accents, Markers, Arrows)
DARK = RGBColor(30, 41, 59)          # #1E293B - High-Contrast Body Text
MUTED = RGBColor(71, 85, 105)        # #475569 - Secondary Descriptions
BORDER = RGBColor(203, 213, 225)     # #CBD5E1 - 1pt Diagram Border
LIGHT_BG = RGBColor(248, 250, 252)   # #F8FAFC - Very Subtle Panel Tint (Used Sparingly)
WHITE = RGBColor(255, 255, 255)

# Semantic Accents (Used only for status / comparison)
RED_TEXT = RGBColor(185, 28, 28)     # #B91C1C
GREEN_TEXT = RGBColor(21, 128, 61)   # #15803D
AMBER_TEXT = RGBColor(180, 83, 9)    # #B45309


# ---------------------------------------------------------------------------
# CORE HELPERS (Typography-Driven, Minimal Decoration)
# ---------------------------------------------------------------------------
def add_slide_header(slide, section_label, title_text):
    """Clean, compact header: 16pt category eyebrow + 28pt bold title. Leaves ample whitespace!"""
    # Eyebrow (e.g., '01 — PROBLEM')
    tb_eye = slide.shapes.add_textbox(Inches(1.0), Inches(0.42), Inches(11.333), Inches(0.3))
    tf_eye = tb_eye.text_frame
    tf_eye.margin_left = tf_eye.margin_top = tf_eye.margin_right = tf_eye.margin_bottom = 0
    p_eye = tf_eye.paragraphs[0]
    p_eye.text = section_label.upper()
    p_eye.font.name = 'Calibri'
    p_eye.font.size = Pt(16)
    p_eye.font.bold = True
    p_eye.font.color.rgb = BLUE

    # Main Title
    tb_title = slide.shapes.add_textbox(Inches(1.0), Inches(0.72), Inches(11.333), Inches(0.55))
    tf_title = tb_title.text_frame
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = 'Calibri'
    p_title.font.size = Pt(28)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY


def add_slide_footer(slide, current_slide, total_slides=10):
    """Subtle, professional divider line and bottom text."""
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(1.0), Inches(6.85), Inches(11.333), Inches(0.015)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = BORDER
    line.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(1.0), Inches(6.93), Inches(8.5), Inches(0.32))
    tf = tb.text_frame
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "Campus Complaint & Maintenance Management System  |  Software Engineering Lab"
    p.font.name = 'Calibri'
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = MUTED

    tb_r = slide.shapes.add_textbox(Inches(9.5), Inches(6.93), Inches(2.833), Inches(0.32))
    tf_r = tb_r.text_frame
    tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0
    p_r = tf_r.paragraphs[0]
    p_r.alignment = PP_ALIGN.RIGHT
    p_r.text = f"Slide {current_slide} of {total_slides}"
    p_r.font.name = 'Calibri'
    p_r.font.size = Pt(15)
    p_r.font.bold = True
    p_r.font.color.rgb = BLUE


def add_thin_box(slide, left, top, width, height, text, bg_color=WHITE, border_color=BORDER, text_color=NAVY, font_size=18, bold=True):
    """Simple clean rectangular diagram box (NOT a heavy rounded card)."""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.2)
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = PP_ALIGN.CENTER
    p.font.name = 'Calibri'
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = text_color
    return shape


def add_arrow_right(slide, left, top, width=0.3, height=0.2, color=BLUE):
    arrow = slide.shapes.add_shape(
        MSO_SHAPE.RIGHT_ARROW,
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = color
    arrow.line.fill.background()
    return arrow


def add_arrow_down(slide, left, top, width=0.2, height=0.3, color=BLUE):
    arrow = slide.shapes.add_shape(
        MSO_SHAPE.DOWN_ARROW,
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = color
    arrow.line.fill.background()
    return arrow


# ---------------------------------------------------------------------------
# 10 SLIDES BUILDER
# ---------------------------------------------------------------------------
def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1 — TITLE (Minimal, Open Whitespace, No Cards)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)

    # Left vertical accent line
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.4), Inches(0.08), Inches(4.5))
    bar.fill.solid(); bar.fill.fore_color.rgb = BLUE
    bar.line.fill.background()

    # Left typography block
    tb1 = s1.shapes.add_textbox(Inches(1.3), Inches(1.3), Inches(6.8), Inches(4.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0

    p = tf1.paragraphs[0]
    p.text = "23CS4219 — SOFTWARE ENGINEERING LABORATORY"
    p.font.name = 'Calibri'; p.font.size = Pt(17); p.font.bold = True; p.font.color.rgb = BLUE
    p.space_after = Pt(14)

    p = tf1.add_paragraph()
    p.text = "Campus Complaint &\nMaintenance Management System"
    p.font.name = 'Calibri'; p.font.size = Pt(32); p.font.bold = True; p.font.color.rgb = NAVY
    p.space_after = Pt(12)

    p = tf1.add_paragraph()
    p.text = "Role-Based Full-Stack Web Application for Institutional Facility Grievance Tracking"
    p.font.name = 'Calibri'; p.font.size = Pt(20); p.font.color.rgb = MUTED
    p.space_after = Pt(28)

    meta = [
        ("Student Name:", "Karthikeyan Gullipalli (Roll No: [ROLL NUMBER])"),
        ("Course & Dept:", "B.Tech CSE  |  Department of Computer Science & Engineering"),
        ("Institution:", "Anil Neerukonda Institute of Technology & Sciences (ANITS)"),
        ("Academic Year:", "2024–2025  |  Guide: [GUIDE NAME]")
    ]
    for label, val in meta:
        p = tf1.add_paragraph()
        p.space_before = Pt(4)
        r1 = p.add_run(); r1.text = f"{label:16} "; r1.font.bold = True; r1.font.size = Pt(18); r1.font.color.rgb = NAVY
        r2 = p.add_run(); r2.text = val; r2.font.size = Pt(18); r2.font.color.rgb = DARK

    # Subtle Right-Side Workflow Timeline
    tb_wf = s1.shapes.add_textbox(Inches(8.5), Inches(1.8), Inches(3.8), Inches(4.0))
    tf_wf = tb_wf.text_frame; tf_wf.word_wrap = True; tf_wf.margin_left = tf_wf.margin_top = 0

    p = tf_wf.paragraphs[0]; p.text = "DIGITAL LIFECYCLE"
    p.font.name = 'Calibri'; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = BLUE
    p.space_after = Pt(16)

    flow_steps = [
        ("01", "Grievance Lodging", "Student reports issue with room & photo"),
        ("02", "Administrative Triage", "Verification & staff allocation"),
        ("03", "Technician Dispatch", "Active work order in queue"),
        ("04", "Audited Resolution", "Diagnostic remarks & student rating")
    ]
    for num, step_t, step_d in flow_steps:
        p = tf_wf.add_paragraph(); p.space_before = Pt(8)
        r1 = p.add_run(); r1.text = f"{num}  "; r1.font.bold = True; r1.font.size = Pt(18); r1.font.color.rgb = BLUE
        r2 = p.add_run(); r2.text = f"{step_t}\n"; r2.font.bold = True; r2.font.size = Pt(18); r2.font.color.rgb = NAVY
        r3 = p.add_run(); r3.text = f"     {step_d}"; r3.font.size = Pt(17); r3.font.color.rgb = MUTED

    # =========================================================================
    # SLIDE 2 — PROBLEM (Visual Story: TODAY vs. WITH CCMS)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_slide_header(s2, "01 — PROBLEM", "Why Campus Complaints Need a Digital Workflow")
    add_slide_footer(s2, 2)

    # LEFT SIDE: TODAY (Manual Process)
    tb_l = s2.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(4.6), Inches(0.4))
    tb_l.text_frame.margin_left = tb_l.text_frame.margin_top = 0
    p = tb_l.text_frame.paragraphs[0]; p.text = "TODAY"
    p.font.name = 'Calibri'; p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = RED_TEXT

    # Thin vertical timeline line
    v_line_l = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(2.3), Inches(0.02), Inches(2.9))
    v_line_l.fill.solid(); v_line_l.fill.fore_color.rgb = BORDER
    v_line_l.line.fill.background()

    t_steps = [
        ("Paper Register", "Physical logbooks kept at administrative counters"),
        ("Physical Counter", "In-person reporting limited to office hours"),
        ("Verbal Work Order", "Unrecorded task assignments without SLAs"),
        ("❌ No Tracking", "Lost complaints, zero visibility, delayed repairs")
    ]
    for idx, (title, sub) in enumerate(t_steps):
        # Dot marker
        dot = s2.shapes.add_shape(MSO_SHAPE.OVAL, Inches(1.12), Inches(2.3 + idx * 0.95), Inches(0.18), Inches(0.18))
        dot.fill.solid(); dot.fill.fore_color.rgb = RED_TEXT; dot.line.fill.background()

        tb = s2.shapes.add_textbox(Inches(1.45), Inches(2.2 + idx * 0.95), Inches(4.0), Inches(0.7))
        tf = tb.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]; p.text = title
        p.font.name = 'Calibri'; p.font.size = Pt(20); p.font.bold = True; p.font.color.rgb = NAVY
        p2 = tf.add_paragraph(); p2.text = sub
        p2.font.name = 'Calibri'; p2.font.size = Pt(17); p2.font.color.rgb = MUTED

    # CENTER: VS
    tb_vs = s2.shapes.add_textbox(Inches(5.8), Inches(3.2), Inches(1.6), Inches(0.8))
    tf_vs = tb_vs.text_frame; tf_vs.margin_left = tf_vs.margin_top = 0
    p = tf_vs.paragraphs[0]; p.text = "VS"
    p.alignment = PP_ALIGN.CENTER
    p.font.name = 'Calibri'; p.font.size = Pt(40); p.font.bold = True; p.font.color.rgb = MUTED

    # RIGHT SIDE: WITH CCMS
    tb_r = s2.shapes.add_textbox(Inches(7.6), Inches(1.6), Inches(4.7), Inches(0.4))
    tb_r.text_frame.margin_left = tb_r.text_frame.margin_top = 0
    p = tb_r.text_frame.paragraphs[0]; p.text = "WITH CCMS"
    p.font.name = 'Calibri'; p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = BLUE

    v_line_r = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.8), Inches(2.25), Inches(0.02), Inches(3.1))
    v_line_r.fill.solid(); v_line_r.fill.fore_color.rgb = BLUE
    v_line_r.line.fill.background()

    c_steps = [
        ("Web Portal", "24/7 access with campus location & photo"),
        ("Admin Verification", "Supervisory triage and validity checking"),
        ("Staff Assignment", "Work dispatched directly to technician queue"),
        ("Status Tracking", "Live milestone progression from NEW to CLOSED"),
        ("Audited Resolution", "Diagnostic completion notes and 1–5 star rating")
    ]
    for idx, (title, sub) in enumerate(c_steps):
        dot = s2.shapes.add_shape(MSO_SHAPE.OVAL, Inches(7.72), Inches(2.25 + idx * 0.76), Inches(0.18), Inches(0.18))
        dot.fill.solid(); dot.fill.fore_color.rgb = BLUE; dot.line.fill.background()

        tb = s2.shapes.add_textbox(Inches(8.05), Inches(2.15 + idx * 0.76), Inches(4.2), Inches(0.65))
        tf = tb.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]; p.text = title
        p.font.name = 'Calibri'; p.font.size = Pt(19); p.font.bold = True; p.font.color.rgb = NAVY
        p2 = tf.add_paragraph(); p2.text = sub
        p2.font.name = 'Calibri'; p2.font.size = Pt(17); p2.font.color.rgb = MUTED

    # BOTTOM: One bold sentence
    tb_bot = s2.shapes.add_textbox(Inches(1.0), Inches(5.95), Inches(11.333), Inches(0.45))
    tf_bot = tb_bot.text_frame; tf_bot.margin_left = tf_bot.margin_top = 0
    p = tf_bot.paragraphs[0]
    p.text = "CCMS replaces an untracked manual process with a centralized digital lifecycle."
    p.font.name = 'Calibri'; p.font.size = Pt(21); p.font.bold = True; p.font.color.rgb = NAVY

    # =========================================================================
    # SLIDE 3 — SOFTWARE ENGINEERING APPROACH (Timeline + 4 Mappings)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_slide_header(s3, "02 — SE APPROACH", "SDLC Progression & Requirements Traceability")
    add_slide_footer(s3, 3)

    # TOP: Elegant Horizontal SDLC Timeline
    sdlc_y = 1.6
    sdlc_steps = ["REQUIREMENTS", "DESIGN", "IMPLEMENTATION", "SECURITY", "TESTING", "MAINTENANCE"]
    
    # Continuous thin line connecting steps
    h_line = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(sdlc_y + 0.12), Inches(10.7), Inches(0.02))
    h_line.fill.solid(); h_line.fill.fore_color.rgb = BLUE
    h_line.line.fill.background()

    step_xs = [1.0, 3.1, 5.2, 7.3, 9.3, 11.2]
    for idx, (name, sx) in enumerate(zip(sdlc_steps, step_xs)):
        # Node dot
        dot = s3.shapes.add_shape(MSO_SHAPE.OVAL, Inches(sx + 0.35), Inches(sdlc_y + 0.04), Inches(0.18), Inches(0.18))
        dot.fill.solid(); dot.fill.fore_color.rgb = BLUE; dot.line.fill.background()

        tb = s3.shapes.add_textbox(Inches(sx - 0.2), Inches(sdlc_y + 0.32), Inches(1.3), Inches(0.4))
        tf = tb.text_frame; tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]; p.text = name
        p.alignment = PP_ALIGN.CENTER
        p.font.name = 'Calibri'; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = NAVY

    # MIDDLE: Subheading
    tb_map_h = s3.shapes.add_textbox(Inches(1.0), Inches(2.7), Inches(11.333), Inches(0.4))
    tb_map_h.text_frame.margin_left = tb_map_h.text_frame.margin_top = 0
    p = tb_map_h.text_frame.paragraphs[0]; p.text = "Requirements → Implementation Traceability Mapping"
    p.font.name = 'Calibri'; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = NAVY

    # 4 Important Requirement Mappings (Clean Typography & Thin Connectors)
    reqs = [
        ("Secure Access", "Stateless JWT authentication + bcryptjs password hashing + verifyToken middleware"),
        ("Complaint Lodging", "Dynamic React form + campus category & room mapping + Multer evidence upload"),
        ("Lifecycle Control", "Strict server-side Finite State Machine validator + immutable complaint_updates log"),
        ("Quality Verification", "Playwright end-to-end journeys + Basis Path Testing on transitions (V(G) = 11)")
    ]
    tb_req = s3.shapes.add_textbox(Inches(1.0), Inches(3.2), Inches(11.333), Inches(3.2))
    tf_req = tb_req.text_frame; tf_req.word_wrap = True; tf_req.margin_left = tf_req.margin_top = 0

    for idx, (req_title, req_impl) in enumerate(reqs):
        p = tf_req.paragraphs[0] if idx == 0 else tf_req.add_paragraph()
        if idx > 0: p.space_before = Pt(14)
        r1 = p.add_run(); r1.text = f"{req_title:24} "; r1.font.bold = True; r1.font.size = Pt(20); r1.font.color.rgb = BLUE
        r2 = p.add_run(); r2.text = "→   "; r2.font.bold = True; r2.font.size = Pt(20); r2.font.color.rgb = NAVY
        r3 = p.add_run(); r3.text = req_impl; r3.font.size = Pt(20); r3.font.color.rgb = DARK

    # =========================================================================
    # SLIDE 4 — SYSTEM ARCHITECTURE (Actual Layered Software Diagram)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_slide_header(s4, "03 — ARCHITECTURE", "Decoupled 3-Tier Layered Architecture")
    add_slide_footer(s4, 4)

    # LEFT SIDE: Architecture Diagram (Layered, with Clean Lines)
    arch_left = 1.0
    arch_w = 6.2

    # Layer 1: Users
    add_thin_box(s4, arch_left, 1.6, arch_w, 0.55, "STUDENTS  |  FACULTY  |  ADMIN  |  STAFF", bg_color=WHITE, border_color=NAVY, text_color=NAVY, font_size=17)
    add_arrow_down(s4, arch_left + arch_w/2 - 0.1, 2.18, width=0.2, height=0.25, color=BLUE)

    # Layer 2: Frontend
    add_thin_box(s4, arch_left, 2.45, arch_w, 0.65, "REACT FRONTEND (SPA)\nReact 18 · Vite 5 · Tailwind CSS · Axios Client", bg_color=WHITE, border_color=BLUE, text_color=NAVY, font_size=17)
    add_arrow_down(s4, arch_left + arch_w/2 - 0.1, 3.12, width=0.2, height=0.25, color=BLUE)

    # Layer 3: REST API Server with Sub-Block
    add_thin_box(s4, arch_left, 3.4, arch_w, 0.45, "REST API SERVER (Node.js 18 + Express 4.19)", bg_color=WHITE, border_color=BLUE, text_color=NAVY, font_size=17)
    
    # Sub-block inside REST API: Business Logic & Middleware
    add_thin_box(s4, arch_left + 0.3, 3.9, arch_w - 0.6, 0.58, "Auth Middleware  |  Validation  |  FSM State Engine\nStaff Assignment  |  Multer Upload  |  Audit Logger", bg_color=LIGHT_BG, border_color=BORDER, text_color=DARK, font_size=16, bold=False)
    add_arrow_down(s4, arch_left + arch_w/2 - 0.1, 4.52, width=0.2, height=0.25, color=BLUE)

    # Layer 4: MySQL Database
    add_thin_box(s4, arch_left, 4.8, arch_w, 0.65, "MYSQL 8 RELATIONAL DATABASE\nccms_db · 7 Normalized Tables · InnoDB Transactions", bg_color=NAVY, border_color=NAVY, text_color=WHITE, font_size=17)

    # Side Flow: JWT
    jwt_box = add_thin_box(s4, 5.0, 2.85, 2.1, 0.45, "JWT Bearer Token", bg_color=WHITE, border_color=BLUE, text_color=BLUE, font_size=15)

    # RIGHT SIDE: Three Core Principles (Clean Typography, No Paragraphs)
    tb_pr = s4.shapes.add_textbox(Inches(7.8), Inches(1.6), Inches(4.5), Inches(4.6))
    tf_pr = tb_pr.text_frame; tf_pr.word_wrap = True; tf_pr.margin_left = tf_pr.margin_top = 0

    p = tf_pr.paragraphs[0]; p.text = "Key Architectural Principles"
    p.font.name = 'Calibri'; p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = NAVY
    p.space_after = Pt(14)

    principles = [
        ("Separation of Concerns", "Presentation tier is strictly decoupled from storage. The client never queries MySQL directly; all operations are governed by validated REST endpoints."),
        ("Stateless JWT Authorization", "HS256 signed Bearer tokens eliminate server-side session state, enabling fast horizontal scaling and seamless route protection."),
        ("ACID & Referential Integrity", "Normalized 3NF relational schema with strict foreign keys, atomic transactions, and parameterized SQL queries eliminating SQL injection.")
    ]
    for p_title, p_desc in principles:
        p = tf_pr.add_paragraph(); p.space_before = Pt(12)
        r1 = p.add_run(); r1.text = f"• {p_title}\n"; r1.font.bold = True; r1.font.size = Pt(20); r1.font.color.rgb = BLUE
        r2 = p.add_run(); r2.text = p_desc; r2.font.size = Pt(18); r2.font.color.rgb = DARK

    # =========================================================================
    # SLIDE 5 — COMPLAINT LIFECYCLE (Horizontal Process + 3 Roles Underneath)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_slide_header(s5, "04 — WORKFLOW", "Finite State Machine & Role Responsibilities")
    add_slide_footer(s5, 5)

    # TOP: One Large Horizontal Lifecycle Flow
    fsm_y = 1.7
    fsm_nodes = [
        ("NEW", 1.0, 1.4),
        ("VERIFIED", 2.8, 1.6),
        ("ASSIGNED", 4.8, 1.6),
        ("IN PROGRESS", 6.8, 1.8),
        ("RESOLVED", 9.0, 1.6),
        ("CLOSED", 11.0, 1.333)
    ]
    for idx, (name, x, w) in enumerate(fsm_nodes):
        add_thin_box(s5, x, fsm_y, w, 0.65, name, bg_color=NAVY, border_color=NAVY, text_color=WHITE, font_size=18)
        if idx < len(fsm_nodes) - 1:
            add_arrow_right(s5, x + w + 0.08, fsm_y + 0.2, width=0.22, height=0.2, color=BLUE)

    # Branches: REJECTED & REOPENED
    add_thin_box(s5, 2.8, 2.7, 2.2, 0.5, "REJECTED (Invalid)", bg_color=WHITE, border_color=RED_TEXT, text_color=RED_TEXT, font_size=16)
    add_arrow_down(s5, 3.8, 2.37, width=0.18, height=0.3, color=RED_TEXT)

    add_thin_box(s5, 10.133, 2.7, 2.2, 0.5, "REOPENED (Recurring)", bg_color=WHITE, border_color=AMBER_TEXT, text_color=AMBER_TEXT, font_size=16)
    add_arrow_down(s5, 11.1, 2.37, width=0.18, height=0.3, color=AMBER_TEXT)

    # BOTTOM: Three Role Columns (Submit -> Track -> Rate, etc.)
    role_y = 3.65
    role_col_w = 3.6

    role_data = [
        ("STUDENT / FACULTY", "Submit  →  Track  →  Rate", [
            "Lodges complaint with building, room & photo evidence",
            "Tracks live milestone timeline from submission to fix",
            "Submits 1–5 star rating and feedback upon closure"
        ], BLUE),
        ("ADMINISTRATOR", "Verify  →  Assign  →  Close", [
            "Inspects ticket details; marks VERIFIED or REJECTED",
            "Dispatches work order to qualified maintenance staff",
            "Reviews repair diagnostic notes and confirms closure"
        ], NAVY),
        ("MAINTENANCE STAFF", "Accept  →  Work  →  Resolve", [
            "Accesses assigned work orders in dedicated queue",
            "Transitions status to IN PROGRESS upon starting repair",
            "Logs diagnostic remarks and marks ticket RESOLVED"
        ], GREEN_TEXT)
    ]
    for idx, (r_name, r_flow, r_items, r_color) in enumerate(role_data):
        rx = 1.0 + idx * (role_col_w + 0.25)
        tb_r = s5.shapes.add_textbox(Inches(rx), Inches(role_y), Inches(role_col_w), Inches(2.7))
        tf_r = tb_r.text_frame; tf_r.word_wrap = True; tf_r.margin_left = tf_r.margin_top = 0
        
        p = tf_r.paragraphs[0]; p.text = r_name
        p.font.name = 'Calibri'; p.font.size = Pt(21); p.font.bold = True; p.font.color.rgb = r_color

        p2 = tf_r.add_paragraph(); p2.space_before = Pt(4)
        p2.text = r_flow; p2.font.name = 'Calibri'; p2.font.size = Pt(18); p2.font.bold = True; p2.font.color.rgb = NAVY

        for item in r_items:
            p_i = tf_r.add_paragraph(); p_i.space_before = Pt(6)
            p_i.text = "• " + item; p_i.font.name = 'Calibri'; p_i.font.size = Pt(17); p_i.font.color.rgb = DARK

    # =========================================================================
    # SLIDE 6 — MODULES + TECHNOLOGY (System Map + Clean Tech Stack List)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_slide_header(s6, "05 — MODULES & TECH", "System Modules & Production Technology Stack")
    add_slide_footer(s6, 6)

    # LEFT SIDE: Module Flow Pipeline
    tb_m = s6.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(5.3), Inches(0.4))
    tb_m.text_frame.margin_left = tb_m.text_frame.margin_top = 0
    p = tb_m.text_frame.paragraphs[0]; p.text = "MODULE FLOW"
    p.font.name = 'Calibri'; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = NAVY

    mod_flow = [
        ("Authentication & RBAC", "Registration, login, JWT token issuance, route guards"),
        ("Complaint Lodging", "Dynamic React form, category/room mapping, Multer upload"),
        ("Administrative Triage", "Campus-wide review, status filtering, staff assignment"),
        ("Maintenance Work Orders", "Technician queue, work commencement, repair remarks"),
        ("Audit & Feedback", "Append-only status history in complaint_updates & ratings")
    ]
    mod_top = 2.05
    for idx, (m_title, m_desc) in enumerate(mod_flow):
        add_thin_box(s6, 1.0, mod_top + idx * 0.9, 5.3, 0.58, f"{m_title}\n{m_desc}", bg_color=WHITE, border_color=BLUE, text_color=NAVY, font_size=16)
        if idx < len(mod_flow) - 1:
            add_arrow_down(s6, 3.55, mod_top + idx * 0.9 + 0.6, width=0.18, height=0.26, color=BLUE)

    # RIGHT SIDE: Technology Stack as a Clean Vertical List (No Card Clutter!)
    tb_t = s6.shapes.add_textbox(Inches(7.2), Inches(1.5), Inches(5.1), Inches(4.8))
    tf_t = tb_t.text_frame; tf_t.word_wrap = True; tf_t.margin_left = tf_t.margin_top = 0
    p = tf_t.paragraphs[0]; p.text = "TECHNOLOGY STACK"
    p.font.name = 'Calibri'; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = NAVY
    p.space_after = Pt(12)

    tech_stack = [
        ("FRONTEND", "React 18  ·  Vite 5  ·  Tailwind CSS  ·  Axios  ·  React Router"),
        ("BACKEND", "Node.js 18 LTS  ·  Express 4.19  ·  express-validator  ·  Multer"),
        ("DATABASE", "MySQL 8.0  ·  mysql2 Connection Pool  ·  InnoDB Engine (7 Tables)"),
        ("SECURITY / TESTING", "JSON Web Tokens (JWT HS256)  ·  bcryptjs (10 rounds)  ·  Playwright")
    ]
    for cat_name, tech_line in tech_stack:
        p = tf_t.add_paragraph(); p.space_before = Pt(14)
        r1 = p.add_run(); r1.text = f"{cat_name}\n"; r1.font.bold = True; r1.font.size = Pt(20); r1.font.color.rgb = BLUE
        r2 = p.add_run(); r2.text = tech_line; r2.font.size = Pt(18); r2.font.color.rgb = DARK

    # =========================================================================
    # SLIDE 7 — DATABASE DESIGN (Real ER Relationship Diagram)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_slide_header(s7, "06 — DATA MODEL", "Relational Database Schema & Data Integrity")
    add_slide_footer(s7, 7)

    # TOP: Real ER-Style Diagram
    # Row 1: Users -> Complaints <- Locations & Categories
    add_thin_box(s7, 1.0, 1.55, 3.2, 1.05, "USERS\nid (PK) · name · email\nrole · department", bg_color=WHITE, border_color=NAVY, text_color=NAVY, font_size=17)
    
    add_arrow_right(s7, 4.3, 1.95, width=0.35, height=0.22, color=BLUE)

    add_thin_box(s7, 4.8, 1.55, 3.733, 1.05, "COMPLAINTS (Core Entity)\nid (PK) · complaint_number · user_id (FK)\ncategory_id (FK) · location_id (FK) · status", bg_color=NAVY, border_color=NAVY, text_color=WHITE, font_size=17)

    add_arrow_right(s7, 8.65, 1.95, width=0.35, height=0.22, color=BLUE)

    add_thin_box(s7, 9.133, 1.55, 3.2, 1.05, "LOCATIONS & CATEGORIES\nbuilding · floor · room\ncategory_name", bg_color=WHITE, border_color=NAVY, text_color=NAVY, font_size=17)

    # Row 2: Connected Child Tables
    add_arrow_down(s7, 2.5, 2.65, width=0.2, height=0.3, color=BLUE)
    add_thin_box(s7, 1.0, 3.0, 3.2, 1.05, "COMPLAINT_ASSIGNMENTS\nstaff_id (FK) · assigned_by (FK)\nassigned_at · notes", bg_color=WHITE, border_color=BLUE, text_color=BLUE, font_size=17)

    add_arrow_down(s7, 6.55, 2.65, width=0.2, height=0.3, color=BLUE)
    add_thin_box(s7, 4.8, 3.0, 3.733, 1.05, "COMPLAINT_UPDATES (Audit Log)\nold_status · new_status · remarks\nupdated_by (FK) · created_at", bg_color=WHITE, border_color=BLUE, text_color=BLUE, font_size=17)

    add_arrow_down(s7, 10.6, 2.65, width=0.2, height=0.3, color=BLUE)
    add_thin_box(s7, 9.133, 3.0, 3.2, 1.05, "FEEDBACK\ncomplaint_id (FK) · user_id (FK)\nrating (1–5) · comments", bg_color=WHITE, border_color=BLUE, text_color=BLUE, font_size=17)

    # BOTTOM: Three Short Concepts (Clean Typography & Divider Line)
    div_line = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(4.4), Inches(11.333), Inches(0.015))
    div_line.fill.solid(); div_line.fill.fore_color.rgb = BORDER
    div_line.line.fill.background()

    db_concepts = [
        ("3NF Normalization", "Redundancy eliminated. Campus locations and categories are stored as independent master tables, allowing dynamic additions without schema alterations.", NAVY),
        ("Referential Integrity", "Foreign key constraints with ON UPDATE / ON DELETE rules guarantee that tickets and history always map to valid users and rooms.", BLUE),
        ("Immutable Audit Trail", "The complaint_updates table operates as an append-only transaction log, recording every status transition with operator IDs and timestamps.", GREEN_TEXT)
    ]
    b_col_w = 3.6
    for idx, (title, desc, color) in enumerate(db_concepts):
        bx = 1.0 + idx * (b_col_w + 0.25)
        tb = s7.shapes.add_textbox(Inches(bx), Inches(4.55), Inches(b_col_w), Inches(2.0))
        tf = tb.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]; p.text = title
        p.font.name = 'Calibri'; p.font.size = Pt(21); p.font.bold = True; p.font.color.rgb = color
        p2 = tf.add_paragraph(); p2.space_before = Pt(6)
        p2.text = desc; p2.font.name = 'Calibri'; p2.font.size = Pt(17); p2.font.color.rgb = DARK

    # =========================================================================
    # SLIDE 8 — ACTUAL APPLICATION (Mostly Screenshots: 65-75% of Slide!)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_slide_header(s8, "07 — APPLICATION", "Authentic Application User Interface")
    add_slide_footer(s8, 8)

    # Two Large Screenshots Side-by-Side (5.4 in wide, 3.375 in high)
    img_w = 5.4
    img_y = 1.55

    # Screen 1: Admin Dashboard
    if os.path.exists("docs/screenshots/07_admin_dashboard.png"):
        s8.shapes.add_picture("docs/screenshots/07_admin_dashboard.png", Inches(1.0), Inches(img_y), width=Inches(img_w))
    
    tb_c1 = s8.shapes.add_textbox(Inches(1.0), Inches(5.1), Inches(img_w), Inches(1.5))
    tf_c1 = tb_c1.text_frame; tf_c1.word_wrap = True; tf_c1.margin_left = tf_c1.margin_top = 0
    p = tf_c1.paragraphs[0]; p.text = "Administrator Control Center"
    p.font.name = 'Calibri'; p.font.size = Pt(21); p.font.bold = True; p.font.color.rgb = NAVY
    p2 = tf_c1.add_paragraph(); p2.space_before = Pt(4)
    p2.text = "• Real-Time Campus KPIs: Total, open, resolved, and critical ticket counts.\n• Interactive Triage: Instant search, category filters, and verify/reject controls."
    p2.font.name = 'Calibri'; p2.font.size = Pt(18); p2.font.color.rgb = DARK

    # Screen 2: Technician Tasks
    if os.path.exists("docs/screenshots/15_maintenance_tasks.png"):
        s8.shapes.add_picture("docs/screenshots/15_maintenance_tasks.png", Inches(6.933), Inches(img_y), width=Inches(img_w))

    tb_c2 = s8.shapes.add_textbox(Inches(6.933), Inches(5.1), Inches(img_w), Inches(1.5))
    tf_c2 = tb_c2.text_frame; tf_c2.word_wrap = True; tf_c2.margin_left = tf_c2.margin_top = 0
    p = tf_c2.paragraphs[0]; p.text = "Technician Work Order Queue"
    p.font.name = 'Calibri'; p.font.size = Pt(21); p.font.bold = True; p.font.color.rgb = GREEN_TEXT
    p2 = tf_c2.add_paragraph(); p2.space_before = Pt(4)
    p2.text = "• Room-Level Dispatching: Displays exact campus building, floor, and urgency.\n• Work Execution: Single-click 'Start Work' and diagnostic remarks submission."
    p2.font.name = 'Calibri'; p2.font.size = Pt(18); p2.font.color.rgb = DARK

    # =========================================================================
    # SLIDE 9 — TESTING (Visually Dominant Metric + 4 Areas + 3 Key Tests)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_slide_header(s9, "08 — TESTING", "Quality Assurance & Test Execution Results")
    add_slide_footer(s9, 9)

    # LEFT SIDE: Dominant Metric & 4 Areas
    tb_met = s9.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(5.0), Inches(1.3))
    tf_met = tb_met.text_frame; tf_met.margin_left = tf_met.margin_top = 0
    p = tf_met.paragraphs[0]; p.text = "30 / 30"
    p.font.name = 'Calibri'; p.font.size = Pt(48); p.font.bold = True; p.font.color.rgb = GREEN_TEXT
    p2 = tf_met.add_paragraph(); p2.text = "TEST CASES PASSED  ·  100% PASS RATE"
    p2.font.name = 'Calibri'; p2.font.size = Pt(19); p2.font.bold = True; p2.font.color.rgb = NAVY

    # 4 Simple Testing Areas
    tb_areas = s9.shapes.add_textbox(Inches(1.0), Inches(3.0), Inches(5.0), Inches(3.5))
    tf_areas = tb_areas.text_frame; tf_areas.word_wrap = True; tf_areas.margin_left = tf_areas.margin_top = 0

    test_areas = [
        ("UNIT", "Authentication, token verification, unique CMP-ID generators"),
        ("BASIS PATH", "Cyclomatic Complexity V(G) = 11 covering all legal & illegal FSM branches"),
        ("ROLE ACCESS", "Student tokens strictly barred from admin endpoints (HTTP 403 Forbidden)"),
        ("INTEGRATION", "End-to-end browser workflows automated and validated with Playwright")
    ]
    for idx, (a_name, a_desc) in enumerate(test_areas):
        p = tf_areas.paragraphs[0] if idx == 0 else tf_areas.add_paragraph()
        if idx > 0: p.space_before = Pt(10)
        r1 = p.add_run(); r1.text = f"{a_name}\n"; r1.font.bold = True; r1.font.size = Pt(19); r1.font.color.rgb = BLUE
        r2 = p.add_run(); r2.text = a_desc; r2.font.size = Pt(17); r2.font.color.rgb = DARK

    # RIGHT SIDE: 3 Representative Test Cases (Clean Rows, NOT an Excel Sheet!)
    tb_tcases = s9.shapes.add_textbox(Inches(6.6), Inches(1.5), Inches(5.7), Inches(5.0))
    tf_tc = tb_tcases.text_frame; tf_tc.word_wrap = True; tf_tc.margin_left = tf_tc.margin_top = 0

    p = tf_tc.paragraphs[0]; p.text = "Key Verification Scenarios"
    p.font.name = 'Calibri'; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = NAVY
    p.space_after = Pt(14)

    t_cases = [
        ("TC-01", "Administrator Authentication", "POST /api/auth/login", "HTTP 200; Valid JWT token issued; Admin authorized", "PASS"),
        ("TC-04", "Illegal Transition Protection", "PUT /api/complaints/:id/status", "HTTP 400 Bad Request; FSM validator blocks NEW → CLOSED jump", "PASS"),
        ("TC-05", "RBAC Route Authorization", "POST /api/complaints/:id/assign", "HTTP 403 Forbidden; Non-admin role barred from assignment API", "PASS")
    ]
    for tc_id, tc_name, tc_endpoint, tc_res, tc_status in t_cases:
        p = tf_tc.add_paragraph(); p.space_before = Pt(14)
        r1 = p.add_run(); r1.text = f"• {tc_id} | {tc_name}\n"; r1.font.bold = True; r1.font.size = Pt(19); r1.font.color.rgb = NAVY
        r2 = p.add_run(); r2.text = f"   Endpoint: {tc_endpoint}\n"; r2.font.size = Pt(17); r2.font.color.rgb = MUTED
        r3 = p.add_run(); r3.text = f"   Result: {tc_res}\n"; r3.font.size = Pt(17); r3.font.color.rgb = DARK
        r4 = p.add_run(); r4.text = f"   Status: "; r4.font.bold = True; r4.font.size = Pt(17); r4.font.color.rgb = NAVY
        r5 = p.add_run(); r5.text = f"{tc_status}"; r5.font.bold = True; r5.font.size = Pt(18); r5.font.color.rgb = GREEN_TEXT

    # =========================================================================
    # SLIDE 10 — CONCLUSION (Clean Achievements + Future Arrow + Thank You)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_slide_header(s10, "09 — CONCLUSION", "Project Achievements & Future Roadmap")
    add_slide_footer(s10, 10)

    # TOP: What We Achieved
    tb_ach = s10.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.333), Inches(2.4))
    tf_ach = tb_ach.text_frame; tf_ach.word_wrap = True; tf_ach.margin_left = tf_ach.margin_top = 0

    p = tf_ach.paragraphs[0]; p.text = "What We Achieved"
    p.font.name = 'Calibri'; p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = NAVY
    p.space_after = Pt(8)

    achievements = [
        ("✓ Digital Complaint Management", "Replaced error-prone manual logbooks with a 24/7 web-based grievance ecosystem."),
        ("✓ Role-Based Access Control", "Enforced strict privilege separation across Student, Faculty, Staff, and Administrator."),
        ("✓ Controlled Complaint Lifecycle", "Server-side Finite State Machine preventing illegal state jumps and unauthorized closures."),
        ("✓ Complete Audit Trail", "Immutable update history logging operator IDs, remarks, and timestamps for full governance.")
    ]
    for ach_t, ach_d in achievements:
        p = tf_ach.add_paragraph(); p.space_before = Pt(6)
        r1 = p.add_run(); r1.text = f"{ach_t}: "; r1.font.bold = True; r1.font.size = Pt(19); r1.font.color.rgb = GREEN_TEXT
        r2 = p.add_run(); r2.text = ach_d; r2.font.size = Pt(18); r2.font.color.rgb = DARK

    # MIDDLE: Progression Arrow
    tb_arrow = s10.shapes.add_textbox(Inches(1.0), Inches(4.0), Inches(11.333), Inches(0.4))
    tf_arr = tb_arrow.text_frame; tf_arr.margin_left = tf_arr.margin_top = 0
    p = tf_arr.paragraphs[0]
    r1 = p.add_run(); r1.text = "CURRENT SYSTEM (Core Web Platform)   "; r1.font.bold = True; r1.font.size = Pt(19); r1.font.color.rgb = NAVY
    r2 = p.add_run(); r2.text = "────────────►   "; r2.font.bold = True; r2.font.size = Pt(20); r2.font.color.rgb = BLUE
    r3 = p.add_run(); r3.text = "FUTURE ROADMAP"; r3.font.bold = True; r3.font.size = Pt(19); r3.font.color.rgb = BLUE

    # BOTTOM: Future Roadmap Items
    tb_fut = s10.shapes.add_textbox(Inches(1.0), Inches(4.5), Inches(11.333), Inches(1.4))
    tf_fut = tb_fut.text_frame; tf_fut.word_wrap = True; tf_fut.margin_left = tf_fut.margin_top = 0

    future_items = [
        "Email / SMS Alerts: Automated push notifications via Nodemailer (SMTP) and Twilio (SMS).",
        "Cloud Object Storage: Migration of uploaded complaint photos from local disk to Amazon S3.",
        "Native Mobile Client: Cross-platform iOS/Android app built using React Native.",
        "Automated Task Dispatch: AI-driven technician assignment based on active workload and trade skills."
    ]
    for idx, fut in enumerate(future_items):
        p = tf_fut.paragraphs[0] if idx == 0 else tf_fut.add_paragraph()
        if idx > 0: p.space_before = Pt(4)
        p.text = "• " + fut; p.font.name = 'Calibri'; p.font.size = Pt(18); p.font.color.rgb = DARK

    # BOTTOM BANNER: Thank You
    tb_th = s10.shapes.add_textbox(Inches(1.0), Inches(6.05), Inches(11.333), Inches(0.6))
    tf_th = tb_th.text_frame; tf_th.margin_left = tf_th.margin_top = 0
    p = tf_th.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "Thank You  |  Questions & Answers"
    p.font.name = 'Calibri'; p.font.size = Pt(26); p.font.bold = True; p.font.color.rgb = NAVY

    # Save
    output_path = "Campus_Complaint_Management_System_Mini_Project_Presentation.pptx"
    prs.save(output_path)
    print(f"Masterpiece presentation saved to: {output_path}")


if __name__ == "__main__":
    build_deck()
