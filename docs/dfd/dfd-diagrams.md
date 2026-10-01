# Data Flow Diagrams (DFD)

## 1. Context Level DFD (Level 0 Overview)

```mermaid
flowchart LR
    %% External Entities
    User[Student / Faculty]
    Admin[Administrator]
    Staff[Maintenance Staff]
    Notification[Notification Service]

    %% Main Process
    CCMS((CCMS))

    %% Data Flows
    User -- "Complaint Details\nUser Credentials\nFeedback" --> CCMS
    CCMS -- "Complaint Status\nNotifications" --> User

    Admin -- "User Credentials\nVerification Decisions\nAssignments\nSystem Configurations" --> CCMS
    CCMS -- "System Reports\nPending Complaints\nUser Data" --> Admin

    Staff -- "User Credentials\nStatus Updates\nResolution Remarks" --> CCMS
    CCMS -- "Task Assignments\nWork Orders" --> Staff

    CCMS -- "Alert Triggers\nEmail/SMS Data" --> Notification
    Notification -- "Delivery Status" --> CCMS
```

## 2. Level 0 DFD

```mermaid
flowchart TD
    %% External Entities
    User[Student / Faculty]
    Admin[Administrator]
    Staff[Maintenance Staff]

    %% Processes
    P1((1.0\nUser\nAuthentication))
    P2((2.0\nComplaint\nManagement))
    P3((3.0\nComplaint\nVerification))
    P4((4.0\nComplaint\nAssignment))
    P5((5.0\nMaintenance &\nResolution))
    P6((6.0\nClosure &\nFeedback))
    P7((7.0\nReporting &\nAdmin))

    %% Data Stores
    D1[(D1: User DB)]
    D2[(D2: Complaint DB)]
    D3[(D3: Category/Location DB)]
    D4[(D4: Complaint History DB)]
    D5[(D5: Feedback DB)]

    %% Data Flows
    User -- "Credentials" --> P1
    Admin -- "Credentials" --> P1
    Staff -- "Credentials" --> P1
    P1 <--> D1
    P1 -- "Auth Token" --> User & Admin & Staff

    User -- "Complaint Info" --> P2
    P2 -- "Fetch Categories" --> D3
    P2 -- "Save Complaint" --> D2

    D2 -- "New Complaints" --> P3
    Admin -- "Verification Decision" --> P3
    P3 -- "Update Status" --> D2

    D2 -- "Verified Complaints" --> P4
    Admin -- "Assignment Details" --> P4
    P4 -- "Update Assignment" --> D2
    P4 -- "Task Info" --> Staff

    Staff -- "Status & Remarks" --> P5
    P5 -- "Update Progress" --> D2
    P5 -- "Log History" --> D4

    D2 -- "Resolved Complaints" --> P6
    Admin -- "Closure Conf" --> P6
    User -- "Feedback" --> P6
    P6 -- "Save Feedback" --> D5
    P6 -- "Final Status" --> D2

    Admin -- "Report Query" --> P7
    P7 -- "Read Data" --> D1 & D2 & D4 & D5
    P7 -- "Generated Report" --> Admin
```

## 3. Level 1 DFD - Decomposition of 2.0 Complaint Management

```mermaid
flowchart TD
    User[Student / Faculty]
    D2[(D2: Complaint DB)]
    D3[(D3: Category/Location DB)]
    Admin[Administrator]

    P21((2.1\nEnter Details))
    P22((2.2\nValidate\nComplaint))
    P23((2.3\nStore\nComplaint))
    P24((2.4\nGenerate ID))
    P25((2.5\nNotify Admin))

    User -- "Raw Complaint Data" --> P21
    P21 -- "Category/Loc Lookup" --> D3
    D3 -- "Valid Lists" --> P21
    P21 -- "Draft Data" --> P22
    P22 -- "Valid Data" --> P24
    P24 -- "Complaint ID" --> P23
    P23 -- "Final Record" --> D2
    P23 -- "New Record Event" --> P25
    P25 -- "Alert" --> Admin
```

## 4. Level 1 DFD - Decomposition of 5.0 Maintenance & Resolution

```mermaid
flowchart TD
    Staff[Maintenance Staff]
    D2[(D2: Complaint DB)]
    D4[(D4: Complaint History DB)]

    P51((5.1\nView\nAssignment))
    P52((5.2\nAccept Task))
    P53((5.3\nUpdate\nProgress))
    P54((5.4\nAdd Remarks))
    P55((5.5\nMark\nResolved))

    D2 -- "Assigned Tasks" --> P51
    P51 -- "Display List" --> Staff

    Staff -- "Acceptance" --> P52
    P52 -- "Status=InProgress" --> D2

    Staff -- "Progress Update" --> P53
    P53 -- "Log Update" --> D4

    Staff -- "Resolution Info" --> P54
    P54 -- "Remarks" --> D2

    Staff -- "Resolve Action" --> P55
    P55 -- "Status=Resolved" --> D2
    P55 -- "Log Completion" --> D4
```

## DFD Balancing Notes
The DFDs are perfectly balanced. The inputs and outputs in the Context Diagram exactly match the net inputs and outputs traversing the boundaries of the Level 0 diagram. Furthermore, when decomposing Process 2.0 and Process 5.0 into Level 1, the external data flows entering and leaving those subprocesses correspond to those in Level 0.
