# Testing Strategy
**Project:** Campus Complaint & Maintenance Management System (CCMS)
**Course Code:** 23CS4219

## 1. Testing Objectives
The primary objective is to verify that the CCMS application satisfies all specified functional and non-functional requirements. This includes ensuring data integrity, checking role-based access controls, validating system workflows (from complaint creation to resolution), and guaranteeing a seamless user experience.

## 2. Testing Scope
**In Scope:**
- User Authentication & Authorization (Student, Staff, Admin)
- Complaint Management Module (Creation, Tracking, Updating)
- Maintenance Assignment Module
- Admin Dashboard and Reporting
- Basic Security (Input Validation, XSS/SQLi prevention)

**Out of Scope:**
- Stress and Load testing of the production server
- Hardware-specific testing
- Third-party payment gateway integrations (not applicable)

## 3. Testing Levels
- **Unit Testing:** Validating individual functions and components (e.g., password hashing, date formatting).
- **Integration Testing:** Ensuring modules work together (e.g., linking a complaint to a specific maintenance staff).
- **System Testing:** End-to-end testing of the fully integrated CCMS application.
- **Acceptance Testing:** Validating the system against business requirements from the end-user perspective.

## 4. Testing Types
- **Functional Testing:** Validating features against the SRS.
- **Performance Testing:** Ensuring API response times are under acceptable thresholds (< 2s).
- **Security Testing:** Verifying JWT implementation, role checks, and input sanitization.
- **Usability Testing:** Ensuring the UI is intuitive and responsive on desktop and mobile.
- **Regression Testing:** Re-testing application after bug fixes to ensure existing features remain unaffected.

## 5. Test Environment
- **OS:** Windows 10/11, Ubuntu 22.04
- **Browser:** Google Chrome (latest), Mozilla Firefox (latest)
- **Node Version:** Node.js v18.x
- **Database:** MySQL 8.0

## 6. Entry Criteria / Exit Criteria
**Entry Criteria:**
- Code implementation is complete for the module.
- Unit tests run successfully.
- Test environment is set up and database is seeded.

**Exit Criteria:**
- 100% of planned test cases executed.
- No Critical or High severity defects remain open.
- All functional requirements validated.

## 7. Test Data Requirements
- Pre-registered Student, Staff, and Admin accounts.
- Sample complaints with varying statuses (New, Verified, Assigned, In Progress, Resolved).
- Sample image files for upload testing.

## 8. Risk-Based Testing
Higher priority is given to:
- Authentication and Role-based access control (High Risk).
- State transitions of complaints (High Risk).
- File upload handling (Medium Risk).

## 9. Defect Management Process
1. Tester logs defect in the tracking system (ID, Description, Steps to Reproduce, Severity).
2. Developer fixes defect and marks as "Resolved".
3. Tester re-tests; if fixed, status is "Closed", otherwise "Reopened".

## 10. Boundary Value Analysis Examples for CCMS
- **Password Length (Min 8, Max 20):**
  - Test values: 7 (Invalid), 8 (Valid), 9 (Valid), 19 (Valid), 20 (Valid), 21 (Invalid).
- **Complaint Description (Min 10, Max 500 chars):**
  - Test values: 9 (Invalid), 10 (Valid), 500 (Valid), 501 (Invalid).

## 11. Equivalence Partitioning Examples for CCMS
- **Role Assignment:**
  - Valid Partitions: "STUDENT", "ADMIN", "STAFF"
  - Invalid Partitions: "GUEST", "SUPER_ADMIN", empty string, numbers.
- **File Upload Size (Max 5MB):**
  - Valid Partition: File size <= 5MB
  - Invalid Partition: File size > 5MB

## 12. Acceptance Criteria
- A student can successfully log a complaint and track its status.
- An admin can assign complaints to staff and view statistics.
- A staff member can update the status of assigned complaints.
- The system prevents unauthorized access to admin/staff endpoints.
