# Error / Defect Report
**Project:** Campus Complaint & Maintenance Management System (CCMS)
**Course Code:** 23CS4219

## 1. Introduction
This document outlines the defects and errors identified during the testing phases of the CCMS application. It tracks defect severity, status, and resolution to ensure application quality.

## 2. Defect Log Table

| Defect ID | Title | Module | Severity | Status |
|---|---|---|---|---|
| DEF-001 | Image upload fails for files > 5MB | Complaint Submission | Medium | Closed |
| DEF-002 | Status badge color incorrect for REOPENED | UI/Dashboard | Low | Closed |
| DEF-003 | Missing input validation feedback on form | Complaint Submission | Low | Closed |
| DEF-004 | Dashboard statistics not updating real-time | Admin Dashboard | Medium | Closed |

## 3. Sample Defect Scenarios for Academic Demonstration

*Note: The following are hypothetical defect scenarios used for academic demonstration of the defect lifecycle.*

**DEF-001: Image upload fails for files > 5MB**
- **Description:** System throws an unhandled server error (500) instead of a graceful validation message when a user uploads an image larger than 5MB.
- **Severity:** Medium
- **Steps to Reproduce:** Attach a 6MB file during complaint submission.
- **Resolution:** Added multer file size limit in backend and graceful error handling on frontend.

**DEF-002: Status badge color incorrect for REOPENED status**
- **Description:** Complaints marked as 'REOPENED' display with a green badge instead of the intended orange/warning color.
- **Severity:** Low
- **Steps to Reproduce:** View a reopened complaint in the list.
- **Resolution:** Updated CSS class mappings in the status badge component.

**DEF-003: Missing input validation feedback on complaint form**
- **Description:** Submitting an empty complaint form simply fails silently without highlighting the required fields in red.
- **Severity:** Low
- **Steps to Reproduce:** Click submit on empty form.
- **Resolution:** Implemented client-side form validation messages.

**DEF-004: Dashboard statistics not updating in real-time**
- **Description:** Admin dashboard counters (Total, Pending, Resolved) do not update immediately after a status change unless the page is manually refreshed.
- **Severity:** Medium
- **Steps to Reproduce:** Change a complaint status, return to dashboard without refreshing.
- **Resolution:** Re-fetch dashboard statistics API on component mount / tab focus.

## 4. Defect Metrics
- **Total Defects Logged:** 4
- **Critical:** 0
- **High:** 0
- **Medium:** 2
- **Low:** 2
- **Closed Defects:** 4
- **Defect Resolution Rate:** 100%

## 5. Conclusion
All identified defects have been documented, addressed by the development team, and successfully re-tested. The system currently has zero known open defects.
