import React from 'react';
import { NavLink } from 'react-router-dom';
import { FiHome, FiList, FiPlus, FiUsers, FiLayers, FiMapPin, FiBriefcase, FiTool } from 'react-icons/fi';

const Sidebar = ({ role }) => {
  let links = [];

  if (role === 'STUDENT' || role === 'FACULTY') {
    links = [
      { to: '/student/dashboard', icon: <FiHome />, label: 'Dashboard' },
      { to: '/student/complaints/new', icon: <FiPlus />, label: 'New Complaint' },
      { to: '/student/complaints', icon: <FiList />, label: 'My Complaints' },
    ];
  } else if (role === 'ADMIN') {
    links = [
      { to: '/admin/dashboard', icon: <FiHome />, label: 'Dashboard' },
      { to: '/admin/complaints', icon: <FiList />, label: 'Complaints' },
      { to: '/admin/assignments', icon: <FiBriefcase />, label: 'Assignments' },
      { to: '/admin/users', icon: <FiUsers />, label: 'Users' },
      { to: '/admin/categories', icon: <FiLayers />, label: 'Categories' },
      { to: '/admin/locations', icon: <FiMapPin />, label: 'Locations' },
    ];
  } else if (role === 'MAINTENANCE_STAFF') {
    links = [
      { to: '/maintenance/dashboard', icon: <FiHome />, label: 'Dashboard' },
      { to: '/maintenance/tasks', icon: <FiTool />, label: 'My Tasks' },
    ];
  }

  return (
    <aside className="w-64 bg-primary text-white flex flex-col hidden md:flex h-full">
      <div className="h-16 flex items-center px-6 font-bold text-xl tracking-wider border-b border-blue-800">
        CCMS Portal
      </div>
      <nav className="flex-1 py-6 px-3 space-y-1 overflow-y-auto">
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) =>
              `flex items-center px-4 py-3 text-sm rounded-lg transition-colors ${
                isActive ? 'bg-secondary text-white' : 'text-blue-100 hover:bg-blue-800'
              }`
            }
          >
            <span className="w-5 h-5 mr-3">{link.icon}</span>
            {link.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
};

export default Sidebar;
