import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# ---------------------------------------------------------------------------
# GLOBAL CONSTANTS & ACADEMIC DESIGN TOKENS
# ---------------------------------------------------------------------------
NAVY = RGBColor(15, 39, 68)          # #0F2744 - Academic Primary Navy
DARK_TEXT = RGBColor(17, 24, 39)     # #111827 - High Contrast Body Text
SLATE_TEXT = RGBColor(51, 65, 85)    # #334155 - Secondary Details Text
BLUE = RGBColor(29, 78, 216)         # #1D4ED8 - Engineering Brand Blue
LIGHT_BG = RGBColor(248, 250, 252)   # #F8FAFC - Clean Card Background
BORDER = RGBColor(203, 213, 225)     # #CBD5E1 - 1pt Neutral Border
WHITE = RGBColor(255, 255, 255)      # Pure White

# Status Alert Colors
RED_BG = RGBColor(254, 242, 242)     # #FEF2F2
RED_BORDER = RGBColor(239, 68, 68)   # #EF4444
RED_TEXT = RGBColor(153, 27, 27)     # #991B1B

GREEN_BG = RGBColor(240, 253, 244)   # #F0FDF4
GREEN_BORDER = RGBColor(34, 197, 94) # #22C55E
GREEN_TEXT = RGBColor(20, 83, 45)    # #14532D

AMBER_BG = RGBColor(255, 251, 235)   # #FFFBEB
AMBER_BORDER = RGBColor(245, 158, 11)# #F59E0B
AMBER_TEXT = RGBColor(146, 64, 14)   # #92400E

BLUE_BG = RGBColor(239, 246, 255)    # #EFF6FF
BLUE_BORDER = RGBColor(59, 130, 246) # #3B82F6


# ---------------------------------------------------------------------------
# HELPER FUNCTIONS FOR SHAPES, TEXT, & LAYOUT
# ---------------------------------------------------------------------------
def add_card(slide, left, top, width, height, bg_color=LIGHT_BG, border_color=BORDER):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.2)
    return shape


def add_header(slide, section_num_name, title_text):
    # Eyebrow / Section indicator
    tb_eye = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.35))
    tf_eye = tb_eye.text_frame
    tf_eye.word_wrap = True
    tf_eye.margin_left = tf_eye.margin_top = tf_eye.margin_right = tf_eye.margin_bottom = 0
    p_eye = tf_eye.paragraphs[0]
    p_eye.text = section_num_name.upper()
    p_eye.font.name = 'Arial'
    p_eye.font.size = Pt(18)
    p_eye.font.bold = True
    p_eye.font.color.rgb = BLUE

    # Primary Slide Title
    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.733), Inches(0.55))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = 'Arial'
    p_title.font.size = Pt(32)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY


def add_footer(slide, current_slide, total_slides=10):
    # Divider Rule
    rule = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.8), Inches(6.82), Inches(11.733), Inches(0.015)
    )
    rule.fill.solid()
    rule.fill.fore_color.rgb = BORDER
    rule.line.fill.background()

    # Left text: Project Title & Context
    tb_left = slide.shapes.add_textbox(Inches(0.8), Inches(6.92), Inches(9.2), Inches(0.35))
    tf_left = tb_left.text_frame
    tf_left.margin_left = tf_left.margin_top = tf_left.margin_right = tf_left.margin_bottom = 0
    p_left = tf_left.paragraphs[0]
    p_left.text = "Campus Complaint & Maintenance Management System  |  Software Engineering Mini Project"
    p_left.font.name = 'Arial'
    p_left.font.size = Pt(16)
    p_left.font.bold = True
    p_left.font.color.rgb = SLATE_TEXT

    # Right text: Slide numbering
    tb_right = slide.shapes.add_textbox(Inches(10.0), Inches(6.92), Inches(2.533), Inches(0.35))
    tf_right = tb_right.text_frame
    tf_right.margin_left = tf_right.margin_top = tf_right.margin_right = tf_right.margin_bottom = 0
    p_right = tf_right.paragraphs[0]
    p_right.alignment = PP_ALIGN.RIGHT
    p_right.text = f"Slide {current_slide} of {total_slides}"
    p_right.font.name = 'Arial'
    p_right.font.size = Pt(16)
    p_right.font.bold = True
    p_right.font.color.rgb = BLUE


def add_flow_node(slide, left, top, width, height, text, bg_color=WHITE, border_color=BLUE, text_color=NAVY, font_size=18):
    node = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    node.fill.solid()
    node.fill.fore_color.rgb = bg_color
    node.line.color.rgb = border_color
    node.line.width = Pt(1.5)
    tf = node.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = PP_ALIGN.CENTER
    p.font.name = 'Arial'
    p.font.size = Pt(font_size)
    p.font.bold = True
    p.font.color.rgb = text_color
    return node


def add_arrow_right(slide, left, top, width=0.35, height=0.22, color=BLUE):
    arrow = slide.shapes.add_shape(
        MSO_SHAPE.RIGHT_ARROW,
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = color
    arrow.line.fill.background()
    return arrow


def add_arrow_down(slide, left, top, width=0.22, height=0.35, color=BLUE):
    arrow = slide.shapes.add_shape(
        MSO_SHAPE.DOWN_ARROW,
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = color
    arrow.line.fill.background()
    return arrow


# ---------------------------------------------------------------------------
# MAIN PRESENTATION BUILDER
# ---------------------------------------------------------------------------
def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: ACADEMIC TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    
    # Outer Framing & Background Card
    add_card(s1, 0.8, 0.7, 11.733, 6.1, bg_color=LIGHT_BG, border_color=BORDER)
    
    # Vertical Accent Brand Bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(1.2), Inches(0.18), Inches(5.1))
    bar.fill.solid(); bar.fill.fore_color.rgb = NAVY
    bar.line.fill.background()

    # Title & Metadata Text Frame
    tb1 = s1.shapes.add_textbox(Inches(1.6), Inches(1.15), Inches(10.5), Inches(5.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0

    p = tf1.paragraphs[0]
    p.text = "23CS4219 — SOFTWARE ENGINEERING LABORATORY"
    p.font.name = 'Arial'; p.font.size = Pt(20); p.font.bold = True; p.font.color.rgb = BLUE
    p.space_after = Pt(10)

    p = tf1.add_paragraph()
    p.text = "Campus Complaint & Maintenance Management System"
    p.font.name = 'Arial'; p.font.size = Pt(36); p.font.bold = True; p.font.color.rgb = NAVY
    p.space_after = Pt(8)

    p = tf1.add_paragraph()
    p.text = "A Role-Based Full-Stack Web Application for Institutional Facility Grievance Tracking"
    p.font.name = 'Arial'; p.font.size = Pt(22); p.font.bold = False; p.font.color.rgb = SLATE_TEXT
    p.space_after = Pt(24)

    # Dividing line in title frame
    meta_items = [
        ("Student Name:", "Karthikeyan Gullipalli  (Roll No: [ROLL NUMBER])"),
        ("Faculty Guide:", "[GUIDE NAME]"),
        ("Department:", "Department of Computer Science and Engineering"),
        ("Institution:", "Anil Neerukonda Institute of Technology & Sciences (ANITS)"),
        ("Academic Year:", "2024–2025")
    ]
    for label, val in meta_items:
        p = tf1.add_paragraph()
        p.space_before = Pt(4)
        r1 = p.add_run(); r1.text = f"{label:16} "; r1.font.bold = True; r1.font.size = Pt(20); r1.font.color.rgb = NAVY
        r2 = p.add_run(); r2.text = val; r2.font.size = Pt(20); r2.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 2: 1. PROBLEM & MOTIVATION
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "1. Problem & Motivation", "Manual Paper Registers vs. Digital Campus Grievance Platform")
    add_footer(s2, 2)

    # PANEL A: Traditional Manual Flow (Top Half)
    add_card(s2, 0.8, 1.45, 11.733, 2.45, bg_color=RED_BG, border_color=RED_BORDER)
    
    # Header A
    tb = s2.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(11.3), Inches(0.35))
    tf = tb.text_frame; tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]; p.text = "Traditional Process: Physical Paper Logbooks & Verbal Dispatch"
    p.font.name = 'Arial'; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = RED_TEXT

    # Flowchart Nodes (Traditional)
    flow_y_trad = 1.98
    add_flow_node(s2, 1.0, flow_y_trad, 2.4, 0.52, "Paper Register", bg_color=WHITE, border_color=RED_BORDER, text_color=RED_TEXT, font_size=18)
    add_arrow_right(s2, 3.5, flow_y_trad + 0.15, width=0.3, height=0.2, color=RED_BORDER)
    add_flow_node(s2, 3.9, flow_y_trad, 2.4, 0.52, "Physical Counter", bg_color=WHITE, border_color=RED_BORDER, text_color=RED_TEXT, font_size=18)
    add_arrow_right(s2, 6.4, flow_y_trad + 0.15, width=0.3, height=0.2, color=RED_BORDER)
    add_flow_node(s2, 6.8, flow_y_trad, 2.4, 0.52, "Verbal Work Orders", bg_color=WHITE, border_color=RED_BORDER, text_color=RED_TEXT, font_size=18)
    add_arrow_right(s2, 9.3, flow_y_trad + 0.15, width=0.3, height=0.2, color=RED_BORDER)
    add_flow_node(s2, 9.7, flow_y_trad, 2.5, 0.52, "No Tracking / Lost", bg_color=WHITE, border_color=RED_BORDER, text_color=RED_TEXT, font_size=18)

    # Pain points bullets
    tb = s2.shapes.add_textbox(Inches(1.0), Inches(2.6), Inches(11.3), Inches(1.15))
    tf = tb.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = "• Physical Vulnerability: Logbooks are prone to damage, misplacement, and zero data backup."
    p.font.name = 'Arial'; p.font.size = Pt(20); p.font.color.rgb = DARK_TEXT
    p2 = tf.add_paragraph()
    p2.text = "• Zero Transparency & Accountability: Complainants cannot track progress; verbal orders lack audit trails."
    p2.font.name = 'Arial'; p2.font.size = Pt(20); p2.font.color.rgb = DARK_TEXT; p2.space_before = Pt(4)

    # PANEL B: Proposed CCMS Flow (Bottom Half)
    add_card(s2, 0.8, 4.1, 11.733, 2.45, bg_color=GREEN_BG, border_color=GREEN_BORDER)
    
    # Header B
    tb = s2.shapes.add_textbox(Inches(1.0), Inches(4.2), Inches(11.3), Inches(0.35))
    tf = tb.text_frame; tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]; p.text = "Proposed CCMS: Structured Full-Stack Web Platform"
    p.font.name = 'Arial'; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = GREEN_TEXT

    # Flowchart Nodes (CCMS)
    flow_y_ccms = 4.63
    add_flow_node(s2, 1.0, flow_y_ccms, 2.4, 0.52, "24/7 Web Portal", bg_color=WHITE, border_color=GREEN_BORDER, text_color=GREEN_TEXT, font_size=18)
    add_arrow_right(s2, 3.5, flow_y_ccms + 0.15, width=0.3, height=0.2, color=GREEN_BORDER)
    add_flow_node(s2, 3.9, flow_y_ccms, 2.4, 0.52, "Admin Triage", bg_color=WHITE, border_color=GREEN_BORDER, text_color=GREEN_TEXT, font_size=18)
    add_arrow_right(s2, 6.4, flow_y_ccms + 0.15, width=0.3, height=0.2, color=GREEN_BORDER)
    add_flow_node(s2, 6.8, flow_y_ccms, 2.4, 0.52, "Technician Queue", bg_color=WHITE, border_color=GREEN_BORDER, text_color=GREEN_TEXT, font_size=18)
    add_arrow_right(s2, 9.3, flow_y_ccms + 0.15, width=0.3, height=0.2, color=GREEN_BORDER)
    add_flow_node(s2, 9.7, flow_y_ccms, 2.5, 0.52, "Audit & Feedback", bg_color=WHITE, border_color=GREEN_BORDER, text_color=GREEN_TEXT, font_size=18)

    # Solution bullets
    tb = s2.shapes.add_textbox(Inches(1.0), Inches(5.25), Inches(11.3), Inches(1.15))
    tf = tb.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = "• Location & Urgency Tagging: Complaints mapped to exact buildings, floors, and rooms with priority levels."
    p.font.name = 'Arial'; p.font.size = Pt(20); p.font.color.rgb = DARK_TEXT
    p2 = tf.add_paragraph()
    p2.text = "• Complete Lifecycle Governance: Real-time status progression, staff assignment, and immutable audit logs."
    p2.font.name = 'Arial'; p2.font.size = Pt(20); p2.font.color.rgb = DARK_TEXT; p2.space_before = Pt(4)

    # =========================================================================
    # SLIDE 3: 2. SOFTWARE ENGINEERING APPROACH
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "2. Software Engineering Approach", "SDLC Lifecycle Progression & Requirements Traceability")
    add_footer(s3, 3)

    # TOP: SDLC Phase Progression Bar
    add_card(s3, 0.8, 1.45, 11.733, 1.25, bg_color=BLUE_BG, border_color=BLUE_BORDER)
    
    sdlc_y = 1.78
    sdlc_steps = [
        ("Requirements", 1.0, 1.55),
        ("System Design", 2.95, 1.55),
        ("Implementation", 4.9, 1.55),
        ("Security", 6.85, 1.55),
        ("Testing", 8.8, 1.55),
        ("Maintenance", 10.75, 1.55)
    ]
    for idx, (step_name, sx, sw) in enumerate(sdlc_steps):
        add_flow_node(s3, sx, sdlc_y, sw, 0.58, step_name, bg_color=NAVY, border_color=NAVY, text_color=WHITE, font_size=18)
        if idx < len(sdlc_steps) - 1:
            add_arrow_right(s3, sx + sw + 0.08, sdlc_y + 0.18, width=0.22, height=0.2, color=BLUE)

    # BOTTOM: Requirements -> Implementation Traceability Mapping
    add_card(s3, 0.8, 2.9, 11.733, 3.75, bg_color=WHITE, border_color=BORDER)
    
    tb = s3.shapes.add_textbox(Inches(1.0), Inches(3.05), Inches(11.3), Inches(0.4))
    tf = tb.text_frame; tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]; p.text = "Requirements Traceability: Demand  →  Engineering Implementation"
    p.font.name = 'Arial'; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = NAVY

    mappings = [
        ("Secure Multi-Role Access", "bcryptjs (10 rounds) + Stateless JWT with verifyToken / requireRole middleware guards"),
        ("Structured Grievance Lodging", "Dynamic React form with Category & Location dropdowns + Multer photo attachment"),
        ("Administrative Triage & Control", "Centralized Admin Dashboard with status filtering and one-click Verify / Reject actions"),
        ("Technician Task Dispatching", "Assignment controller dispatching work orders to dedicated staff task queues"),
        ("Audited Lifecycle Governance", "Finite State Machine transition validator with immutable complaint_updates logging"),
        ("Resolution Verification & Quality", "1 to 5 star student rating submission + reopening capability for unresolved issues")
    ]
    
    tb_map = s3.shapes.add_textbox(Inches(1.0), Inches(3.55), Inches(11.3), Inches(2.95))
    tf_map = tb_map.text_frame; tf_map.word_wrap = True; tf_map.margin_left = tf_map.margin_top = 0
    
    for idx, (req, impl) in enumerate(mappings):
        p = tf_map.paragraphs[0] if idx == 0 else tf_map.add_paragraph()
        if idx > 0: p.space_before = Pt(8)
        r1 = p.add_run(); r1.text = f"{req:32} "; r1.font.name = 'Arial'; r1.font.bold = True; r1.font.size = Pt(19); r1.font.color.rgb = BLUE
        r_arr = p.add_run(); r_arr.text = " →  "; r_arr.font.bold = True; r_arr.font.size = Pt(20); r_arr.font.color.rgb = NAVY
        r2 = p.add_run(); r2.text = impl; r2.font.name = 'Arial'; r2.font.size = Pt(19); r2.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 4: 3. SYSTEM ARCHITECTURE
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "3. System Architecture", "Decoupled 3-Tier Client-Server Architecture with Stateless API Security")
    add_footer(s4, 4)

    # LEFT COLUMN: Architectural Tier Diagram (Native Visual Hierarchy)
    add_card(s4, 0.8, 1.45, 6.2, 5.2, bg_color=LIGHT_BG, border_color=BORDER)

    # Tier 1: Presentation
    add_flow_node(s4, 1.1, 1.7, 5.6, 0.95, "Presentation Tier (Client SPA)\nReact 18 • Vite 5 • Tailwind CSS • Axios Interceptor", bg_color=WHITE, border_color=BLUE, text_color=NAVY, font_size=18)
    
    # Arrow 1 -> 2
    add_arrow_down(s4, 3.8, 2.75, width=0.22, height=0.35, color=BLUE)
    tb_lbl1 = s4.shapes.add_textbox(Inches(4.1), Inches(2.75), Inches(2.6), Inches(0.35))
    tb_lbl1.text_frame.paragraphs[0].text = "HTTPS REST + Bearer JWT"
    tb_lbl1.text_frame.paragraphs[0].font.size = Pt(16); tb_lbl1.text_frame.paragraphs[0].font.bold = True; tb_lbl1.text_frame.paragraphs[0].font.color.rgb = BLUE

    # Tier 2: Application
    add_flow_node(s4, 1.1, 3.2, 5.6, 1.05, "Application Tier (REST API Server)\nNode.js 18 LTS • Express 4.19 • Multer Upload\nJWT Auth Middleware • State Machine Validator", bg_color=WHITE, border_color=BLUE, text_color=NAVY, font_size=18)

    # Arrow 2 -> 3
    add_arrow_down(s4, 3.8, 4.35, width=0.22, height=0.35, color=BLUE)
    tb_lbl2 = s4.shapes.add_textbox(Inches(4.1), Inches(4.35), Inches(2.6), Inches(0.35))
    tb_lbl2.text_frame.paragraphs[0].text = "Parameterized Queries (Pool)"
    tb_lbl2.text_frame.paragraphs[0].font.size = Pt(16); tb_lbl2.text_frame.paragraphs[0].font.bold = True; tb_lbl2.text_frame.paragraphs[0].font.color.rgb = BLUE

    # Tier 3: Database
    add_flow_node(s4, 1.1, 4.8, 5.6, 0.95, "Data Tier (Relational Storage)\nMySQL 8 Relational Database (ccms_db)\n7 Normalized 3NF Tables • InnoDB Transactions", bg_color=WHITE, border_color=NAVY, text_color=NAVY, font_size=18)

    # RIGHT COLUMN: Architectural Principles & Technical Rationale
    add_card(s4, 7.3, 1.45, 5.233, 5.2, bg_color=WHITE, border_color=BORDER)
    
    tb_r = s4.shapes.add_textbox(Inches(7.55), Inches(1.65), Inches(4.75), Inches(4.8))
    tf_r = tb_r.text_frame; tf_r.word_wrap = True; tf_r.margin_left = tf_r.margin_top = 0

    p = tf_r.paragraphs[0]; p.text = "Key Architectural Principles"
    p.font.name = 'Arial'; p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = NAVY
    p.space_after = Pt(14)

    arch_points = [
        ("Separation of Concerns", "The presentation layer is strictly decoupled from storage. The client never queries the database directly; all operations pass through audited REST controllers."),
        ("Stateless Authorization", "JSON Web Tokens (JWT) eliminate server-side session memory. Each request carries cryptographic proof of role, supporting seamless horizontal scaling."),
        ("Relational Integrity & ACID", "MySQL InnoDB engine enforces strict foreign keys, atomic transactions for status transitions, and data integrity across complaint history."),
        ("Defense in Depth Security", "Layered defense combining client route guards, express-validator sanitization, parameterized queries, and bcryptjs password salting.")
    ]
    for h_txt, b_txt in arch_points:
        p = tf_r.add_paragraph()
        p.space_before = Pt(10)
        r1 = p.add_run(); r1.text = "• " + h_txt + ":\n"; r1.font.bold = True; r1.font.size = Pt(20); r1.font.color.rgb = BLUE
        r2 = p.add_run(); r2.text = b_txt; r2.font.size = Pt(19); r2.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 5: 4. COMPLAINT WORKFLOW & STATE LIFECYCLE
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "4. Complaint Workflow & Lifecycle", "Finite State Machine Enforcing Audited Status Progression")
    add_footer(s5, 5)

    # TOP: Flowchart of Primary State Lifecycle (Happy Path)
    add_card(s5, 0.8, 1.45, 11.733, 2.15, bg_color=LIGHT_BG, border_color=BORDER)
    
    tb = s5.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(11.3), Inches(0.35))
    tf = tb.text_frame; tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]; p.text = "Finite State Machine (FSM) Lifecycle Flowchart"
    p.font.name = 'Arial'; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = NAVY

    # Primary States: NEW -> VERIFIED -> ASSIGNED -> IN_PROGRESS -> RESOLVED -> CLOSED
    fsm_states = [
        ("NEW", 1.0, 1.4),
        ("VERIFIED", 2.8, 1.6),
        ("ASSIGNED", 4.8, 1.6),
        ("IN_PROGRESS", 6.8, 1.8),
        ("RESOLVED", 9.0, 1.6),
        ("CLOSED", 11.0, 1.3)
    ]
    state_y = 2.05
    for idx, (st_name, sx, sw) in enumerate(fsm_states):
        add_flow_node(s5, sx, state_y, sw, 0.55, st_name, bg_color=NAVY, border_color=NAVY, text_color=WHITE, font_size=18)
        if idx < len(fsm_states) - 1:
            add_arrow_right(s5, sx + sw + 0.08, state_y + 0.16, width=0.22, height=0.2, color=BLUE)

    # Branching States Callout below primary flow
    tb_br = s5.shapes.add_textbox(Inches(1.0), Inches(2.9), Inches(11.3), Inches(0.55))
    tf_br = tb_br.text_frame; tf_br.margin_left = tf_br.margin_top = 0
    p = tf_br.paragraphs[0]
    r1 = p.add_run(); r1.text = "Exception & Feedback Branches:  "; r1.font.bold = True; r1.font.size = Pt(19); r1.font.color.rgb = NAVY
    r2 = p.add_run(); r2.text = "• NEW / VERIFIED → REJECTED (Invalid or out-of-scope ticket dismissed with reason)\n• CLOSED → REOPENED (Student flags that recurring defect was not resolved properly)"; r2.font.size = Pt(19); r2.font.color.rgb = SLATE_TEXT

    # BOTTOM: Role Authority & Responsibilities (3 Structured Columns)
    col_w = 3.71
    col_y = 3.8
    col_h = 2.85

    # Role 1: Complainant
    add_card(s5, 0.8, col_y, col_w, col_h, bg_color=WHITE, border_color=BORDER)
    tb = s5.shapes.add_textbox(Inches(1.0), Inches(col_y + 0.15), Inches(col_w - 0.4), Inches(col_h - 0.3))
    tf = tb.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]; p.text = "1. Student / Faculty"
    p.font.name = 'Arial'; p.font.size = Pt(21); p.font.bold = True; p.font.color.rgb = BLUE
    items = [
        "Lodges complaint with building, room, and photo.",
        "Monitors real-time status & updates.",
        "Confirms repair & provides 1–5 star rating."
    ]
    for it in items:
        p = tf.add_paragraph(); p.space_before = Pt(6)
        p.text = "• " + it; p.font.size = Pt(19); p.font.color.rgb = DARK_TEXT

    # Role 2: Administrator
    add_card(s5, 4.81, col_y, col_w, col_h, bg_color=WHITE, border_color=BORDER)
    tb = s5.shapes.add_textbox(Inches(5.01), Inches(col_y + 0.15), Inches(col_w - 0.4), Inches(col_h - 0.3))
    tf = tb.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]; p.text = "2. Administrator"
    p.font.name = 'Arial'; p.font.size = Pt(21); p.font.bold = True; p.font.color.rgb = NAVY
    items = [
        "Reviews validity; marks VERIFIED or REJECTED.",
        "Assigns ticket to designated maintenance staff.",
        "Monitors SLA resolution & closes tickets."
    ]
    for it in items:
        p = tf.add_paragraph(); p.space_before = Pt(6)
        p.text = "• " + it; p.font.size = Pt(19); p.font.color.rgb = DARK_TEXT

    # Role 3: Maintenance Staff
    add_card(s5, 8.82, col_y, col_w, col_h, bg_color=WHITE, border_color=BORDER)
    tb = s5.shapes.add_textbox(Inches(9.02), Inches(col_y + 0.15), Inches(col_w - 0.4), Inches(col_h - 0.3))
    tf = tb.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]; p.text = "3. Maintenance Staff"
    p.font.name = 'Arial'; p.font.size = Pt(21); p.font.bold = True; p.font.color.rgb = GREEN_TEXT
    items = [
        "Receives work orders in dedicated queue.",
        "Transitions status to IN_PROGRESS upon start.",
        "Records diagnostic remarks & marks RESOLVED."
    ]
    for it in items:
        p = tf.add_paragraph(); p.space_before = Pt(6)
        p.text = "• " + it; p.font.size = Pt(19); p.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 6: 5. MAJOR MODULES & TECHNOLOGY STACK
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "5. Major Modules & Tech Stack", "Cohesive Functional Modules Mapped to Modern Technologies")
    add_footer(s6, 6)

    # LEFT COLUMN: Major Functional Modules
    add_card(s6, 0.8, 1.45, 5.7, 5.2, bg_color=LIGHT_BG, border_color=BORDER)
    
    tb_m = s6.shapes.add_textbox(Inches(1.05), Inches(1.65), Inches(5.2), Inches(4.8))
    tf_m = tb_m.text_frame; tf_m.word_wrap = True; tf_m.margin_left = tf_m.margin_top = 0
    p = tf_m.paragraphs[0]; p.text = "Major System Modules"
    p.font.name = 'Arial'; p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = NAVY
    p.space_after = Pt(12)

    modules_data = [
        ("Authentication & RBAC", "User registration, bcryptjs hashing, JWT token issuance, and Student/Faculty/Maintenance/Admin route protection."),
        ("Complaint Lodging", "Dynamic React form mapping issues to campus buildings & rooms, Multer image upload, unique CMP-ID generation."),
        ("Admin Control Center", "Campus-wide ticket visibility, multi-criteria filtering, one-click verify/reject, and technician allocation."),
        ("Maintenance Task Queue", "Staff-focused work order queue with real-time status transitions (In Progress) and resolution remarks logging."),
        ("Audit History & Feedback", "Append-only status history in complaint_updates and 1 to 5 star user feedback collection.")
    ]
    for m_title, m_desc in modules_data:
        p = tf_m.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run(); r1.text = f"• {m_title}: "; r1.font.bold = True; r1.font.size = Pt(20); r1.font.color.rgb = BLUE
        r2 = p.add_run(); r2.text = m_desc; r2.font.size = Pt(19); r2.font.color.rgb = DARK_TEXT

    # RIGHT COLUMN: Actual Technology Stack (Categorized)
    add_card(s6, 6.833, 1.45, 5.7, 5.2, bg_color=WHITE, border_color=BORDER)
    
    tb_t = s6.shapes.add_textbox(Inches(7.083), Inches(1.65), Inches(5.2), Inches(4.8))
    tf_t = tb_t.text_frame; tf_t.word_wrap = True; tf_t.margin_left = tf_t.margin_top = 0
    p = tf_t.paragraphs[0]; p.text = "Production Technology Stack"
    p.font.name = 'Arial'; p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = NAVY
    p.space_after = Pt(12)

    tech_categories = [
        ("Frontend Tier", "React 18.2 SPA, Vite 5.0 (Build Tool), Tailwind CSS 3.3 (Styling), React Router v6, Axios 1.6"),
        ("Backend Tier", "Node.js 18+ LTS, Express.js 4.19 REST API, express-validator, Multer 1.4 (Evidence Upload)"),
        ("Database & Storage", "MySQL 8.0 Relational DBMS, mysql2 3.9 Connection Pool, 7 Normalized 3NF Tables, InnoDB Engine"),
        ("Security & Tooling", "JSON Web Tokens (JWT HS256), bcryptjs (10 salt rounds), Git & GitHub, Playwright Test Runner")
    ]
    for c_title, c_tech in tech_categories:
        p = tf_t.add_paragraph()
        p.space_before = Pt(12)
        r1 = p.add_run(); r1.text = f"{c_title}\n"; r1.font.bold = True; r1.font.size = Pt(21); r1.font.color.rgb = NAVY
        r2 = p.add_run(); r2.text = c_tech; r2.font.size = Pt(20); r2.font.color.rgb = SLATE_TEXT

    # =========================================================================
    # SLIDE 7: 6. DATABASE DESIGN & CORE DATA MODEL
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "6. Database Design & Data Model", "Normalized 3NF Relational Schema with Immutable Audit Trail")
    add_footer(s7, 7)

    # TOP: Visual Relational Entity Structure
    add_card(s7, 0.8, 1.45, 11.733, 2.5, bg_color=LIGHT_BG, border_color=BORDER)
    
    tb = s7.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(11.3), Inches(0.35))
    tf = tb.text_frame; tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]; p.text = "Core Relational Entities & Associations"
    p.font.name = 'Arial'; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = NAVY

    # Entity Boxes
    # Row 1: Users, Categories, Locations
    add_flow_node(s7, 1.0, 2.0, 3.6, 0.85, "USERS\nid, name, email, role, department", bg_color=WHITE, border_color=NAVY, text_color=NAVY, font_size=18)
    add_flow_node(s7, 4.86, 2.0, 3.6, 0.85, "COMPLAINTS (Core Entity)\nid, complaint_no, priority, status", bg_color=NAVY, border_color=NAVY, text_color=WHITE, font_size=18)
    add_flow_node(s7, 8.73, 2.0, 3.6, 0.85, "LOCATIONS & CATEGORIES\nbuilding, floor, room, category_name", bg_color=WHITE, border_color=NAVY, text_color=NAVY, font_size=18)

    # Row 2: Assignments, Updates, Feedback
    add_flow_node(s7, 1.0, 3.0, 3.6, 0.8, "COMPLAINT_ASSIGNMENTS\nstaff_id, assigned_by, assigned_at", bg_color=WHITE, border_color=BLUE, text_color=BLUE, font_size=17)
    add_flow_node(s7, 4.86, 3.0, 3.6, 0.8, "COMPLAINT_UPDATES (Audit Log)\nold_status, new_status, remarks", bg_color=WHITE, border_color=BLUE, text_color=BLUE, font_size=17)
    add_flow_node(s7, 8.73, 3.0, 3.6, 0.8, "FEEDBACK\nuser_id, rating (1-5), comments", bg_color=WHITE, border_color=BLUE, text_color=BLUE, font_size=17)

    # BOTTOM: Relational Engineering Decisions (3 Clean Cards)
    b_card_w = 3.71
    b_card_y = 4.15
    b_card_h = 2.5

    decisions = [
        ("Third Normal Form (3NF)", "Redundancy eliminated. Campus locations and categories are stored as independent master tables, allowing dynamic additions without schema alterations.", NAVY),
        ("Immutable Audit Trail", "All lifecycle transitions insert a new record into complaint_updates with old/new status, operator ID, and timestamp, guaranteeing complete accountability.", BLUE),
        ("Referential Integrity", "Foreign key constraints with RESTRICT/CASCADE rules prevent orphaned records. Inactive users and locations are flagged rather than deleted.", GREEN_TEXT)
    ]
    for idx, (d_title, d_desc, d_color) in enumerate(decisions):
        dx = 0.8 + idx * (b_card_w + 0.3)
        add_card(s7, dx, b_card_y, b_card_w, b_card_h, bg_color=WHITE, border_color=BORDER)
        tb_d = s7.shapes.add_textbox(Inches(dx + 0.2), Inches(b_card_y + 0.15), Inches(b_card_w - 0.4), Inches(b_card_h - 0.3))
        tf_d = tb_d.text_frame; tf_d.word_wrap = True; tf_d.margin_left = tf_d.margin_top = 0
        p = tf_d.paragraphs[0]; p.text = d_title
        p.font.name = 'Arial'; p.font.size = Pt(21); p.font.bold = True; p.font.color.rgb = d_color
        p2 = tf_d.add_paragraph(); p2.space_before = Pt(8)
        p2.text = d_desc; p2.font.name = 'Arial'; p2.font.size = Pt(19); p2.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 8: 7. IMPLEMENTED SYSTEM — APPLICATION SCREENS
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "7. Implemented Application Screens", "Authentic User Interfaces Captured from the Running CCMS Application")
    add_footer(s8, 8)

    # Two Large Screenshots Side-by-Side with Numbered Callouts
    scr_w = 5.6
    scr_h = 3.5
    scr_y = 1.5

    # Screen 1: Admin Dashboard & Triage
    add_card(s8, 0.8, scr_y, scr_w, scr_h + 1.6, bg_color=WHITE, border_color=BORDER)
    if os.path.exists("docs/screenshots/07_admin_dashboard.png"):
        s8.shapes.add_picture("docs/screenshots/07_admin_dashboard.png", Inches(0.9), Inches(scr_y + 0.1), width=Inches(scr_w - 0.2))

    tb_call1 = s8.shapes.add_textbox(Inches(0.95), Inches(scr_y + scr_h + 0.15), Inches(scr_w - 0.3), Inches(1.3))
    tf_call1 = tb_call1.text_frame; tf_call1.word_wrap = True; tf_call1.margin_left = tf_call1.margin_top = 0
    p = tf_call1.paragraphs[0]; p.text = "1. Administrator Control Center"
    p.font.name = 'Arial'; p.font.size = Pt(21); p.font.bold = True; p.font.color.rgb = NAVY
    p2 = tf_call1.add_paragraph(); p2.space_before = Pt(4)
    p2.text = "① Real-Time Campus KPIs: Total, open, resolved, and critical ticket tallies.\n② Governance & Triage: Instant search, category filters, and verify/reject controls."
    p2.font.name = 'Arial'; p2.font.size = Pt(19); p2.font.color.rgb = DARK_TEXT

    # Screen 2: Technician Task Queue
    add_card(s8, 6.933, scr_y, scr_w, scr_h + 1.6, bg_color=WHITE, border_color=BORDER)
    if os.path.exists("docs/screenshots/15_maintenance_tasks.png"):
        s8.shapes.add_picture("docs/screenshots/15_maintenance_tasks.png", Inches(7.033), Inches(scr_y + 0.1), width=Inches(scr_w - 0.2))

    tb_call2 = s8.shapes.add_textbox(Inches(7.083), Inches(scr_y + scr_h + 0.15), Inches(scr_w - 0.3), Inches(1.3))
    tf_call2 = tb_call2.text_frame; tf_call2.word_wrap = True; tf_call2.margin_left = tf_call2.margin_top = 0
    p = tf_call2.paragraphs[0]; p.text = "2. Technician Work Order Queue"
    p.font.name = 'Arial'; p.font.size = Pt(21); p.font.bold = True; p.font.color.rgb = GREEN_TEXT
    p2 = tf_call2.add_paragraph(); p2.space_before = Pt(4)
    p2.text = "① Focused Dispatching: Displays exact campus building, floor, room, and urgency.\n② Work Execution: Single-click 'Start Work' and diagnostic resolution remarks submission."
    p2.font.name = 'Arial'; p2.font.size = Pt(19); p2.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 9: 8. TESTING & QUALITY VERIFICATION
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "8. Testing & Quality Verification", "Rigorous Multi-Level Verification with 100% Pass Rate")
    add_footer(s9, 9)

    # LEFT COLUMN: Testing Methodology & Basis Path Metrics
    add_card(s9, 0.8, 1.45, 4.8, 5.2, bg_color=LIGHT_BG, border_color=BORDER)
    
    tb_test = s9.shapes.add_textbox(Inches(1.05), Inches(1.65), Inches(4.3), Inches(4.8))
    tf_test = tb_test.text_frame; tf_test.word_wrap = True; tf_test.margin_left = tf_test.margin_top = 0
    p = tf_test.paragraphs[0]; p.text = "Verification Methodology"
    p.font.name = 'Arial'; p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = NAVY
    p.space_after = Pt(10)

    t_methods = [
        ("Unit Testing", "Validated bcrypt password salting, token signing/verification, and unique CMP-ID generators."),
        ("Basis Path Testing", "Mapped Cyclomatic Complexity V(G) = 11 for statusController.js; validated all legal and illegal transition branches."),
        ("Role Access Boundary", "Verified that student tokens cannot access administrative or technician endpoints (HTTP 403 Forbidden)."),
        ("System Integration", "Automated browser validation via Playwright confirming end-to-end user journeys.")
    ]
    for m_title, m_desc in t_methods:
        p = tf_test.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run(); r1.text = "• " + m_title + ":\n"; r1.font.bold = True; r1.font.size = Pt(20); r1.font.color.rgb = BLUE
        r2 = p.add_run(); r2.text = m_desc; r2.font.size = Pt(19); r2.font.color.rgb = DARK_TEXT

    # Summary Badge
    p_badge = tf_test.add_paragraph()
    p_badge.space_before = Pt(14)
    r_b = p_badge.add_run(); r_b.text = "✓ 30 / 30 Test Cases PASSED (100%)"; r_b.font.bold = True; r_b.font.size = Pt(20); r_b.font.color.rgb = GREEN_TEXT

    # RIGHT COLUMN: Executed Test Results Table
    t_shape = s9.shapes.add_table(7, 4, Inches(5.8), Inches(1.45), Inches(6.733), Inches(5.2))
    tbl = t_shape.table
    tbl.columns[0].width = Inches(1.0)
    tbl.columns[1].width = Inches(2.2)
    tbl.columns[2].width = Inches(2.533)
    tbl.columns[3].width = Inches(1.0)

    test_headers = ["Test ID", "Scenario Evaluated", "Observed Result", "Status"]
    for c_idx, h_text in enumerate(test_headers):
        cell = tbl.cell(0, c_idx)
        cell.fill.solid(); cell.fill.fore_color.rgb = NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h_text; p.font.name = 'Arial'; p.font.size = Pt(19); p.font.bold = True; p.font.color.rgb = WHITE
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
            cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 0 else LIGHT_BG
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = 'Arial'; p.font.size = Pt(18)
            if c_idx == 0:
                p.font.bold = True; p.font.color.rgb = NAVY; p.alignment = PP_ALIGN.CENTER
            elif c_idx == 3:
                p.font.bold = True; p.font.color.rgb = GREEN_TEXT; p.alignment = PP_ALIGN.CENTER
            else:
                p.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 10: 9. CONCLUSION & FUTURE SCOPE
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "9. Conclusion & Future Scope", "Engineering Milestones, Current Constraints & System Roadmap")
    add_footer(s10, 10)

    # 3 Structured Vertical Columns: Achievements | Limitations | Future Scope
    col_w3 = 3.71
    col_y3 = 1.45
    col_h3 = 4.45

    # Column 1: Achievements
    add_card(s10, 0.8, col_y3, col_w3, col_h3, bg_color=GREEN_BG, border_color=GREEN_BORDER)
    tb1 = s10.shapes.add_textbox(Inches(1.0), Inches(col_y3 + 0.15), Inches(col_w3 - 0.4), Inches(col_h3 - 0.3))
    tf1 = tb1.text_frame; tf1.word_wrap = True; tf1.margin_left = tf1.margin_top = 0
    p = tf1.paragraphs[0]; p.text = "What CCMS Achieved"
    p.font.name = 'Arial'; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = GREEN_TEXT
    achievements = [
        "Eliminated error-prone manual logbooks with a 24/7 web-based grievance ecosystem.",
        "Enforced strict role-based access across Student, Faculty, Staff, and Admin.",
        "Implemented an audited Finite State Machine preventing illegal status jumps.",
        "Established an immutable audit log ensuring complete administrative transparency."
    ]
    for ach in achievements:
        p = tf1.add_paragraph(); p.space_before = Pt(8)
        p.text = "✓ " + ach; p.font.size = Pt(19); p.font.color.rgb = DARK_TEXT

    # Column 2: Current Constraints
    add_card(s10, 4.81, col_y3, col_w3, col_h3, bg_color=AMBER_BG, border_color=AMBER_BORDER)
    tb2 = s10.shapes.add_textbox(Inches(5.01), Inches(col_y3 + 0.15), Inches(col_w3 - 0.4), Inches(col_h3 - 0.3))
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
    add_card(s10, 8.82, col_y3, col_w3, col_h3, bg_color=BLUE_BG, border_color=BLUE_BORDER)
    tb3 = s10.shapes.add_textbox(Inches(9.02), Inches(col_y3 + 0.15), Inches(col_w3 - 0.4), Inches(col_h3 - 0.3))
    tf3 = tb3.text_frame; tf3.word_wrap = True; tf3.margin_left = tf3.margin_top = 0
    p = tf3.paragraphs[0]; p.text = "Future Roadmap"
    p.font.name = 'Arial'; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = BLUE
    future = [
        "Integration of Nodemailer (SMTP) and Twilio (SMS) for automated alerts.",
        "Migration of evidence storage to Amazon S3 / Cloudinary cloud buckets.",
        "Development of cross-platform mobile app using React Native.",
        "Automated technician dispatching based on active workload and trade skills."
    ]
    for fut in future:
        p = tf3.add_paragraph(); p.space_before = Pt(8)
        p.text = "→ " + fut; p.font.size = Pt(19); p.font.color.rgb = DARK_TEXT

    # BOTTOM BANNER: Thank You & Viva Q&A
    tb_thank = s10.shapes.add_textbox(Inches(0.8), Inches(6.05), Inches(11.733), Inches(0.65))
    tf_thank = tb_thank.text_frame; tf_thank.margin_left = tf_thank.margin_top = 0
    p_thank = tf_thank.paragraphs[0]
    p_thank.alignment = PP_ALIGN.CENTER
    p_thank.text = "Thank You  |  Questions & Answers"
    p_thank.font.name = 'Arial'; p_thank.font.size = Pt(26); p_thank.font.bold = True; p_thank.font.color.rgb = NAVY

    # Save presentation
    output_path = "Campus_Complaint_Management_System_Mini_Project_Presentation.pptx"
    prs.save(output_path)
    print(f"Redesigned presentation successfully saved to: {output_path}")

if __name__ == "__main__":
    build_presentation()
