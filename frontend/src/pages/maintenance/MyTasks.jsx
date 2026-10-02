import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const MyTasks = () => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const res = await axios.get('/api/assignments/my');
      setTasks(res.data.data || []);
    } catch (error) {
      console.error('Error fetching tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusUpdate = async (id, new_status, remarks = '') => {
    try {
      await axios.put(`/api/complaints/${id}/status`, { new_status, remarks });
      fetchTasks();
    } catch (error) {
      console.error('Error updating task status:', error);
    }
  };

  if (loading) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">My Assigned Tasks</h1>
      
      <div className="bg-white rounded shadow overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-gray-50 border-b">
              <th className="p-4 font-semibold text-sm text-gray-600">Complaint #</th>
              <th className="p-4 font-semibold text-sm text-gray-600">Title & Location</th>
              <th className="p-4 font-semibold text-sm text-gray-600">Category</th>
              <th className="p-4 font-semibold text-sm text-gray-600">Status</th>
              <th className="p-4 font-semibold text-sm text-gray-600">Assigned At</th>
              <th className="p-4 font-semibold text-sm text-gray-600">Actions</th>
            </tr>
          </thead>
          <tbody>
            {tasks.map(task => (
              <tr key={task.id} className="border-b hover:bg-gray-50">
                <td className="p-4 text-sm font-medium text-gray-900">{task.complaint_number}</td>
                <td className="p-4 text-sm text-gray-700">
                  <div className="font-semibold">{task.title}</div>
                  <div className="text-xs text-gray-500">{task.location_name}</div>
                </td>
                <td className="p-4 text-sm text-gray-700">{task.category_name}</td>
                <td className="p-4 text-sm text-gray-700">
                  <span className={`px-2 py-1 text-xs rounded-full ${task.status === 'RESOLVED' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                    {task.status}
                  </span>
                </td>
                <td className="p-4 text-sm text-gray-700">{new Date(task.assigned_at).toLocaleString()}</td>
                <td className="p-4 text-sm space-x-2">
                  <Link to={`/maintenance/tasks/${task.id}`} className="text-blue-600 hover:underline mr-2">View</Link>
                  {task.status === 'ASSIGNED' && (
                    <button 
                      onClick={() => handleStatusUpdate(task.id, 'IN_PROGRESS')}
                      className="px-2 py-1 bg-blue-600 text-white text-xs rounded hover:bg-blue-700"
                    >
                      Start Work
                    </button>
                  )}
                  {task.status === 'IN_PROGRESS' && (
                    <button 
                      onClick={() => {
                        const remarks = prompt("Resolution remarks:");
                        if (remarks !== null) handleStatusUpdate(task.id, 'RESOLVED', remarks);
                      }}
                      className="px-2 py-1 bg-green-600 text-white text-xs rounded hover:bg-green-700"
                    >
                      Mark Resolved
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {tasks.length === 0 && (
          <div className="p-4 text-center text-gray-500">No tasks assigned to you right now.</div>
        )}
      </div>
    </div>
  );
};

export default MyTasks;
