# Test Cases
**Project:** Campus Complaint & Maintenance Management System (CCMS)
**Course Code:** 23CS4219

## Authentication Tests

| Field | Value |
|---|---|
| TC ID | TC-001 |
| Requirement | FR-01 |
| Test Scenario | Valid user registration |
| Preconditions | User not registered |
| Test Data | name: John Doe, email: john@test.com, password: Test@123, role: STUDENT |
| Steps | 1. Navigate to /register <br> 2. Fill form <br> 3. Click Register |
| Expected Result | User created, redirected to login |
| Actual Result | PASS |
| Status | PASS |

| Field | Value |
|---|---|
| TC ID | TC-002 |
| Requirement | FR-01 |
| Test Scenario | Duplicate email registration |
| Preconditions | User already registered with email |
| Test Data | email: existing@test.com |
| Steps | 1. Navigate to /register <br> 2. Fill form with existing email <br> 3. Click Register |
| Expected Result | Error message: Email already exists |
| Actual Result | PASS |
| Status | PASS |

| Field | Value |
|---|---|
| TC ID | TC-003 |
| Requirement | FR-02 |
| Test Scenario | Valid login |
| Preconditions | User is registered |
| Test Data | email: valid@test.com, password: Valid@123 |
| Steps | 1. Navigate to /login <br> 2. Enter credentials <br> 3. Click Login |
| Expected Result | Successful login, redirected to dashboard |
| Actual Result | PASS |
| Status | PASS |

| Field | Value |
|---|---|
| TC ID | TC-004 |
| Requirement | FR-02 |
| Test Scenario | Invalid password login |
| Preconditions | User is registered |
| Test Data | email: valid@test.com, password: WrongPassword |
| Steps | 1. Navigate to /login <br> 2. Enter credentials <br> 3. Click Login |
| Expected Result | Error message: Invalid credentials |
| Actual Result | PASS |
| Status | PASS |

| Field | Value |
|---|---|
| TC ID | TC-005 |
| Requirement | FR-02 |
| Test Scenario | Empty fields login |
| Preconditions | None |
| Test Data | email: (empty), password: (empty) |
| Steps | 1. Navigate to /login <br> 2. Leave fields empty <br> 3. Click Login |
| Expected Result | Validation error: Fields cannot be empty |
| Actual Result | PASS |
| Status | PASS |

| Field | Value |
|---|---|
| TC ID | TC-006 |
| Requirement | SR-01 |
| Test Scenario | Unauthorized API access without token |
| Preconditions | User not logged in |
| Test Data | None |
| Steps | 1. Send GET request to /api/complaints without Authorization header |
| Expected Result | 401 Unauthorized response |
| Actual Result | PASS |
| Status | PASS |

| Field | Value |
|---|---|
| TC ID | TC-007 |
| Requirement | SR-02 |
| Test Scenario | Role-based access control |
| Preconditions | Logged in as STUDENT |
| Test Data | None |
| Steps | 1. Send GET request to /api/admin/dashboard |
| Expected Result | 403 Forbidden response |
| Actual Result | PASS |
| Status | PASS |

## Complaint Submission Tests

| Field | Value |
|---|---|
| TC ID | TC-008 |
| Requirement | FR-03 |
| Test Scenario | Valid complaint submission |
| Preconditions | Logged in as STUDENT |
| Test Data | title: Broken Chair, desc: Chair in Room 101, category: FURNITURE, location: Room 101 |
| Steps | 1. Navigate to Submit Complaint <br> 2. Fill form <br> 3. Submit |
| Expected Result | Complaint created with PENDING status |
| Actual Result | PASS |
| Status | PASS |

| Field | Value |
|---|---|
| TC ID | TC-009 |
| Requirement | FR-03 |
| Test Scenario | Missing title |
| Preconditions | Logged in as STUDENT |
| Test Data | title: (empty) |
| Steps | 1. Fill form leaving title empty <br> 2. Submit |
| Expected Result | Validation error: Title required |
| Actual Result | PASS |
| Status | PASS |

| Field | Value |
|---|---|
| TC ID | TC-010 |
| Requirement | FR-03 |
| Test Scenario | Missing description |
| Preconditions | Logged in as STUDENT |
| Test Data | desc: (empty) |
| Steps | 1. Fill form leaving description empty <br> 2. Submit |
| Expected Result | Validation error: Description required |
| Actual Result | PASS |
| Status | PASS |

| Field | Value |
|---|---|
| TC ID | TC-011 |
| Requirement | FR-03 |
| Test Scenario | Missing category |
| Preconditions | Logged in as STUDENT |
| Test Data | category: (empty) |
| Steps | 1. Fill form leaving category empty <br> 2. Submit |
| Expected Result | Validation error: Category required |
| Actual Result | PASS |
| Status | PASS |

| Field | Value |
|---|---|
| TC ID | TC-012 |
| Requirement | FR-03 |
| Test Scenario | Missing location |
| Preconditions | Logged in as STUDENT |
| Test Data | location: (empty) |
| Steps | 1. Fill form leaving location empty <br> 2. Submit |
| Expected Result | Validation error: Location required |
| Actual Result | PASS |
| Status | PASS |

| Field | Value |
|---|---|
| TC ID | TC-013 |
| Requirement | FR-04 |
| Test Scenario | Complaint with image upload |
| Preconditions | Logged in as STUDENT |
| Test Data | Valid form data + valid image file |
| Steps | 1. Fill form <br> 2. Attach image <br> 3. Submit |
| Expected Result | Complaint created with image URL attached |
| Actual Result | PASS |
| Status | PASS |

## Complaint Tracking Tests

| Field | Value |
|---|---|
| TC ID | TC-014 |
| Requirement | FR-05 |
| Test Scenario | Student views own complaints |
| Preconditions | Logged in as STUDENT |
| Test Data | None |
| Steps | 1. Navigate to My Complaints |
| Expected Result | List of complaints submitted by the student |
| Actual Result | PASS |
| Status | PASS |

| Field | Value |
|---|---|
| TC ID | TC-015 |
| Requirement | FR-06 |
| Test Scenario | Student views complaint detail |
| Preconditions | Logged in as STUDENT, has existing complaint |
| Test Data | complaint_id |
| Steps | 1. Click on a complaint from the list |
| Expected Result | Complaint details page displayed |
| Actual Result | PASS |
| Status | PASS |

| Field | Value |
|---|---|
| TC ID | TC-016 |
| Requirement | SR-02 |
| Test Scenario | Student cannot view other student's complaints |
| Preconditions | Logged in as STUDENT A |
| Test Data | complaint_id of STUDENT B |
| Steps | 1. Access /api/complaints/{complaint_id} directly |
| Expected Result | 403 Forbidden response |
| Actual Result | PASS |
| Status | PASS |

## Admin Verification Tests

| Field | Value |
|---|---|
| TC ID | TC-017 |
| Requirement | FR-07 |
| Test Scenario | Admin verifies complaint |
| Preconditions | Logged in as ADMIN, PENDING complaint exists |
| Test Data | complaint_id |
| Steps | 1. Open PENDING complaint <br> 2. Click Verify |
| Expected Result | Status changed to VERIFIED |
| Actual Result | PASS |
| Status | PASS |

| Field | Value |
|---|---|
| TC ID | TC-018 |
| Requirement | FR-08 |
| Test Scenario | Admin rejects complaint |
| Preconditions | Logged in as ADMIN, PENDING complaint exists |
| Test Data | complaint_id, rejection reason |
| Steps | 1. Open PENDING complaint <br> 2. Click Reject <br> 3. Provide reason |
| Expected Result | Status changed to REJECTED |
| Actual Result | PASS |
| Status | PASS |

| Field | Value |
|---|---|
| TC ID | TC-019 |
| Requirement | SR-02 |
| Test Scenario | Non-admin cannot verify complaint |
| Preconditions | Logged in as STUDENT |
| Test Data | complaint_id |
| Steps | 1. Attempt to send verify API request |
| Expected Result | 403 Forbidden response |
| Actual Result | PASS |
| Status | PASS |

## Assignment Tests

| Field | Value |
|---|---|
| TC ID | TC-020 |
| Requirement | FR-09 |
| Test Scenario | Admin assigns complaint to maintenance staff |
| Preconditions | Logged in as ADMIN, VERIFIED complaint exists |
| Test Data | staff_id |
| Steps | 1. Select complaint <br> 2. Select staff <br> 3. Assign |
| Expected Result | Complaint status ASSIGNED, staff_id updated |
| Actual Result | PASS |
| Status | PASS |

| Field | Value |
|---|---|
| TC ID | TC-021 |
| Requirement | FR-09 |
| Test Scenario | Invalid staff assignment (wrong role) |
| Preconditions | Logged in as ADMIN |
| Test Data | staff_id of a STUDENT |
| Steps | 1. Attempt to assign complaint to student ID |
| Expected Result | Error: Invalid staff selected |
| Actual Result | PASS |
| Status | PASS |

| Field | Value |
|---|---|
| TC ID | TC-022 |
| Requirement | SR-02 |
| Test Scenario | Unauthorized assignment attempt |
| Preconditions | Logged in as STAFF |
| Test Data | staff_id, complaint_id |
| Steps | 1. Attempt to send assignment API request |
| Expected Result | 403 Forbidden response |
| Actual Result | PASS |
| Status | PASS |

## Status Update Tests

| Field | Value |
|---|---|
| TC ID | TC-023 |
| Requirement | FR-10 |
| Test Scenario | Maintenance staff updates to IN_PROGRESS |
| Preconditions | Logged in as STAFF, ASSIGNED complaint exists |
| Test Data | complaint_id |
| Steps | 1. View assigned complaint <br> 2. Update status to IN_PROGRESS |
| Expected Result | Status updated to IN_PROGRESS |
| Actual Result | PASS |
| Status | PASS |

| Field | Value |
|---|---|
| TC ID | TC-024 |
| Requirement | FR-11 |
| Test Scenario | Invalid state transition (NEW to CLOSED) |
| Preconditions | Logged in as STAFF |
| Test Data | complaint_id of NEW complaint |
| Steps | 1. Attempt to update status to CLOSED |
| Expected Result | Error: Invalid state transition |
| Actual Result | PASS |
| Status | PASS |

| Field | Value |
|---|---|
| TC ID | TC-025 |
| Requirement | FR-12 |
| Test Scenario | Maintenance marks resolved with remarks |
| Preconditions | Logged in as STAFF |
| Test Data | remarks: "Fixed wiring" |
| Steps | 1. Change status to RESOLVED <br> 2. Enter remarks |
| Expected Result | Status RESOLVED, remarks saved |
| Actual Result | PASS |
| Status | PASS |

| Field | Value |
|---|---|
| TC ID | TC-026 |
| Requirement | FR-13 |
| Test Scenario | Admin closes resolved complaint |
| Preconditions | Logged in as ADMIN |
| Test Data | complaint_id of RESOLVED complaint |
| Steps | 1. Review complaint <br> 2. Update status to CLOSED |
| Expected Result | Status updated to CLOSED |
| Actual Result | PASS |
| Status | PASS |

## Feedback Tests

| Field | Value |
|---|---|
| TC ID | TC-027 |
| Requirement | FR-14 |
| Test Scenario | Student provides feedback after resolution |
| Preconditions | Logged in as STUDENT |
| Test Data | rating: 5, comment: "Good job" |
| Steps | 1. View CLOSED complaint <br> 2. Submit feedback |
| Expected Result | Feedback saved successfully |
| Actual Result | PASS |
| Status | PASS |

| Field | Value |
|---|---|
| TC ID | TC-028 |
| Requirement | FR-14 |
| Test Scenario | Duplicate feedback submission |
| Preconditions | Logged in as STUDENT, feedback already submitted |
| Test Data | rating: 4 |
| Steps | 1. Attempt to submit feedback again |
| Expected Result | Error: Feedback already exists |
| Actual Result | PASS |
| Status | PASS |

## Security Tests

| Field | Value |
|---|---|
| TC ID | TC-029 |
| Requirement | SR-03 |
| Test Scenario | SQL injection attempt |
| Preconditions | Logged in as STUDENT |
| Test Data | desc: "'; DROP TABLE users; --" |
| Steps | 1. Submit complaint with SQL injection payload |
| Expected Result | Input sanitized, no database error |
| Actual Result | PASS |
| Status | PASS |

| Field | Value |
|---|---|
| TC ID | TC-030 |
| Requirement | SR-04 |
| Test Scenario | XSS attempt in complaint description |
| Preconditions | Logged in as STUDENT |
| Test Data | desc: "<script>alert('XSS')</script>" |
| Steps | 1. Submit complaint with XSS payload <br> 2. View complaint |
| Expected Result | Script tags encoded/removed, script not executed |
| Actual Result | PASS |
| Status | PASS |
