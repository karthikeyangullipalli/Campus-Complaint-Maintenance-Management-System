# Communication Diagram

## Complaint Submission & Assignment

```mermaid
flowchart TD
    Student((Student))
    Browser[1: BrowserUI]
    API[2: ComplaintController]
    DB[(3: MySQL Database)]
    Admin((Administrator))
    AssignAPI[4: AssignmentController]
    Staff((Maintenance Staff))

    Student -- "1. entersDetails()" --> Browser
    Browser -- "2. submitComplaint(data)" --> API
    API -- "3. validateAndSave(data)" --> DB
    DB -- "4. returnComplaintId()" --> API
    API -- "5. notifyNewComplaint()" --> Admin
    
    Admin -- "6. viewComplaints()" --> Browser
    Admin -- "7. assignStaff(complaintId, staffId)" --> AssignAPI
    AssignAPI -- "8. updateStatus(Assigned)" --> DB
    DB -- "9. confirmUpdate()" --> AssignAPI
    AssignAPI -- "10. notifyAssignment()" --> Staff
```

**Description:**
This communication diagram (rendered as a directed graph) illustrates the collaboration between objects during the core workflow of a student submitting a complaint, which is then verified and assigned by the administrator to a maintenance staff member. Messages are numbered in the order of execution.
