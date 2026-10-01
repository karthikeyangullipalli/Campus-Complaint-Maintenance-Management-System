# Experiment No: 12
## Title: Project Presentation

**Course Code:** 23CS4219 | **Course:** Software Engineering Lab

---

### Slide 1: Title Slide
**Campus Complaint & Maintenance Management System (CCMS)**
Course: Software Engineering Lab | Code: 23CS4219
B.Tech CSE | Academic Year: 2024-25

---

### Slide 2: Problem Statement
- Manual, paper-based complaint registers.
- High risk of data loss and delayed responses.
- Lack of transparency in the resolution process.
- No central dashboard for administrative oversight.

---

### Slide 3: Objectives
- To digitize and streamline the complaint submission process.
- To provide real-time tracking of maintenance issues.
- To improve accountability among maintenance staff.
- To generate actionable analytics for administration.

---

### Slide 4: Existing vs Proposed System
| Feature | Existing System | Proposed System (CCMS) |
|---------|-----------------|------------------------|
| Submission | Paper Registers | 24/7 Web Portal |
| Tracking | Verbal inquiries | Real-time Dashboard |
| Assignment | Manual/Ad-hoc | Automated/Systematic |
| Reports | Difficult | Auto-generated |

---

### Slide 5: System Architecture
- **Presentation Layer:** React.js / HTML5 UI.
- **Application Layer:** Node.js REST API handling business logic.
- **Data Layer:** Relational Database (MySQL).
- **Deployment:** Cloud hosting with centralized DB.

---

### Slide 6: Use Case Diagram
**Key Actors:** Student, Admin, Maintenance Staff.
**Core Use Cases:** Submit Complaint, Track Status, Assign Task, Update Status, Generate Reports.

---

### Slide 7: Data Flow Diagrams
- **Context Diagram:** Highlights interactions between users and the core system.
- **Level 0 DFD:** Breaks down into Manage Complaints, Assign Tasks, and Process Resolution.

---

### Slide 8: Class & Sequence Diagrams
- **Classes:** User, Complaint, Assignment.
- **Interactions:** Demonstrates the systematic passing of data from UI to Controller to Database during complaint submission.

---

### Slide 9: State & Activity Diagrams
- **Lifecycle states:** Submitted -> Assigned -> In Progress -> Resolved -> Closed.
- **Workflow:** Clear swimlanes depicting responsibilities passing from Student to Admin to Staff.

---

### Slide 10: Testing Strategy & Results
- Conducted Unit, Integration, and System testing.
- Over 95% of test cases passed in final build.
- Key modules (Auth, Submission, Assignment) verified.

---

### Slide 11: Features & Screenshots
*(Placeholder for actual application screenshots)*
- User Dashboard
- Admin Analytics Panel
- Mobile-responsive forms

---

### Slide 12: Conclusion & Future Scope
- **Conclusion:** CCMS successfully replaces an inefficient legacy system, bringing transparency and speed to campus maintenance.
- **Future Scope:** Mobile app deployment, AI auto-assignment, and predictive maintenance tracking.
