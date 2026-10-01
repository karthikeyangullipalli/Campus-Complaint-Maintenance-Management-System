# Software Requirements Specification (SRS)
## Campus Complaint & Maintenance Management System (CCMS)
**Course Code**: 23CS4219

### 1. Introduction

#### 1.1 Purpose
The purpose of this Software Requirements Specification (SRS) document is to provide a detailed overview of the software requirements for the Campus Complaint & Maintenance Management System (CCMS). This document describes the project's target audience, its user interface, hardware and software requirements, system features, and non-functional requirements. It serves as a foundational guide for the development, testing, and deployment phases.

#### 1.2 Scope
The CCMS is a web-based campus complaint management system designed to replace the existing manual, paper-based process. The scope includes allowing students and faculty to submit, track, and provide feedback on maintenance complaints within the campus. It also provides tools for the administration to verify, assign, and manage complaints, and for maintenance staff to accept and update tasks. The system aims to streamline the workflow, ensure accountability, and provide a clear audit trail.

#### 1.3 Definitions, Acronyms and Abbreviations
- **CCMS**: Campus Complaint & Maintenance Management System
- **SRS**: Software Requirements Specification
- **UI**: User Interface
- **RBAC**: Role-Based Access Control
- **JWT**: JSON Web Token
- **DB**: Database
- **API**: Application Programming Interface

#### 1.4 References
- IEEE Std 830-1998, IEEE Recommended Practice for Software Requirements Specifications.
- Software Engineering principles and practices course materials (23CS4219).

#### 1.5 Overview
This document is organized into several sections. Section 2 provides a general description of the system, its perspective, and user characteristics. Section 3 details the specific functional requirements. Section 4 outlines the non-functional requirements such as performance and security. Section 5 describes external interfaces. Subsequent sections cover system models, database requirements, constraints, and future enhancements.

---

### 2. Overall Description

#### 2.1 Product Perspective
CCMS is a new, self-contained web-based application designed to replace the legacy manual complaint logging system on campus. It operates independently but may interface with existing user authentication systems if integrated in the future.

#### 2.2 Product Functions
The primary functions of the CCMS include:
- User registration and authentication
- Role-based access control and dashboarding
- Complaint submission with categorization, location tagging, and image upload
- Complaint tracking and status monitoring
- Administration module for verification, assignment, and management
- Maintenance staff module for task acceptance and progress updates
- Feedback and rating system upon resolution
- Comprehensive reporting and statistics dashboard

#### 2.3 User Classes and Characteristics
- **Student/Faculty**: General users who submit complaints, track their status, and provide feedback. They need an intuitive and simple interface.
- **Maintenance Staff**: Users assigned to resolve complaints. They need clear task details, the ability to update statuses, and add resolution remarks.
- **Administrator**: Users responsible for managing the entire system, verifying complaints, assigning them to staff, managing users, and monitoring overall performance metrics.

#### 2.4 Operating Environment
- **Client Side**: Modern web browsers (Chrome, Firefox, Safari, Edge) on desktop and mobile devices.
- **Server Side**: Node.js runtime environment.
- **Database**: MySQL database server.

#### 2.5 Design and Implementation Constraints
- The system must comply with data privacy regulations regarding user information.
- The user interface must be responsive and accessible across various devices.
- The initial deployment will be limited to standard web browsers without native mobile applications.

#### 2.6 Assumptions and Dependencies
- Users will have access to a device with an internet connection.
- Maintenance staff will have basic digital literacy to use the system.
- The campus network infrastructure is reliable to support the web application.

---

### 3. Functional Requirements

**FR-01: User Registration**
- **Description**: The system shall allow new users (Students, Faculty) to register by providing necessary details (name, email, password, role).
- **Actor**: Student, Faculty
- **Input**: User Details (Name, Email, Password, Department)
- **Output**: Confirmation message, User account creation
- **Priority**: High

**FR-02: User Login**
- **Description**: Registered users shall be able to log in using their credentials (email and password).
- **Actor**: All Users
- **Input**: Email, Password
- **Output**: Authentication token (JWT), Redirection to appropriate dashboard
- **Priority**: High

**FR-03: Role-based Access Control**
- **Description**: The system shall grant access to specific features and dashboards based on the user's role (Admin, Staff, Student, Faculty).
- **Actor**: System
- **Input**: User Role (from JWT)
- **Output**: Access granted or denied to specific modules
- **Priority**: High

**FR-04: Student/Faculty Submit Complaint**
- **Description**: Users shall be able to submit a new maintenance complaint.
- **Actor**: Student, Faculty
- **Input**: Complaint details (Title, Description, Category, Location)
- **Output**: New complaint record created, Complaint ID generated
- **Priority**: High

**FR-05: Complaint Category Selection**
- **Description**: Users must select a category for their complaint (e.g., Electrical, Plumbing, IT).
- **Actor**: Student, Faculty
- **Input**: Category Selection
- **Output**: Category associated with the complaint
- **Priority**: High

**FR-06: Complaint Location Selection**
- **Description**: Users must specify the location of the issue (e.g., Building name, Room number).
- **Actor**: Student, Faculty
- **Input**: Location Details
- **Output**: Location associated with the complaint
- **Priority**: High

**FR-07: Image Upload with Complaint**
- **Description**: Users shall have the option to upload an image providing visual context of the issue.
- **Actor**: Student, Faculty
- **Input**: Image file (JPG, PNG)
- **Output**: Image saved and linked to the complaint
- **Priority**: Medium

**FR-08: View Own Complaints**
- **Description**: Users shall be able to view a list of all complaints they have submitted.
- **Actor**: Student, Faculty
- **Input**: User ID
- **Output**: List of user's complaints
- **Priority**: High

**FR-09: Track Complaint Status**
- **Description**: Users shall be able to see the current status of their complaints (e.g., Pending, Assigned, In Progress, Resolved).
- **Actor**: Student, Faculty
- **Input**: Complaint ID
- **Output**: Current status and history
- **Priority**: High

**FR-10: Admin View All Complaints**
- **Description**: Administrators shall be able to view all complaints submitted in the system.
- **Actor**: Administrator
- **Input**: None/Filters
- **Output**: List of all complaints
- **Priority**: High

**FR-11: Admin Verify Complaint**
- **Description**: Administrators can review and verify a submitted complaint before assignment.
- **Actor**: Administrator
- **Input**: Complaint ID, Verification action
- **Output**: Complaint status updated to "Verified"
- **Priority**: High

**FR-12: Admin Reject Complaint**
- **Description**: Administrators can reject invalid or duplicate complaints, providing a reason.
- **Actor**: Administrator
- **Input**: Complaint ID, Rejection Reason
- **Output**: Complaint status updated to "Rejected", notification to user
- **Priority**: Medium

**FR-13: Admin Assign Complaint to Maintenance Staff**
- **Description**: Administrators shall assign verified complaints to specific maintenance staff members.
- **Actor**: Administrator
- **Input**: Complaint ID, Staff ID
- **Output**: Complaint status updated to "Assigned", Staff notified
- **Priority**: High

**FR-14: Admin Set Priority**
- **Description**: Administrators can set the priority level (Low, Medium, High, Urgent) of a complaint.
- **Actor**: Administrator
- **Input**: Complaint ID, Priority Level
- **Output**: Priority updated
- **Priority**: Medium

**FR-15: Maintenance Staff View Assigned Complaints**
- **Description**: Maintenance staff shall see a list of complaints assigned to them.
- **Actor**: Maintenance Staff
- **Input**: Staff ID
- **Output**: List of assigned tasks
- **Priority**: High

**FR-16: Maintenance Staff Accept Task**
- **Description**: Staff must acknowledge and accept an assigned task.
- **Actor**: Maintenance Staff
- **Input**: Complaint ID
- **Output**: Status updated to "In Progress"
- **Priority**: High

**FR-17: Maintenance Staff Update Status/Progress**
- **Description**: Staff can update the progress of their ongoing tasks.
- **Actor**: Maintenance Staff
- **Input**: Complaint ID, Status update
- **Output**: Status updated
- **Priority**: High

**FR-18: Maintenance Staff Add Resolution Remarks**
- **Description**: Upon fixing the issue, staff must provide details of the resolution.
- **Actor**: Maintenance Staff
- **Input**: Complaint ID, Remarks
- **Output**: Remarks saved
- **Priority**: High

**FR-19: Maintenance Staff Mark Complaint Resolved**
- **Description**: Staff can mark a task as resolved once completed.
- **Actor**: Maintenance Staff
- **Input**: Complaint ID
- **Output**: Status updated to "Resolved"
- **Priority**: High

**FR-20: Admin Close Complaint**
- **Description**: Administrators review resolved complaints and officially close them.
- **Actor**: Administrator
- **Input**: Complaint ID
- **Output**: Status updated to "Closed"
- **Priority**: High

**FR-21: Student/Faculty Provide Feedback**
- **Description**: After a complaint is resolved/closed, the original submitter can rate the service and provide feedback.
- **Actor**: Student, Faculty
- **Input**: Complaint ID, Rating (1-5 stars), Comments
- **Output**: Feedback saved
- **Priority**: Medium

**FR-22: Admin Manage Categories**
- **Description**: Administrators can add, edit, or delete complaint categories.
- **Actor**: Administrator
- **Input**: Category Details
- **Output**: Database updated with category changes
- **Priority**: Medium

**FR-23: Admin Manage Locations**
- **Description**: Administrators can manage predefined locations on campus.
- **Actor**: Administrator
- **Input**: Location Details
- **Output**: Database updated with location changes
- **Priority**: Medium

**FR-24: Admin Manage Users**
- **Description**: Administrators can view, edit, or deactivate user accounts.
- **Actor**: Administrator
- **Input**: User ID, Action
- **Output**: User record updated
- **Priority**: High

**FR-25: Admin Dashboard with Statistics**
- **Description**: The system shall provide a dashboard with metrics (total complaints, pending, resolved, average resolution time).
- **Actor**: Administrator
- **Input**: None
- **Output**: Statistical charts and metrics
- **Priority**: Medium

**FR-26: Complaint Status History/Audit Trail**
- **Description**: The system shall maintain a history log of all status changes for every complaint.
- **Actor**: System
- **Input**: Status change event
- **Output**: Log entry created
- **Priority**: High

**FR-27: Complaint Reopening**
- **Description**: If a user is unsatisfied with the resolution, they can request to reopen the complaint within a specific timeframe.
- **Actor**: Student, Faculty
- **Input**: Complaint ID, Reason
- **Output**: Status updated to "Reopened"
- **Priority**: Low

**FR-28: System Notifications**
- **Description**: The system shall notify users (via in-app or email) regarding significant status changes to their complaints.
- **Actor**: System
- **Input**: Event trigger (e.g., status change)
- **Output**: Notification dispatched
- **Priority**: Medium

---

### 4. Non-Functional Requirements

- **Performance**: The system shall respond to user interactions (page loads, form submissions) in under 2 seconds. It must support at least 100 concurrent users without significant performance degradation.
- **Security**: 
    - User passwords must be securely hashed (e.g., using bcrypt).
    - API endpoints must be protected using JWT authentication.
    - Role-Based Access Control (RBAC) must strictly enforce permissions.
    - All database queries must be parameterized to prevent SQL injection.
- **Usability**: The user interface shall be intuitive, requiring minimal training. The design must be fully responsive, providing an optimal experience on both desktop and mobile screens.
- **Reliability**: The system should target 99% uptime during standard campus operating hours. Data integrity mechanisms must be in place to prevent data corruption.
- **Availability**: The web application should be accessible 24/7.
- **Maintainability**: The codebase must be modular, adhering to best practices (e.g., MVC architecture) and thoroughly documented to facilitate future updates.
- **Scalability**: The architecture must allow for easy vertical or horizontal scaling to accommodate future growth in the user base and data volume.

---

### 5. External Interface Requirements

#### 5.1 User Interfaces
- Clean, modern web interface using frameworks like React or standard HTML/CSS/JS.
- Dashboards tailored to the specific role logged in.
- Clear forms with validation feedback.

#### 5.2 Hardware Interfaces
- The application is software-based and accesses hardware (like cameras for image upload) through standard web browser APIs.

#### 5.3 Software Interfaces
- **Database Server**: Interacts with a MySQL database.
- **Operating System**: Runs on a Linux/Windows server hosting the Node.js application.

#### 5.4 Communication Interfaces
- Uses HTTPS protocol for secure communication between client and server.
- RESTful API design for client-server data exchange (JSON format).

---

### 6. System Models
Various UML diagrams (Use Case, Class, Sequence, Activity, State) and Data Flow Diagrams (DFD) model the system's architecture and flow. (Refer to respective documentation artifacts).

### 7. Database Requirements
The database encompasses entities such as `Users`, `Complaints`, `Categories`, `Locations`, `Assignments`, and `Feedback`. Relationships include One-to-Many (e.g., one user submits many complaints, one category contains many complaints).

### 8. Constraints
- The project must be completed within the academic semester timeframe.
- Open-source technologies must be prioritized to minimize costs.

### 9. Future Enhancements
- Integration with the university's central authentication system (LDAP/SSO).
- Mobile application development (Android/iOS).
- AI-based auto-categorization of complaints.
- SMS notification integration.
