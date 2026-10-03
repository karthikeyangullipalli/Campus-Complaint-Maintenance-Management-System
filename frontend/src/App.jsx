import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import ProtectedRoute from './components/common/ProtectedRoute';

import LoginPage from './pages/auth/LoginPage';
import RegisterPage from './pages/auth/RegisterPage';

import StudentLayout from './layouts/StudentLayout';
import StudentDashboard from './pages/student/StudentDashboard';
import StudentComplaintList from './pages/student/ComplaintList';
import StudentNewComplaint from './pages/student/NewComplaint';
import StudentComplaintDetail from './pages/student/ComplaintDetail';

import AdminLayout from './layouts/AdminLayout';
import AdminDashboard from './pages/admin/AdminDashboard';
import AdminComplaints from './pages/admin/AdminComplaints';
import AdminComplaintDetail from './pages/admin/ComplaintDetail';
import UsersPage from './pages/admin/UsersPage';
import CategoriesPage from './pages/admin/CategoriesPage';
import LocationsPage from './pages/admin/LocationsPage';
import AssignmentsPage from './pages/admin/AssignmentsPage';

import MaintenanceLayout from './layouts/MaintenanceLayout';
import MaintenanceDashboard from './pages/maintenance/MaintenanceDashboard';
import MyTasks from './pages/maintenance/MyTasks';
import TaskDetail from './pages/maintenance/TaskDetail';

function App() {
  const { user, isAuthenticated } = useAuth();

  return (
    <Routes>
      <Route path="/" element={
        !isAuthenticated ? <Navigate to="/login" /> :
        user.role === 'ADMIN' ? <Navigate to="/admin/dashboard" /> :
        (user.role === 'MAINTENANCE' || user.role === 'MAINTENANCE_STAFF') ? <Navigate to="/maintenance/dashboard" /> :
        <Navigate to="/student/dashboard" />
      } />
      
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      {/* Student Routes */}
      <Route path="/student" element={<ProtectedRoute allowedRoles={['STUDENT', 'FACULTY']}><StudentLayout /></ProtectedRoute>}>
        <Route path="dashboard" element={<StudentDashboard />} />
        <Route path="complaints" element={<StudentComplaintList />} />
        <Route path="complaints/new" element={<StudentNewComplaint />} />
        <Route path="complaints/:id" element={<StudentComplaintDetail />} />
      </Route>

      {/* Admin Routes */}
      <Route path="/admin" element={<ProtectedRoute allowedRoles={['ADMIN']}><AdminLayout /></ProtectedRoute>}>
        <Route path="dashboard" element={<AdminDashboard />} />
        <Route path="complaints" element={<AdminComplaints />} />
        <Route path="complaints/:id" element={<AdminComplaintDetail />} />
        <Route path="users" element={<UsersPage />} />
        <Route path="categories" element={<CategoriesPage />} />
        <Route path="locations" element={<LocationsPage />} />
        <Route path="assignments" element={<AssignmentsPage />} />
      </Route>

      {/* Maintenance Routes */}
      <Route path="/maintenance" element={<ProtectedRoute allowedRoles={['MAINTENANCE', 'MAINTENANCE_STAFF']}><MaintenanceLayout /></ProtectedRoute>}>
        <Route path="dashboard" element={<MaintenanceDashboard />} />
        <Route path="tasks" element={<MyTasks />} />
        <Route path="tasks/:id" element={<TaskDetail />} />
      </Route>
    </Routes>
  );
}

export default App;
