USE ccms_db;

-- 1. Users
-- Password for all users is Admin@123 (hashed)
INSERT INTO users (name, email, password_hash, role, department, phone) VALUES
('Admin User', 'admin@ccms.local', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lh23', 'ADMIN', 'IT', '1234567890'),
('Student User', 'student@ccms.local', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lh23', 'STUDENT', 'Computer Science', '1234567891'),
('Faculty User', 'faculty@ccms.local', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lh23', 'FACULTY', 'Mechanical Engineering', '1234567892'),
('Maintenance Staff 1', 'maintenance@ccms.local', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lh23', 'MAINTENANCE', 'Facilities', '1234567893'),
('Maintenance Staff 2', 'maintenance2@ccms.local', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lh23', 'MAINTENANCE', 'Facilities', '1234567894');

-- 2. Complaint Categories
INSERT INTO complaint_categories (name, description) VALUES
('Electrical', 'Issues related to power, lights, fans, etc.'),
('Plumbing', 'Issues with water, pipes, washrooms, leaks.'),
('Furniture', 'Broken desks, chairs, tables, etc.'),
('Cleaning', 'Issues regarding cleanliness of rooms or corridors.'),
('Internet/Network', 'Wi-Fi or LAN connection issues.'),
('Classroom Equipment', 'Projectors, whiteboards, microphones.'),
('Laboratory Equipment', 'Defective lab machinery or computers.'),
('HVAC', 'Heating, Ventilation, and Air Conditioning issues.'),
('Security', 'Issues related to locks, doors, or campus security.'),
('Other', 'Miscellaneous issues.');

-- 3. Locations
INSERT INTO locations (building, floor, room, description) VALUES
('Main Block', 'Ground Floor', 'G-01', 'Reception area'),
('Main Block', 'First Floor', '101', 'Classroom'),
('Main Block', 'First Floor', '102', 'Classroom'),
('CS Block', 'Ground Floor', 'CS-Lab1', 'Computer Lab 1'),
('CS Block', 'First Floor', 'Staff Room', 'CS Faculty Staff Room'),
('Library', 'Ground Floor', 'Reading Room', 'Main Reading Area'),
('Hostel A', 'Second Floor', '205', 'Student Room'),
('Hostel A', 'Ground Floor', 'Mess', 'Dining Area'),
('Sports Complex', 'Ground Floor', 'Gym', 'Gymnasium'),
('Auditorium', 'Ground Floor', 'Main Hall', 'Main event hall');

-- 4. Complaints
INSERT INTO complaints (complaint_number, user_id, category_id, location_id, title, description, priority, status) VALUES
('CMP-20231001-001', 2, 1, 2, 'Fan not working in 101', 'The ceiling fan near the door is making noise and not spinning properly.', 'MEDIUM', 'NEW'),
('CMP-20231001-002', 3, 6, 3, 'Projector bulb fused', 'The projector in room 102 is not turning on. Needs bulb replacement.', 'HIGH', 'VERIFIED'),
('CMP-20231002-003', 2, 5, 7, 'No Wi-Fi in Hostel Room', 'Unable to connect to the campus Wi-Fi network from room 205.', 'MEDIUM', 'ASSIGNED'),
('CMP-20231002-004', 3, 2, 5, 'Leaking tap in washroom', 'The tap in the CS staff washroom is leaking continuously.', 'LOW', 'IN_PROGRESS'),
('CMP-20231003-005', 2, 3, 6, 'Broken chair in Library', 'One of the reading chairs has a broken leg.', 'LOW', 'RESOLVED'),
('CMP-20231003-006', 3, 7, 4, 'PC #12 not booting', 'Computer number 12 in CS Lab 1 shows a disk error on boot.', 'CRITICAL', 'CLOSED'),
('CMP-20231004-007', 2, 8, 1, 'AC cooling issue', 'The AC in the reception area is blowing warm air.', 'HIGH', 'REJECTED'),
('CMP-20231004-008', 3, 4, 10, 'Dust in Auditorium', 'The seats in the auditorium are very dusty.', 'MEDIUM', 'REOPENED');

-- 5. Complaint Assignments
INSERT INTO complaint_assignments (complaint_id, maintenance_staff_id, assigned_by, notes) VALUES
(3, 4, 1, 'Check the access point near room 205.'),
(4, 5, 1, 'Please fix the washer in the tap.'),
(5, 4, 1, 'Remove the broken chair from the library.'),
(6, 4, 1, 'Check the hard drive connection or replace the drive.'),
(8, 5, 1, 'Reassigned to check dust issue again.');

-- 6. Complaint Updates
INSERT INTO complaint_updates (complaint_id, updated_by, old_status, new_status, remarks) VALUES
(2, 1, 'NEW', 'VERIFIED', 'Issue verified by admin.'),
(3, 1, 'NEW', 'ASSIGNED', 'Assigned to network technician.'),
(4, 1, 'NEW', 'ASSIGNED', 'Assigned to plumber.'),
(4, 5, 'ASSIGNED', 'IN_PROGRESS', 'Checking the tap now.'),
(5, 1, 'NEW', 'ASSIGNED', 'Assigned to carpenter.'),
(5, 4, 'ASSIGNED', 'IN_PROGRESS', 'Fixing the chair.'),
(5, 4, 'IN_PROGRESS', 'RESOLVED', 'Chair removed and sent for repair.'),
(6, 1, 'NEW', 'ASSIGNED', 'Assigned to IT support.'),
(6, 4, 'ASSIGNED', 'IN_PROGRESS', 'Checking the PC.'),
(6, 4, 'IN_PROGRESS', 'RESOLVED', 'Replaced the faulty SATA cable. PC boots now.'),
(6, 3, 'RESOLVED', 'CLOSED', 'Confirmed working.'),
(7, 1, 'NEW', 'REJECTED', 'AC maintenance is scheduled for next week by external vendor.'),
(8, 1, 'NEW', 'ASSIGNED', 'Assigned to cleaning staff.'),
(8, 5, 'ASSIGNED', 'IN_PROGRESS', 'Cleaning seats.'),
(8, 5, 'IN_PROGRESS', 'RESOLVED', 'Seats cleaned.'),
(8, 3, 'RESOLVED', 'REOPENED', 'Still dusty at the back rows.');

-- 7. Feedback
INSERT INTO feedback (complaint_id, user_id, rating, comments) VALUES
(5, 2, 4, 'Quick response, but took a while to bring a replacement chair.'),
(6, 3, 5, 'Excellent and fast service! Thanks.');
