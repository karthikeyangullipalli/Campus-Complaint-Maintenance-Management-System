# Experiment No: 4
## Title: Interaction Diagrams for CCMS

**Course Code:** 23CS4219 | **Course:** Software Engineering Lab

### 1. Aim
To model dynamic interactions within the Campus Complaint & Maintenance Management System (CCMS).

### 2. Objective
Show object interactions for key scenarios using Sequence and Collaboration (Communication) diagrams.

### 3. Theory
Interaction diagrams model the dynamic behavior of a system.
- **Sequence Diagram:** Shows how objects interact in a particular time sequence. It includes lifelines, activation bars, and messages.
- **Collaboration Diagram:** Shows interactions organized around the objects and their links to one another, numbering messages to show sequence.

### 4. Procedure
1. Select a key use case (e.g., Submit Complaint, Assign Complaint).
2. Identify participating objects/lifelines.
3. Determine the sequence of messages passed.
4. Draw sequence and collaboration diagrams.

### 5. Diagrams

#### Sequence Diagram: Submit Complaint
```mermaid
sequenceDiagram
    actor Student
    participant UI as System Interface
    participant Ctrl as ComplaintController
    participant DB as Database

    Student->>UI: Enter complaint details
    UI->>Ctrl: submitComplaint(details)
    Ctrl->>DB: save(complaint)
    DB-->>Ctrl: confirmation (complaintId)
    Ctrl-->>UI: displaySuccessMessage()
    UI-->>Student: Show Success & ID
```

#### Sequence Diagram: Assign Complaint
```mermaid
sequenceDiagram
    actor Admin
    participant UI as Admin Dashboard
    participant Ctrl as AssignmentController
    participant DB as Database
    participant Notif as NotificationSystem

    Admin->>UI: Select open complaint & staff
    UI->>Ctrl: assign(complaintId, staffId)
    Ctrl->>DB: updateComplaintStatus('Assigned')
    Ctrl->>DB: createAssignmentRecord()
    Ctrl->>Notif: sendAlert(staffId)
    Notif-->>Ctrl: alertSent
    Ctrl-->>UI: displayAssignmentSuccess()
    UI-->>Admin: Show Success
```

#### Communication Diagram: Complaint Submission (Logical Flow)
```mermaid
flowchart LR
    S((Student)) -- "1: enterDetails()" --> U[System UI]
    U -- "2: submit(details)" --> C[Controller]
    C -- "3: saveRecord()" --> D[(Database)]
    D -. "4: returnID" .-> C
    C -. "5: showSuccess" .-> U
```

### 6. Result
Dynamic interactions for key CCMS functionalities were successfully modeled using Sequence and Collaboration diagrams.
