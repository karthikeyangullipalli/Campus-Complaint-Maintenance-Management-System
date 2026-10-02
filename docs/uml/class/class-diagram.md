# Class Diagram

## Mermaid Class Diagram

```mermaid
classDiagram
    class User {
        +Int id
        +String name
        +String email
        +String password_hash
        +String role
        +String department
        +String phone
        +Boolean is_active
        +login(): boolean
        +logout(): void
        +updateProfile(): void
    }

    class Student {
        +String rollNumber
        +String department
        +String hostel
    }

    class Faculty {
        +String employeeId
        +String department
        +String officeRoom
    }

    class MaintenanceStaff {
        +String staffId
        +String specialization
        +boolean isAvailable
        +viewAssignments(): List~ComplaintAssignment~
        +updateStatus(complaintId, status): void
    }

    class Administrator {
        +String adminId
        +verifyComplaint(complaintId): void
        +assignStaff(complaintId, staffId): void
        +generateReport(): Report
        +manageUsers(): void
    }

    class Complaint {
        +Int id
        +String complaint_number
        +Int user_id
        +Int category_id
        +Int location_id
        +String title
        +String description
        +String priority
        +String status
        +String image_path
        +Timestamp created_at
        +Timestamp updated_at
        +Timestamp resolved_at
        +Timestamp closed_at
        +submit(): void
        +updateStatus(newStatus): void
        +getDetails(): Complaint
    }

    class ComplaintCategory {
        +Int id
        +String name
        +String description
        +Boolean is_active
        +getCategoryInfo(): String
    }

    class Location {
        +Int id
        +String building
        +String floor
        +String room
        +String description
        +Boolean is_active
        +getDisplayName(): String
    }

    class ComplaintAssignment {
        +Int id
        +Int complaint_id
        +Int maintenance_staff_id
        +Int assigned_by
        +Timestamp assigned_at
        +String notes
        +createAssignment(): void
    }

    class ComplaintUpdate {
        +Int id
        +Int complaint_id
        +Int updated_by
        +String old_status
        +String new_status
        +String remarks
        +Timestamp created_at
        +addUpdate(): void
    }

    class Feedback {
        +String feedbackId
        +int rating
        +String comments
        +Date feedbackDate
        +submitFeedback(): void
    }

    class Notification {
        +String notificationId
        +String message
        +Date timestamp
        +boolean isRead
        +send(): void
        +markAsRead(): void
    }

    class Dashboard {
        +int totalComplaints
        +int pendingComplaints
        +int resolvedComplaints
        +loadStatistics(): void
        +refresh(): void
    }

    class Report {
        +String reportId
        +Date generatedDate
        +String reportType
        +String data
        +exportPDF(): void
        +exportCSV(): void
    }

    %% Inheritance
    User <|-- Student
    User <|-- Faculty
    User <|-- MaintenanceStaff
    User <|-- Administrator

    %% Associations
    Student "1" -- "*" Complaint : submits
    Faculty "1" -- "*" Complaint : submits
    Administrator "1" -- "*" Complaint : verifies/closes
    Administrator "1" -- "*" Report : generates

    Complaint "*" -- "1" ComplaintCategory : categorized as
    Complaint "*" -- "1" Location : located at
    
    Complaint "1" *-- "*" ComplaintUpdate : tracks progress
    Complaint "1" -- "0..1" Feedback : receives
    
    Complaint "1" -- "0..1" ComplaintAssignment : assigned via
    ComplaintAssignment "0..*" -- "1" MaintenanceStaff : handled by
    
    User "1" -- "*" Notification : receives
    User "1" -- "1" Dashboard : views
```

## Detailed Explanation of Classes

1. **User (Abstract/Base Class)**: Represents the base entity for all actors in the system. Contains common attributes like name, email, and authentication methods.
2. **Student**: Inherits from User. Represents a student submitting complaints, contains specific fields like roll number.
3. **Faculty**: Inherits from User. Represents teaching staff, contains employee ID and office details.
4. **MaintenanceStaff**: Inherits from User. Represents the workers who resolve complaints. Has a specialization (e.g., plumbing, electrical).
5. **Administrator**: Inherits from User. Handles system oversight, complaint verification, assignment, and report generation.
6. **Complaint**: The core business entity. Contains all details regarding an issue raised by a Student/Faculty.
7. **ComplaintCategory**: Defines the classification of the complaint (e.g., Electrical, IT, Civil) for better routing.
8. **Location**: Specifies where the issue is occurring (building, room).
9. **ComplaintAssignment**: An associative entity representing the allocation of a specific complaint to a specific maintenance staff member.
10. **ComplaintUpdate**: Records the history and progression of a complaint's status over time.
11. **Feedback**: Stores user ratings and comments after a complaint is resolved and closed.
12. **Notification**: System alerts sent to users regarding status changes or new assignments.
13. **Dashboard**: Represents the UI aggregation of data showing statistics for a specific user role.
14. **Report**: An entity representing aggregated data exports generated by the Administrator.
