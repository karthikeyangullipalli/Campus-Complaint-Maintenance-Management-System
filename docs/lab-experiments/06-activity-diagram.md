# Experiment No: 6
## Title: Activity Diagram for CCMS

**Course Code:** 23CS4219 | **Course:** Software Engineering Lab

### 1. Aim
To model the complete workflow of a complaint in the Campus Complaint & Maintenance Management System (CCMS).

### 2. Objective
Show the flow of activities, decision points, and concurrency from complaint submission to closure using swimlanes.

### 3. Theory
An Activity Diagram represents the workflow of stepwise activities and actions, with support for choice, iteration, and concurrency. 
- **Swimlanes:** Partition the diagram into responsibilities of different actors.
- **Action Nodes:** Represent executable steps.
- **Decision Nodes:** Represent branching based on conditions (Diamond shape).
- **Fork/Join:** Represent concurrent execution of threads.

### 4. Procedure
1. Identify actors involved in the workflow (Student, Admin, Maintenance Staff).
2. Trace the step-by-step process of handling a complaint.
3. Identify decision points (e.g., Is staff available? Is issue fixed?).
4. Draw the diagram using swimlanes.

### 5. Diagram

```mermaid
flowchart TD
    subgraph Student
        Start((Start)) --> A1[Submit Complaint]
        A6[Review Resolution] --> D2{Is Satisfied?}
        D2 -->|Yes| A7[Close Complaint]
        D2 -->|No| A8[Reject & Reopen]
        A7 --> End((End))
    end

    subgraph Admin
        A1 --> A2[Review Complaint]
        A2 --> D1{Requires Action?}
        D1 -->|No| A9[Reject Complaint]
        A9 --> End
        D1 -->|Yes| A3[Assign to Staff]
    end

    subgraph Maintenance Staff
        A3 --> A4[Receive Assignment]
        A4 --> A5[Perform Work & Update Status]
        A5 --> A6
        A8 --> A5
    end
```

### 6. Result
The Activity Diagram successfully models the step-by-step workflow of the complaint resolution process across different actor swimlanes.
