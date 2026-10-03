import React, { useState, useEffect } from 'react';
import api from '../../utils/api';

const UsersPage = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const res = await api.get('/users');
      setUsers(res.data.data || []);
    } catch (error) {
      console.error('Error fetching users:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDeactivate = async (id) => {
    if (!window.confirm('Deactivate this user?')) return;
    try {
      await api.put(`/users/${id}`, { is_active: false });
      fetchUsers();
    } catch (error) {
      console.error('Error deactivating user:', error);
      alert(error.response?.data?.message || 'Error deactivating user');
    }
  };

  if (loading) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Manage Users</h1>
      
      <div className="bg-white rounded shadow overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-gray-50 border-b">
              <th className="p-4 font-semibold text-sm text-gray-600">Name</th>
              <th className="p-4 font-semibold text-sm text-gray-600">Email</th>
              <th className="p-4 font-semibold text-sm text-gray-600">Role</th>
              <th className="p-4 font-semibold text-sm text-gray-600">Department</th>
              <th className="p-4 font-semibold text-sm text-gray-600">Status</th>
              <th className="p-4 font-semibold text-sm text-gray-600">Action</th>
            </tr>
          </thead>
          <tbody>
            {users.map(user => (
              <tr key={user.id} className="border-b hover:bg-gray-50">
                <td className="p-4 text-sm font-medium text-gray-900">{user.name}</td>
                <td className="p-4 text-sm text-gray-700">{user.email}</td>
                <td className="p-4 text-sm text-gray-700">{user.role}</td>
                <td className="p-4 text-sm text-gray-700">{user.department || '-'}</td>
                <td className="p-4 text-sm text-gray-700">
                  <span className={`px-2 py-1 text-xs rounded-full ${user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {user.is_active ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td className="p-4 text-sm text-red-600">
                  {user.is_active && user.role !== 'ADMIN' && (
                    <button onClick={() => handleDeactivate(user.id)} className="hover:underline">
                      Deactivate
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {users.length === 0 && (
          <div className="p-4 text-center text-gray-500">No users found.</div>
        )}
      </div>
    </div>
  );
};

export default UsersPage;
