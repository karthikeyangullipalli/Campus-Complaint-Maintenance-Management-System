import os
import time
from playwright.sync_api import sync_playwright

os.makedirs('docs/diagrams', exist_ok=True)

diagrams = {
    "fig01_dfd_level0": """
flowchart LR
    Student["Student / Faculty"]
    Admin["Administrator"]
    Staff["Maintenance Staff"]
    CCMS(("0<br/><b>Campus Complaint &<br/>Maintenance Management<br/>System (CCMS)</b>"))

    Student -->|"Complaint Details, Evidence Image,<br/>Feedback Rating, Credentials"| CCMS
    CCMS -->|"Complaint Status, Reference ID,<br/>Resolution History"| Student

    Admin -->|"Verification Decision, Staff Assignment,<br/>Category/Location Setup, Credentials"| CCMS
    CCMS -->|"All Complaints, System Analytics,<br/>User Records, Status Logs"| Admin

    Staff -->|"Work Progress Updates,<br/>Resolution Remarks, Credentials"| CCMS
    CCMS -->|"Assigned Task Details,<br/>Location & Category Data"| Staff
""",

    "fig02_dfd_level1": """
flowchart TD
    User["Student / Faculty"]
    Admin["Administrator"]
    Staff["Maintenance Staff"]

    P1(("1.0<br/>Authentication &<br/>Access Control"))
    P2(("2.0<br/>Complaint Registration<br/>& Lodging"))
    P3(("3.0<br/>Verification &<br/>Review"))
    P4(("4.0<br/>Maintenance Task<br/>Assignment"))
    P5(("5.0<br/>Work Execution &<br/>Status Update"))
    P6(("6.0<br/>Closure &<br/>Feedback"))
    P7(("7.0<br/>Dashboard &<br/>System Admin"))

    D1[("D1: Users DB")]
    D2[("D2: Complaints DB")]
    D3[("D3: Categories & Locations DB")]
    D4[("D4: Complaint Updates / Audit Log")]
    D5[("D5: Feedback DB")]

    User -->|"Login / Register"| P1
    Admin -->|"Login Credentials"| P1
    Staff -->|"Login Credentials"| P1
    P1 <-->|"Verify & Read/Write"| D1
    P1 -->|"JWT Token"| User
    P1 -->|"JWT Token"| Admin
    P1 -->|"JWT Token"| Staff

    User -->|"Complaint Form & Image"| P2
    P2 <-->|"Fetch Active Cat & Loc"| D3
    P2 -->|"Save Complaint (NEW)"| D2
    P2 -->|"Initial Status Log"| D4
    P2 -->|"Complaint Reference ID"| User

    Admin -->|"Verify / Reject Decision"| P3
    P3 <-->|"Read & Update Status"| D2
    P3 -->|"Log Status Change"| D4

    Admin -->|"Assign Staff ID & Notes"| P4
    P4 <-->|"Update Status (ASSIGNED)"| D2
    P4 -->|"Create Assignment Record"| D4
    P4 -->|"Task Details"| Staff

    Staff -->|"Accept & Mark RESOLVED"| P5
    P5 <-->|"Update Status (IN_PROGRESS/RESOLVED)"| D2
    P5 -->|"Log Remarks & Timestamps"| D4

    User -->|"Rating & Comments"| P6
    Admin -->|"Confirm Closure"| P6
    P6 -->|"Store Rating"| D5
    P6 <-->|"Update Status (CLOSED/REOPENED)"| D2
    P6 -->|"Log Closure/Reopen"| D4

    Admin -->|"Query System Stats"| P7
    P7 <-->|"Aggregate Metrics"| D1
    P7 <-->|"Aggregate Metrics"| D2
    P7 <-->|"Read Audit"| D4
    P7 -->|"Dashboard Overview"| Admin
""",

    "fig03_dfd_level2": """
flowchart TD
    User["Student / Faculty"]
    Admin["Administrator"]

    D2[("D2: Complaints DB")]
    D3[("D3: Categories & Locations DB")]
    D4[("D4: Complaint Updates DB")]

    P21(("2.1<br/>Input Validation<br/>& Sanitization"))
    P22(("2.2<br/>Fetch Category &<br/>Location Context"))
    P23(("2.3<br/>Generate Unique ID<br/>& Store Record"))
    P24(("2.4<br/>Initialize Audit<br/>History Record"))

    User -->|"Title, Description, Priority,<br/>Category, Location, Image"| P21
    P21 -->|"Validated Fields"| P22
    P22 <-->|"Verify Category & Location IDs"| D3
    P22 -->|"Formatted Record"| P23
    P23 -->|"Insert Complaint (Status: NEW)"| D2
    P23 -->|"Generated CMP-ID"| User
    P23 -->|"Complaint ID & User ID"| P24
    P24 -->|"Log Status 'NEW' by Submitter"| D4
""",

    "fig04_architecture": """
flowchart TD
    subgraph ClientLayer["Presentation Layer (Client Tier - React 18 + Vite)"]
        UI["Web Browser (Chrome / Edge / Firefox)"]
        Components["React Components & Pages<br/>(StudentLayout, AdminLayout, MaintenanceLayout)"]
        Axios["Axios HTTP Client with JWT Request Interceptor<br/>(Bearer Token Injection & Base URL /api)"]
        UI --> Components --> Axios
    end

    subgraph ServerLayer["Application Layer (Server Tier - Node.js + Express 4)"]
        Middleware["Express Middleware<br/>(CORS, JSON Parser, verifyToken, requireRole, Multer)"]
        Routes["RESTful API Route Controllers<br/>(auth, complaints, assignments, dashboard, users, categories, locations)"]
        Service["Business Logic & State Validation<br/>(VALID_TRANSITIONS FSM, bcryptjs, Password Sanitization)"]
        Axios -->|"HTTPS / JSON REST Calls"| Middleware
        Middleware --> Routes --> Service
    end

    subgraph DataLayer["Data Layer (Storage Tier - MySQL 8 Relational Database)"]
        Pool["MySQL2 Connection Pool<br/>(Promise-based, Parameterized Queries)"]
        Tables["Relational Tables (InnoDB, UTF8mb4)<br/>users | complaints | complaint_categories | locations<br/>complaint_assignments | complaint_updates | feedback"]
        Service --> Pool --> Tables
    end
""",

    "fig05_datamodel": """
erDiagram
    USERS ||--o{ COMPLAINTS : "submits"
    USERS ||--o{ COMPLAINT_ASSIGNMENTS : "assigned_to / assigned_by"
    USERS ||--o{ COMPLAINT_UPDATES : "updated_by"
    USERS ||--o{ FEEDBACK : "submits"
    
    COMPLAINT_CATEGORIES ||--o{ COMPLAINTS : "categorizes"
    LOCATIONS ||--o{ COMPLAINTS : "locates"
    
    COMPLAINTS ||--o{ COMPLAINT_ASSIGNMENTS : "assigned_in"
    COMPLAINTS ||--o{ COMPLAINT_UPDATES : "tracked_by"
    COMPLAINTS ||--o| FEEDBACK : "evaluated_in"

    USERS {
        int id PK
        string name
        string email UK
        string password_hash
        enum role "STUDENT, FACULTY, MAINTENANCE, ADMIN"
        string department
        string phone
        boolean is_active
        timestamp created_at
    }

    COMPLAINT_CATEGORIES {
        int id PK
        string name UK
        string description
        boolean is_active
        timestamp created_at
    }

    LOCATIONS {
        int id PK
        string building
        string floor
        string room
        string description
        boolean is_active
        timestamp created_at
    }

    COMPLAINTS {
        int id PK
        string complaint_number UK
        int user_id FK
        int category_id FK
        int location_id FK
        string title
        text description
        enum priority "LOW, MEDIUM, HIGH, CRITICAL"
        enum status "NEW, VERIFIED, ASSIGNED, IN_PROGRESS, RESOLVED, CLOSED, REJECTED, REOPENED"
        string image_path
        timestamp created_at
        timestamp resolved_at
        timestamp closed_at
    }

    COMPLAINT_ASSIGNMENTS {
        int id PK
        int complaint_id FK
        int maintenance_staff_id FK
        int assigned_by FK
        timestamp assigned_at
        text notes
    }

    COMPLAINT_UPDATES {
        int id PK
        int complaint_id FK
        int updated_by FK
        string old_status
        string new_status
        text remarks
        timestamp created_at
    }

    FEEDBACK {
        int id PK
        int complaint_id FK
        int user_id FK
        int rating "1 to 5"
        text comments
        timestamp created_at
    }
""",

    "fig06_usecase": """
flowchart LR
    subgraph Actors
        Student["Student / Faculty"]
        Admin["Administrator"]
        Staff["Maintenance Staff"]
    end

    subgraph CCMS["Campus Complaint Management System"]
        UC01(["UC01: Register / Login"])
        UC02(["UC02: Submit Complaint & Upload Image"])
        UC03(["UC03: Track Own Complaints & History"])
        UC04(["UC04: Submit Resolution Feedback"])
        UC05(["UC05: Reopen Unresolved Complaint"])
        UC06(["UC06: Verify / Reject Complaint"])
        UC07(["UC07: Assign Complaint to Staff"])
        UC08(["UC08: Close Resolved Complaint"])
        UC09(["UC09: Manage Users, Categories & Locations"])
        UC10(["UC10: View Admin Metrics & Dashboard"])
        UC11(["UC11: View Assigned Maintenance Tasks"])
        UC12(["UC12: Update Work Status & Add Remarks"])
    end

    Student --> UC01
    Student --> UC02
    Student --> UC03
    Student --> UC04
    Student --> UC05

    Admin --> UC01
    Admin --> UC06
    Admin --> UC07
    Admin --> UC08
    Admin --> UC09
    Admin --> UC10

    Staff --> UC01
    Staff --> UC11
    Staff --> UC12
""",

    "fig07_class": """
classDiagram
    class User {
        +int id
        +string name
        +string email
        +string password_hash
        +string role
        +string department
        +string phone
        +boolean is_active
        +timestamp created_at
        +login(email, password)
        +logout()
    }

    class Complaint {
        +int id
        +string complaint_number
        +int user_id
        +int category_id
        +int location_id
        +string title
        +string description
        +string priority
        +string status
        +string image_path
        +timestamp created_at
        +timestamp resolved_at
        +timestamp closed_at
        +createComplaint()
        +updateStatus(new_status)
    }

    class ComplaintCategory {
        +int id
        +string name
        +string description
        +boolean is_active
        +getCategories()
    }

    class Location {
        +int id
        +string building
        +string floor
        +string room
        +string description
        +boolean is_active
        +getDisplayName()
    }

    class ComplaintAssignment {
        +int id
        +int complaint_id
        +int maintenance_staff_id
        +int assigned_by
        +timestamp assigned_at
        +string notes
        +assignStaff()
    }

    class ComplaintUpdate {
        +int id
        +int complaint_id
        +int updated_by
        +string old_status
        +string new_status
        +string remarks
        +timestamp created_at
        +logUpdate()
    }

    class Feedback {
        +int id
        +int complaint_id
        +int user_id
        +int rating
        +string comments
        +timestamp created_at
        +submitFeedback()
    }

    User "1" --> "*" Complaint : "lodges"
    ComplaintCategory "1" --> "*" Complaint : "classifies"
    Location "1" --> "*" Complaint : "locates"
    Complaint "1" --> "*" ComplaintAssignment : "receives"
    User "1" --> "*" ComplaintAssignment : "executes/assigns"
    Complaint "1" --> "*" ComplaintUpdate : "audited_by"
    User "1" --> "*" ComplaintUpdate : "authorized_by"
    Complaint "1" --> "0..1" Feedback : "evaluated_by"
    User "1" --> "*" Feedback : "submits"
""",

    "fig08_sequence_submit": """
sequenceDiagram
    autonumber
    actor Student as Student / Faculty
    participant UI as React UI (NewComplaint)
    participant Client as Axios Client (api.js)
    participant Server as Express REST API
    participant DB as MySQL Database

    Student->>UI: Fills form (Title, Category, Location, Priority, Description, Image)
    Student->>UI: Clicks "Submit Complaint"
    UI->>Client: Formats multipart FormData payload
    Client->>Server: POST /api/complaints (Bearer JWT Header)
    Server->>Server: verifyToken checks JWT signature & active status
    Server->>Server: generateComplaintId() -> CMP-YYYYMMDD-XXXXXX
    Server->>DB: INSERT INTO complaints (title, category_id, location_id, priority, status='NEW'...)
    DB-->>Server: Insert Success (insertId)
    Server->>DB: INSERT INTO complaint_updates (complaint_id, updated_by, new_status='NEW', remarks='Complaint submitted')
    DB-->>Server: Audit Log Stored
    Server-->>Client: 201 Created { success: true, complaintId, complaint_number }
    Client-->>UI: Response received
    UI-->>Student: Displays success & redirects to Complaint Detail view
""",

    "fig09_sequence_assign": """
sequenceDiagram
    autonumber
    actor Admin as Administrator
    participant UI as Admin ComplaintDetail
    participant Client as Axios Client (api.js)
    participant Server as Express REST API
    participant DB as MySQL Database
    actor Staff as Maintenance Staff

    Admin->>UI: Opens NEW complaint
    Admin->>UI: Clicks "Verify Complaint"
    UI->>Client: PUT /api/complaints/:id/status { new_status: 'VERIFIED' }
    Client->>Server: Request with JWT Header
    Server->>Server: Check role == 'ADMIN' & VALID_TRANSITIONS['NEW']->'VERIFIED'
    Server->>DB: UPDATE complaints SET status='VERIFIED' WHERE id=:id
    Server->>DB: INSERT INTO complaint_updates (status='VERIFIED', updated_by=adminId)
    Server-->>Client: 200 OK { success: true }
    Client-->>UI: Complaint marked VERIFIED

    Admin->>UI: Selects Maintenance Staff & enters assignment notes
    Admin->>UI: Clicks "Assign Staff"
    UI->>Client: POST /api/complaints/:id/assign { maintenance_staff_id, notes }
    Client->>Server: Request with JWT Header
    Server->>Server: Validate staff exists & role == 'MAINTENANCE'
    Server->>DB: INSERT INTO complaint_assignments (complaint_id, staff_id, assigned_by, notes)
    Server->>DB: UPDATE complaints SET status='ASSIGNED' WHERE id=:id
    Server->>DB: INSERT INTO complaint_updates (status='ASSIGNED', remarks='Assigned to staff...')
    Server-->>Client: 200 OK { success: true }
    Client-->>UI: Complaint view updated with assigned staff info
    Staff->>UI: Later logs in and sees task on Maintenance Dashboard
""",

    "fig10_activity": """
flowchart TD
    Start([User Logs In]) --> CheckRole{User Role?}
    
    CheckRole -->|Student / Faculty| StuAction[Open New Complaint Form]
    StuAction --> FillForm[Select Category, Location, Priority & Enter Description]
    FillForm --> Submit[Submit Complaint -> Status: NEW]
    Submit --> Track[View Status on Student Dashboard]

    CheckRole -->|Administrator| AdminReview[Admin Reviews Complaints on Dashboard]
    Track -.-> AdminReview
    AdminReview --> ValidCheck{Is Complaint Valid?}
    
    ValidCheck -->|No| Reject[Admin Rejects -> Status: REJECTED]
    Reject --> EndTerm([Process Completed])
    
    ValidCheck -->|Yes| Verify[Admin Verifies -> Status: VERIFIED]
    Verify --> Assign[Admin Allocates Staff -> Status: ASSIGNED]

    CheckRole -->|Maintenance Staff| StaffTasks[Staff Views Assigned Tasks]
    Assign -.-> StaffTasks
    StaffTasks --> AcceptTask[Staff Accepts -> Status: IN_PROGRESS]
    AcceptTask --> Work[Perform Repair / Maintenance Work]
    Work --> Resolve[Staff Adds Remarks -> Status: RESOLVED]

    Resolve --> UserReview{Is Issue Satisfactorily Resolved?}
    UserReview -->|Yes| Feedback[Student Submits Rating & Comments]
    Feedback --> Close[Admin / User Closes -> Status: CLOSED]
    Close --> EndTerm
    
    UserReview -->|No - Persists| Reopen[User Reopens -> Status: REOPENED]
    Reopen --> Assign
""",

    "fig11_state": """
stateDiagram-v2
    [*] --> NEW : Student / Faculty submits complaint

    NEW --> VERIFIED : Admin verifies genuineness
    NEW --> REJECTED : Admin rejects (duplicate / out of scope)

    VERIFIED --> ASSIGNED : Admin allocates to maintenance staff
    VERIFIED --> REJECTED : Admin rejects upon technical review

    ASSIGNED --> IN_PROGRESS : Maintenance staff accepts & begins repair

    IN_PROGRESS --> RESOLVED : Maintenance staff completes repair & enters remarks

    RESOLVED --> CLOSED : User or Admin confirms fix is satisfactory
    RESOLVED --> REOPENED : User reports issue still persists

    CLOSED --> REOPENED : Issue reoccurs after formal closure

    REOPENED --> VERIFIED : Admin reviews reoccurrence
    REOPENED --> ASSIGNED : Admin reassigns to maintenance staff

    REJECTED --> [*]
    CLOSED --> [*]
""",

    "fig12_component": """
flowchart TD
    subgraph FrontendComponents["React 18 Client Components (SPA)"]
        AuthContext["AuthContext<br/>(JWT Token & User State)"]
        APIModule["api.js<br/>(Axios Instance & Interceptors)"]
        CommonComp["Common Components<br/>(Navbar, Sidebar, StatusBadge, PriorityBadge)"]
        StudentPages["Student Pages<br/>(StudentDashboard, NewComplaint, ComplaintList, ComplaintDetail)"]
        AdminPages["Admin Pages<br/>(AdminDashboard, AdminComplaints, UsersPage, CategoriesPage, LocationsPage, AssignmentsPage)"]
        MaintPages["Maintenance Pages<br/>(MaintenanceDashboard, MyTasks, TaskDetail)"]

        AuthContext --> APIModule
        APIModule --> StudentPages
        APIModule --> AdminPages
        APIModule --> MaintPages
    end

    subgraph BackendComponents["Express.js Server Components (REST API)"]
        AuthMiddleware["Authentication & Authorization<br/>(verifyToken, requireRole)"]
        UploadMiddleware["Multer Upload Handler<br/>(Image validation & storage)"]
        
        AuthCtrl["authController<br/>(register, login, getMe)"]
        ComplaintCtrl["complaintController<br/>(CRUD, status history, role filter)"]
        AssignCtrl["assignmentController<br/>(assignComplaint, getMyAssignments)"]
        StatusCtrl["statusController<br/>(FSM transition validator)"]
        DashCtrl["dashboardController<br/>(role-specific metrics)"]
        FeedbackCtrl["feedbackController<br/>(ratings & comments)"]
        RefCtrl["categoryController / locationController / userController<br/>(Reference Data Management)"]

        AuthMiddleware --> AuthCtrl
        AuthMiddleware --> ComplaintCtrl
        AuthMiddleware --> AssignCtrl
        AuthMiddleware --> StatusCtrl
        AuthMiddleware --> DashCtrl
        AuthMiddleware --> FeedbackCtrl
        AuthMiddleware --> RefCtrl
        UploadMiddleware --> ComplaintCtrl
    end

    subgraph DataStorage["MySQL 8 Database"]
        MySQL[("ccms_db Relational Tables<br/>InnoDB Engine, Foreign Key Constraints")]
    end

    APIModule -->|"REST / HTTPS"| AuthMiddleware
    BackendComponents -->|"MySQL2 Connection Pool"| MySQL
""",

    "fig13_deployment": """
flowchart TD
    subgraph ClientNode["Client Device (Desktop / Laptop / Mobile Device)"]
        Browser["Modern Web Browser<br/>(Google Chrome, Microsoft Edge, Mozilla Firefox)<br/>Runs React 18 SPA (HTML5, JS Bundle, Tailwind CSS)"]
    end

    subgraph WebServerNode["Application Server Node (Host / Cloud VM)"]
        NodeServer["Node.js 18+ LTS Runtime"]
        ExpressApp["Express.js 4 REST API (Port 5000)<br/>Routes, JWT Verification, Role Guards"]
        LocalStorage["Local File Storage<br/>backend/uploads/ (Uploaded Complaint Evidence Images)"]
        NodeServer --> ExpressApp
        ExpressApp --> LocalStorage
    end

    subgraph DBServerNode["Database Server Node (Dedicated / Localhost)"]
        MySQLServer["MySQL 8.0 Server (Port 3306)<br/>Relational Database Engine: ccms_db<br/>7 Tables with Foreign Keys & B-Tree Indexes"]
    end

    Browser -->|"HTTP / HTTPS (Port 5173 / Port 80)<br/>JSON Payloads with Bearer JWT"| ExpressApp
    ExpressApp -->|"TCP Connection (Port 3306)<br/>Parameterized SQL Queries via MySQL2 Pool"| MySQLServer
"""
}

html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({
            startOnLoad: true,
            theme: 'neutral',
            flowchart: { curve: 'linear' },
            fontFamily: 'Arial, sans-serif',
            fontSize: 14
        });
    </script>
    <style>
        body {
            background-color: #ffffff;
            margin: 0;
            padding: 30px;
            display: inline-block;
        }
        .mermaid {
            background-color: #ffffff;
        }
    </style>
</head>
<body>
    <div class="mermaid">
__MERMAID_CODE__
    </div>
</body>
</html>"""

print("Starting Playwright Chrome to render all 13 diagrams...")
with sync_playwright() as p:
    browser = p.chromium.launch(channel='chrome')
    
    for name, code in diagrams.items():
        html_file = f"docs/diagrams/{name}.html"
        png_file = f"docs/diagrams/{name}.png"
        
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_template.replace("__MERMAID_CODE__", code.strip()))
            
        page = browser.new_page(device_scale_factor=2) # 2x resolution for print quality
        page.goto('file:///' + os.path.abspath(html_file).replace('\\', '/'))
        page.wait_for_selector('svg', timeout=10000)
        time.sleep(0.5)
        
        # Take screenshot of the rendered SVG diagram
        svg = page.locator('svg')
        svg.screenshot(path=png_file)
        page.close()
        print(f"Rendered: {png_file}")
        
    browser.close()

print("All 13 diagrams rendered successfully to docs/diagrams/!")
