# Experiment No: 3
## Title: Class Diagram for CCMS

**Course Code:** 23CS4219 | **Course:** Software Engineering Lab

### 1. Aim
To model the object-oriented structure of the Campus Complaint & Maintenance Management System (CCMS).

### 2. Objective
Identify classes, attributes, methods, and their relationships (association, aggregation, composition, inheritance).

### 3. Theory
A Class Diagram is a static structure diagram that describes the structure of a system by showing its classes, their attributes, operations (or methods), and the relationships among objects.
- **Classes:** Represent entities with common characteristics.
- **Attributes:** Properties of a class.
- **Methods:** Operations a class can perform.
- **Relationships:** Association (general link), Aggregation (weak whole-part), Composition (strong whole-part), Inheritance/Generalization (parent-child).

### 4. Procedure
1. Identify nouns from the problem statement to form classes.
2. Identify attributes for each class.
3. Identify methods/operations.
4. Establish relationships and multiplicity between classes.
5. Draw the class diagram.

### 5. Diagram
```mermaid
classDiagram
    class User {
        +int id
        +String name
        +String email
        +String password_hash
        +String role
        +String department
        +String phone
        +Boolean is_active
        +login() boolean
        +logout() void
    }
    class Student {
        +submitComplaint() void
        +trackStatus() void
        +provideFeedback() void
    }
    class Faculty {
        +submitComplaint() void
        +trackStatus() void
    }
    class Administrator {
        +verifyComplaint() void
        +assignStaff() void
        +generateReport() void
        +manageUsers() void
    }
    class MaintenanceStaff {
        +viewAssignments() void
        +acceptTask() void
        +updateProgress() void
        +markResolved() void
    }
    class Complaint {
        +int id
        +String complaint_number
        +String title
        +String description
        +String priority
        +String status
        +String image_path
        +Timestamp created_at
        +Timestamp resolved_at
        +Timestamp closed_at
        +submit() void
        +updateStatus(newStatus) void
    }
    class ComplaintCategory {
        +int id
        +String name
        +String description
        +Boolean is_active
    }
    class Location {
        +int id
        +String building
        +String floor
        +String room
        +Boolean is_active
        +getDisplayName() String
    }
    class ComplaintAssignment {
        +int id
        +Timestamp assigned_at
        +String notes
    }
    class ComplaintUpdate {
        +int id
        +String old_status
        +String new_status
        +String remarks
        +Timestamp created_at
    }
    class Feedback {
        +int id
        +int rating
        +String comments
        +Timestamp created_at
    }

    User <|-- Student
    User <|-- Faculty
    User <|-- Administrator
    User <|-- MaintenanceStaff

    Student "1" --> "*" Complaint : submits
    Faculty "1" --> "*" Complaint : submits
    Complaint "*" --> "1" ComplaintCategory : categorized by
    Complaint "*" --> "1" Location : located at
    Administrator "1" --> "*" ComplaintAssignment : creates
    ComplaintAssignment "*" --> "1" Complaint : assigned to
    ComplaintAssignment "*" --> "1" MaintenanceStaff : assigned to
    Complaint "1" --> "*" ComplaintUpdate : has history
    Complaint "1" --> "0..1" Feedback : receives
```

### 6. Explanation

| Class | Role | Maps to DB Table |
|-------|------|-----------------|
| **User** | Base class for all actors; stores credentials | `users` |
| **Student / Faculty** | Submitters of complaints (extends User) | `users` (role='STUDENT'/'FACULTY') |
| **Administrator** | Manages all complaints, assigns, generates reports | `users` (role='ADMIN') |
| **MaintenanceStaff** | Receives tasks, updates progress | `users` (role='MAINTENANCE') |
| **Complaint** | Core entity with lifecycle status | `complaints` |
| **ComplaintCategory** | Classifies complaint type | `complaint_categories` |
| **Location** | Physical campus location | `locations` |
| **ComplaintAssignment** | Links complaint to maintenance staff | `complaint_assignments` |
| **ComplaintUpdate** | Audit trail of all status changes | `complaint_updates` |
| **Feedback** | User rating after resolution | `feedback` |

**Key Relationships:**
- **Inheritance:** Student, Faculty, Administrator, MaintenanceStaff all extend User.
- **Association:** A Student/Faculty submits many Complaints; each Complaint belongs to one User.
- **Dependency:** Each Complaint has one Category and one Location.
- **Aggregation:** An Administrator creates ComplaintAssignments; a MaintenanceStaff receives them.
- **Composition:** A Complaint owns its ComplaintUpdates (deletes cascade).
- **Association:** A Complaint optionally has one Feedback entry.

### 7. Result
The structural Class Diagram for the CCMS was successfully modeled with **10 classes**, **4 inheritance relationships**, and **6 association/composition relationships**, all consistent with the implemented database schema and backend controllers.

