# Experiment No: 11
## Title: Complete Case Study - Campus Complaint & Maintenance Management System

**Course Code:** 23CS4219 | **Course:** Software Engineering Lab

### 1. Executive Summary
The Campus Complaint & Maintenance Management System (CCMS) is an integrated web-based platform designed to streamline the reporting, tracking, and resolution of infrastructural and maintenance issues within a university campus. It replaces traditional paper-based methods with a centralized digital solution.

### 2. Problem Statement
Universities frequently struggle with facility management. The existing manual system relies on paper registers or scattered emails, leading to:
- Loss of complaint records.
- Inability to track complaint status.
- Lack of accountability for maintenance staff.
- Difficulty in generating analytical reports for administration.

### 3. Objectives
- Provide a 24/7 accessible portal for students and staff to lodge complaints.
- Enable real-time status tracking for end-users.
- Automate task assignment to relevant maintenance departments.
- Facilitate performance monitoring and report generation for administration.

### 4. Scope and Limitations
**Scope:** Covers electrical, plumbing, IT, and general infrastructure complaints within campus premises.
**Limitations:** Does not handle emergency security threats or financial accounting for maintenance materials.

### 5. System Actors
- **Student/Faculty:** Can register, submit complaints, and view status.
- **Admin:** Manages user accounts, assigns tasks, and views analytical reports.
- **Maintenance Staff:** Views assigned tasks and updates their resolution status.

### 6. Functional Requirements
- **FR1:** The system shall allow users to securely log in.
- **FR2:** Users shall be able to submit complaints with images.
- **FR3:** Admins shall be able to assign complaints to staff.
- **FR4:** Staff shall be able to mark complaints as 'Resolved'.

### 7. Non-Functional Requirements
- **NFR1 (Performance):** System should load within 3 seconds.
- **NFR2 (Security):** Passwords must be encrypted (e.g., bcrypt).
- **NFR3 (Availability):** 99.9% uptime.

### 8. System Architecture
The system follows a standard 3-tier MVC (Model-View-Controller) architecture, separating presentation, business logic, and data storage.

### 9. Technology Stack
- **Frontend:** HTML, CSS, JavaScript (React/Bootstrap).
- **Backend:** Node.js/Express or Python/Django.
- **Database:** MySQL/PostgreSQL.

### 10. Database Design
**Entities:**
- Users (id, name, email, role, password_hash)
- Complaints (id, user_id, category, description, status, created_at)
- Assignments (id, complaint_id, staff_id, assigned_at)

### 11. UML Diagrams Summary
Extensive UML modeling was conducted including Use Case, Class, Sequence, and State Diagrams to ensure robust system design. (Refer to Ex 2-7).

### 12. DFD Summary
Context diagram established the boundaries. Level-0 and Level-1 DFDs mapped the flow of data between users, processes (manage, assign, resolve), and databases.

### 13. Testing Strategy
- **Unit Testing:** Validating individual backend controllers.
- **Integration Testing:** Ensuring UI communicates correctly with the API.
- **System Testing:** End-to-end workflow validation.

### 14. Test Case Summary Table
| TC ID | Scenario | Expected Result | Status |
|-------|----------|-----------------|--------|
| TC01  | Valid Login | Redirect to Dashboard | Pass |
| TC02  | Submit Empty Complaint | Show error msg | Pass |
| TC03  | Update Status | Status reflects in DB | Pass |

### 15. Challenges and Solutions
**Challenge:** Ensuring prompt staff response.
**Solution:** Implemented SMS/Email notification alerts upon task assignment.

### 16. Future Enhancements
- Integration with mobile applications.
- AI-based automatic categorization of complaints.

### 17. Conclusion
CCMS effectively digitizes campus maintenance, reducing resolution time and improving overall campus administrative efficiency.
