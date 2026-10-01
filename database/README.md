# Campus Complaint & Maintenance Management System (CCMS) Database Setup

This directory contains the database schema and seed data for the CCMS application.

## Prerequisites
- MySQL (v5.7 or v8.0+)
- MySQL client or a tool like phpMyAdmin, DBeaver, or MySQL Workbench

## Setup Instructions

1. **Connect to MySQL:**
   Open your terminal or command prompt and log into MySQL:
   ```bash
   mysql -u root -p
   ```

2. **Run the Schema File:**
   This will create the database `ccms_db` (if it doesn't exist) and all necessary tables.
   ```bash
   mysql -u root -p < schema.sql
   ```
   Or inside the MySQL prompt:
   ```sql
   source /path/to/database/schema.sql;
   ```

3. **Run the Seed File:**
   This will insert sample users, categories, locations, and complaints to populate the database for testing.
   ```bash
   mysql -u root -p < seed.sql
   ```
   Or inside the MySQL prompt:
   ```sql
   source /path/to/database/seed.sql;
   ```

## Demo Credentials

The `seed.sql` file creates several demo accounts. The password for all these accounts is:
**Password:** `Admin@123`

| User Role       | Email Address                | Password      |
|-----------------|------------------------------|---------------|
| Admin           | admin@ccms.local             | Admin@123     |
| Student         | student@ccms.local           | Admin@123     |
| Faculty         | faculty@ccms.local           | Admin@123     |
| Maintenance 1   | maintenance@ccms.local       | Admin@123     |
| Maintenance 2   | maintenance2@ccms.local      | Admin@123     |

## Database Tables Overview

| Table Name              | Description |
|-------------------------|-------------|
| `users`                 | Stores user accounts (Students, Faculty, Admin, Maintenance Staff) with roles and hashed passwords. |
| `complaint_categories`  | Defines types of complaints (Electrical, Plumbing, etc.). |
| `locations`             | Stores campus locations (Buildings, floors, rooms). |
| `complaints`            | Main table storing the details of each raised complaint. |
| `complaint_assignments` | Tracks which maintenance staff is assigned to which complaint. |
| `complaint_updates`     | Audit log of status changes and remarks for complaints. |
| `feedback`              | User feedback and ratings for resolved complaints. |
