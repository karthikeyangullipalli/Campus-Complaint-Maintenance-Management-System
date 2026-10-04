import os
import time
import subprocess
import urllib.request
from playwright.sync_api import sync_playwright

os.makedirs('docs/screenshots', exist_ok=True)

# Start backend
backend_proc = subprocess.Popen(
    ["node", "server.js"],
    cwd=os.path.abspath("backend"),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
print("Started backend process (PID:", backend_proc.pid, ")")

# Start frontend
frontend_proc = subprocess.Popen(
    ["npm.cmd", "run", "dev", "--", "--port", "5173"],
    cwd=os.path.abspath("frontend"),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
print("Started frontend process (PID:", frontend_proc.pid, ")")

# Wait for backend and frontend to be ready
def wait_for_url(url, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        try:
            req = urllib.request.urlopen(url)
            if req.status in [200, 304]:
                return True
        except Exception:
            time.sleep(0.5)
    return False

print("Waiting for backend on http://localhost:5000/api/health...")
if wait_for_url("http://localhost:5000/api/health"):
    print("Backend is ready!")
else:
    print("Backend failed to start in time!")

print("Waiting for frontend on http://localhost:5173...")
if wait_for_url("http://localhost:5173"):
    print("Frontend is ready!")
else:
    print("Frontend failed to start in time!")

time.sleep(2)

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='chrome')
        page = browser.new_page(viewport={'width': 1280, 'height': 800})
        
        # 1. Login Page
        page.goto('http://localhost:5173/login')
        page.wait_for_selector('text=CCMS Portal')
        page.screenshot(path='docs/screenshots/01_login_page.png')
        print('Captured 01_login_page.png')
        
        # 2. Register Page
        page.goto('http://localhost:5173/register')
        page.wait_for_selector('text=Create an account')
        page.screenshot(path='docs/screenshots/02_register_page.png')
        print('Captured 02_register_page.png')
        
        # 3. Login as Student
        page.goto('http://localhost:5173/login')
        page.fill('input[type="email"]', 'student@ccms.local')
        page.fill('input[type="password"]', 'Admin@123')
        page.click('button[type="submit"]')
        page.wait_for_url('**/student/dashboard')
        page.wait_for_timeout(1500)
        page.screenshot(path='docs/screenshots/03_student_dashboard.png')
        print('Captured 03_student_dashboard.png')
        
        # 4. Student New Complaint
        page.goto('http://localhost:5173/student/complaints/new')
        page.wait_for_selector('text=File a New Complaint')
        page.screenshot(path='docs/screenshots/04_new_complaint.png')
        print('Captured 04_new_complaint.png')
        
        # 5. Student Complaints List
        page.goto('http://localhost:5173/student/complaints')
        page.wait_for_selector('text=My Complaints')
        page.wait_for_timeout(1500)
        page.screenshot(path='docs/screenshots/05_student_complaints_list.png')
        print('Captured 05_student_complaints_list.png')
        
        # 6. Student Complaint Detail
        page.goto('http://localhost:5173/student/complaints/1')
        page.wait_for_timeout(1500)
        page.screenshot(path='docs/screenshots/06_student_complaint_detail.png')
        print('Captured 06_student_complaint_detail.png')
        
        # 7. Logout and Login as Admin
        page.evaluate('localStorage.clear()')
        page.goto('http://localhost:5173/login')
        page.fill('input[type="email"]', 'admin@ccms.local')
        page.fill('input[type="password"]', 'Admin@123')
        page.click('button[type="submit"]')
        page.wait_for_url('**/admin/dashboard')
        page.wait_for_timeout(1500)
        page.screenshot(path='docs/screenshots/07_admin_dashboard.png')
        print('Captured 07_admin_dashboard.png')
        
        # 8. Admin Complaints Management
        page.goto('http://localhost:5173/admin/complaints')
        page.wait_for_selector('text=Manage Complaints')
        page.wait_for_timeout(1500)
        page.screenshot(path='docs/screenshots/08_admin_complaints.png')
        print('Captured 08_admin_complaints.png')
        
        # 9. Admin Complaint Detail / Manage
        page.goto('http://localhost:5173/admin/complaints/1')
        page.wait_for_timeout(1500)
        page.screenshot(path='docs/screenshots/09_admin_complaint_detail.png')
        print('Captured 09_admin_complaint_detail.png')
        
        # 10. Admin Users Page
        page.goto('http://localhost:5173/admin/users')
        page.wait_for_selector('text=Manage Users')
        page.wait_for_timeout(1500)
        page.screenshot(path='docs/screenshots/10_admin_users.png')
        print('Captured 10_admin_users.png')
        
        # 11. Admin Categories Page
        page.goto('http://localhost:5173/admin/categories')
        page.wait_for_selector('text=Manage Categories')
        page.wait_for_timeout(1500)
        page.screenshot(path='docs/screenshots/11_admin_categories.png')
        print('Captured 11_admin_categories.png')
        
        # 12. Admin Locations Page
        page.goto('http://localhost:5173/admin/locations')
        page.wait_for_selector('text=Manage Locations')
        page.wait_for_timeout(1500)
        page.screenshot(path='docs/screenshots/12_admin_locations.png')
        print('Captured 12_admin_locations.png')
        
        # 13. Admin Assignments Page
        page.goto('http://localhost:5173/admin/assignments')
        page.wait_for_selector('text=All Assignments')
        page.wait_for_timeout(1500)
        page.screenshot(path='docs/screenshots/13_admin_assignments.png')
        print('Captured 13_admin_assignments.png')
        
        # 14. Logout and Login as Maintenance
        page.evaluate('localStorage.clear()')
        page.goto('http://localhost:5173/login')
        page.fill('input[type="email"]', 'maintenance@ccms.local')
        page.fill('input[type="password"]', 'Admin@123')
        page.click('button[type="submit"]')
        page.wait_for_url('**/maintenance/dashboard')
        page.wait_for_timeout(1500)
        page.screenshot(path='docs/screenshots/14_maintenance_dashboard.png')
        print('Captured 14_maintenance_dashboard.png')
        
        # 15. Maintenance My Tasks
        page.goto('http://localhost:5173/maintenance/tasks')
        page.wait_for_selector('text=My Assigned Tasks')
        page.wait_for_timeout(1500)
        page.screenshot(path='docs/screenshots/15_maintenance_tasks.png')
        print('Captured 15_maintenance_tasks.png')
        
        # 16. Maintenance Task Detail
        page.goto('http://localhost:5173/maintenance/tasks/3')
        page.wait_for_timeout(1500)
        page.screenshot(path='docs/screenshots/16_maintenance_task_detail.png')
        print('Captured 16_maintenance_task_detail.png')

        browser.close()
        print('All 16 screenshots captured successfully!')

finally:
    try:
        backend_proc.terminate()
        frontend_proc.terminate()
        print('Cleaned up processes.')
    except Exception:
        pass
