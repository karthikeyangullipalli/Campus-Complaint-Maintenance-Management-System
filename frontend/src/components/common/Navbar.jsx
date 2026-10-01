import React from 'react';
import { useAuth } from '../../context/AuthContext';
import { FiUser, FiLogOut } from 'react-icons/fi';
import { useNavigate } from 'react-router-dom';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="bg-white shadow-sm h-16 flex items-center justify-between px-6 z-10">
      <div className="flex-1"></div>
      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-2 text-gray-700">
          <FiUser className="w-5 h-5" />
          <span className="font-medium">{user?.name}</span>
          <span className="text-xs bg-gray-200 px-2 py-1 rounded-full">{user?.role}</span>
        </div>
        <button
          onClick={handleLogout}
          className="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-full transition-colors"
          title="Logout"
        >
          <FiLogOut className="w-5 h-5" />
        </button>
      </div>
    </header>
  );
};

export default Navbar;
