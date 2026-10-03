# Campus Complaint & Maintenance Management System (CCMS)

> **Course:** Software Engineering Lab &nbsp;|&nbsp; **Code:** 23CS4219  
> **Degree:** B.Tech Computer Science & Engineering  
> **Academic Year:** 2024–25  
> **GitHub Repository:** [https://github.com/karthikeyangullipalli/Campus-Complaint-Maintenance-Management-System](https://github.com/karthikeyangullipalli/Campus-Complaint-Maintenance-Management-System)

---

## Problem Statement

Manual complaint handling in educational institutions leads to delayed resolution, lack of accountability, poor tracking, and no data-driven decision making. The **Campus Complaint & Maintenance Management System (CCMS)** is a web-based solution that enables students and faculty to report infrastructure and maintenance issues digitally, with complete lifecycle tracking from submission to closure.

---

## Objectives

- Provide a centralized platform for reporting campus maintenance issues
- Enable role-based access for Students, Faculty, Maintenance Staff, and Administrators
- Implement a structured complaint lifecycle: **NEW → VERIFIED → ASSIGNED → IN_PROGRESS → RESOLVED → CLOSED**
- Offer real-time status tracking and notifications
- Provide administrators with dashboard analytics and reports
- Maintain a complete audit trail of all complaint activities

---

## Features

| Feature | Student/Faculty | Maintenance | Admin |
|---------|:-:|:-:|:-:|
| Register & Login | ✓ | ✓ | ✓ |
| Submit Complaint | ✓ | — | — |
| Upload Complaint Image | ✓ | — | — |
| Track Own Complaints | ✓ | — | — |
| View All Complaints | — | — | ✓ |
| Verify/Reject Complaints | — | — | ✓ |
| Assign to Staff | — | — | ✓ |
| Set Priority | — | — | ✓ |
| View Assigned Tasks | — | ✓ | — |
| Update Progress | — | ✓ | — |
| Mark Resolved | — | ✓ | — |
| Close Complaint | — | — | ✓ |
| Provide Feedback | ✓ | — | — |
| Manage Users | — | — | ✓ |
| Manage Categories | — | — | ✓ |
| Manage Locations | — | — | ✓ |
| View Dashboard | ✓ | ✓ | ✓ |
| Generate Reports | — | — | ✓ |

---

## System Actors

1. **Student** — Registers, submits complaints, tracks status, provides feedback
2. **Faculty** — Same as Student (separate actor for UML clarity)
3. **Maintenance Staff** — Views assigned tasks, updates progress, marks resolved
4. **Administrator** — Full system control: verify, assign, manage, report

---

## Architecture

```
┌─────────────────────────────────────────┐
│           Presentation Layer            │
│     React + Vite + Tailwind CSS         │
├─────────────────────────────────────────┤
│             API Layer                   │
│        Express.js REST API              │
├─────────────────────────────────────────┤
│           Business Logic Layer          │
│    Controllers + Services + Validators  │
├─────────────────────────────────────────┤
│             Data Layer                  │
│           MySQL Database                │
└─────────────────────────────────────────┘
```

---

## Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend Framework | React | 18.x |
| Build Tool | Vite | 5.x |
| CSS Framework | Tailwind CSS | 3.x |
| Routing | React Router | 6.x |
| HTTP Client | Axios | 1.x |
| Backend Framework | Express.js | 4.x |
| Runtime | Node.js | 18+ |
| Database | MySQL | 8.x |
| Authentication | JWT (jsonwebtoken) | — |
| Password Hashing | bcryptjs | — |
| File Upload | Multer | — |
| Validation | express-validator | — |

---

## Database Design

| Table | Purpose |
|-------|---------|
| `users` | All system users with roles |
| `complaint_categories` | Categories (Electrical, Plumbing, etc.) |
| `locations` | Campus locations (Building, Floor, Room) |
| `complaints` | Core complaint records |
| `complaint_assignments` | Maintenance staff assignments |
| `complaint_updates` | Status change audit trail |
| `feedback` | User feedback after resolution |

### Complaint Status State Machine

```
NEW ──► VERIFIED ──► ASSIGNED ──► IN_PROGRESS ──► RESOLVED ──► CLOSED
 │          │                                                      │
 └──► REJECTED ◄──┘                              REOPENED ◄───────┘
                                                     │
                                              ASSIGNED (again)
```

### Priority Levels

| Priority | Examples |
|---------|---------|
| CRITICAL | Electrical danger, major water leakage, safety hazard |
| HIGH | Lab equipment failure, internet outage in lab |
| MEDIUM | Broken furniture, non-critical equipment |
| LOW | Minor cosmetic issues |

---

## UML Diagrams

| Diagram | Location |
|---------|---------|
| Use Case Diagram + Scenarios | [docs/uml/use-case/use-case-diagram.md](docs/uml/use-case/use-case-diagram.md) |
| Class Diagram | [docs/uml/class/class-diagram.md](docs/uml/class/class-diagram.md) |
| Sequence Diagrams (4) | [docs/uml/sequence/sequence-diagrams.md](docs/uml/sequence/sequence-diagrams.md) |
| Communication Diagram | [docs/uml/communication/communication-diagram.md](docs/uml/communication/communication-diagram.md) |
| State Chart | [docs/uml/state/state-diagram.md](docs/uml/state/state-diagram.md) |
| Activity Diagram | [docs/uml/activity/activity-diagram.md](docs/uml/activity/activity-diagram.md) |
| Component Diagram | [docs/uml/component/component-diagram.md](docs/uml/component/component-diagram.md) |
| Deployment Diagram | [docs/uml/deployment/deployment-diagram.md](docs/uml/deployment/deployment-diagram.md) |

## DFD Diagrams

| Level | Location |
|-------|---------|
| Context Level DFD | [docs/dfd/dfd-diagrams.md](docs/dfd/dfd-diagrams.md) |
| Level-0 DFD | [docs/dfd/dfd-diagrams.md](docs/dfd/dfd-diagrams.md) |
| Level-1 DFD | [docs/dfd/dfd-diagrams.md](docs/dfd/dfd-diagrams.md) |

---

## Project Structure

```
campus-complaint-maintenance-system/
│
├── frontend/                    # React + Vite + Tailwind CSS
│   ├── src/
│   │   ├── components/common/   # Reusable UI components
│   │   ├── context/             # Auth context
│   │   ├── layouts/             # Role-based layouts
│   │   ├── pages/               # Page components
│   │   │   ├── auth/            # Login, Register
│   │   │   ├── student/         # Student pages
│   │   │   ├── admin/           # Admin pages
│   │   │   └── maintenance/     # Maintenance pages
│   │   ├── utils/               # API client, helpers
│   │   ├── App.jsx              # Router setup
│   │   └── main.jsx             # Entry point
│   ├── package.json
│   └── vite.config.js
│
├── backend/                     # Node.js + Express
│   ├── src/
│   │   ├── controllers/         # Request handlers
│   │   ├── routes/              # API route definitions
│   │   ├── middleware/          # Auth, upload, validate
│   │   ├── config/              # Database config
│   │   ├── utils/               # Helper functions
│   │   └── app.js               # Express app setup
│   ├── uploads/                 # Uploaded images
│   ├── server.js                # Entry point
│   ├── package.json
│   └── .env.example
│
├── database/                    # SQL scripts
│   ├── schema.sql               # Table definitions
│   ├── seed.sql                 # Demo data
│   └── README.md
│
├── docs/                        # All documentation
│   ├── SRS.md                   # Software Requirements Spec
│   ├── requirements-traceability-matrix.md
│   ├── uml/                     # UML diagrams (Mermaid)
│   ├── dfd/                     # DFD diagrams (Mermaid)
│   ├── testing/                 # Test cases, reports
│   └── lab-experiments/         # Experiment 1-12 writeups
│
├── presentation/
│   └── project-presentation.md
│
├── .gitignore
├── README.md
└── LICENSE
```

---

## Installation & Setup

### Prerequisites

- Node.js 18+
- MySQL 8.x
- npm 9+

### 1. Clone the repository

```bash
git clone https://github.com/karthikeyangullipalli/Campus-Complaint-Maintenance-Management-System.git
cd Campus-Complaint-Maintenance-Management-System
```

### 2. Database Setup

Make sure your MySQL 8.x server is running. Then load the schema and initial seed data:

**Command Prompt / Linux / macOS:**
```bash
mysql -u root -p < database/schema.sql
mysql -u root -p ccms_db < database/seed.sql
```

**Windows PowerShell:**
```powershell
Get-Content database/schema.sql | mysql -u root -p
Get-Content database/seed.sql | mysql -u root -p ccms_db
```

**Alternatively inside MySQL CLI:**
```sql
mysql -u root -p
source database/schema.sql;
use ccms_db;
source database/seed.sql;
```

### 3. Backend Setup

```bash
cd backend
npm install
cp .env.example .env
# Edit .env with your local MySQL password and configurations
npm run dev
```

### 4. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### 5. Access the Application

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:5000
- **API Health:** http://localhost:5000/api/health

---

## Environment Variables

Create `backend/.env` from `backend/.env.example`:

```env
PORT=5000
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=ccms_db
JWT_SECRET=your_super_secret_key_change_in_production
JWT_EXPIRES_IN=7d
FRONTEND_URL=http://localhost:5173
UPLOAD_DIR=uploads
```

---

## Demo Credentials

> **Demo Password for all accounts:** `Admin@123`

| Role | Email | Password |
|------|-------|---------|
| Administrator | admin@ccms.local | Admin@123 |
| Student | student@ccms.local | Admin@123 |
| Faculty | faculty@ccms.local | Admin@123 |
| Maintenance Staff | maintenance@ccms.local | Admin@123 |
| Maintenance Staff 2 | maintenance2@ccms.local | Admin@123 |

---

## API Endpoints

### Authentication
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/register` | Register new user | Public |
| POST | `/api/auth/login` | Login | Public |
| GET | `/api/auth/me` | Get current user | JWT |

### Complaints
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/complaints` | List complaints (role-filtered) | JWT |
| POST | `/api/complaints` | Create complaint | JWT |
| GET | `/api/complaints/:id` | Get complaint detail | JWT |
| PUT | `/api/complaints/:id` | Update complaint | JWT |
| DELETE | `/api/complaints/:id` | Delete complaint | Admin |
| POST | `/api/complaints/:id/assign` | Assign to maintenance | Admin |
| PUT | `/api/complaints/:id/status` | Update status | JWT |
| POST | `/api/complaints/:id/feedback` | Submit feedback | JWT |

### Reference Data
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/categories` | List categories |
| GET | `/api/locations` | List locations |
| GET | `/api/users` | List users (Admin) |

### Dashboard
| Method | Endpoint | Role |
|--------|----------|------|
| GET | `/api/dashboard/admin` | Admin |
| GET | `/api/dashboard/student` | Student/Faculty |
| GET | `/api/dashboard/maintenance` | Maintenance |

---

## Testing

### Test Execution Summary

| Category | Total | Pass | Fail |
|---------|-------|------|------|
| Authentication | 7 | 7 | 0 |
| Complaint Submission | 6 | 6 | 0 |
| Complaint Tracking | 3 | 3 | 0 |
| Admin Verification | 3 | 3 | 0 |
| Assignment | 3 | 3 | 0 |
| Status Updates | 4 | 4 | 0 |
| Feedback | 2 | 2 | 0 |
| Security | 2 | 2 | 0 |
| **Total** | **30** | **30** | **0** |

Full test documentation: [docs/testing/](docs/testing/)

---

## Lab Experiments

| Exp | Title | File |
|-----|-------|------|
| 1 | Data Flow Diagrams | [01-dfd.md](docs/lab-experiments/01-dfd.md) |
| 2 | Use Case Diagram | [02-use-case.md](docs/lab-experiments/02-use-case.md) |
| 3 | Class Diagram | [03-class-diagram.md](docs/lab-experiments/03-class-diagram.md) |
| 4 | Sequence & Communication | [04-interaction-diagrams.md](docs/lab-experiments/04-interaction-diagrams.md) |
| 5 | State Chart | [05-state-chart.md](docs/lab-experiments/05-state-chart.md) |
| 6 | Activity Diagram | [06-activity-diagram.md](docs/lab-experiments/06-activity-diagram.md) |
| 7 | Component & Deployment | [07-component-deployment.md](docs/lab-experiments/07-component-deployment.md) |
| 8 | SRS Document | [08-srs.md](docs/lab-experiments/08-srs.md) |
| 9 | Test Cases | [09-test-cases.md](docs/lab-experiments/09-test-cases.md) |
| 10 | Test & Error Report | [10-test-report-error-report.md](docs/lab-experiments/10-test-report-error-report.md) |
| 11 | Complete Case Study | [11-case-study.md](docs/lab-experiments/11-case-study.md) |
| 12 | Presentation | [12-presentation.md](docs/lab-experiments/12-presentation.md) |

---

## Future Enhancements

- Email/SMS notification integration (NodeMailer/Twilio)
- Mobile application (React Native)
- QR code-based complaint submission at campus locations
- SLA-based escalation system
- IoT sensor integration for automatic fault detection
- Advanced analytics and PDF report generation
- Multi-campus support

---

## Security Features

- Password hashing with bcryptjs (10 salt rounds)
- JWT-based stateless authentication
- Role-based access control (RBAC) on every endpoint
- Input validation with express-validator
- Parameterized SQL queries (SQL injection prevention)
- CORS configuration
- Environment variable management (secrets never in code)
- File type and size validation for uploads

---

## Project Information

| Field | Detail |
|-------|--------|
| Project Title | Campus Complaint & Maintenance Management System |
| Short Name | CCMS |
| Course | Software Engineering Lab |
| Course Code | 23CS4219 |
| Degree | B.Tech Computer Science & Engineering |

---

*Built as a complete Software Engineering Lab case study demonstrating:*  
*Requirements Engineering → System Modelling → Design → Implementation → Testing → Documentation*
