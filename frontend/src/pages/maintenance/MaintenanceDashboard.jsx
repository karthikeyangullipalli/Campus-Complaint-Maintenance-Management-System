import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../../utils/api';

const MaintenanceDashboard = () => {
  const [data, setData] = useState({ byStatus: [], tasks: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      const res = await api.get('/dashboard/maintenance');
      setData(res.data.data || { byStatus: [], tasks: [] });
    } catch (error) {
      console.error('Error fetching maintenance dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Maintenance Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        {data.byStatus.map(stat => (
          <div key={stat.status} className="bg-white p-6 rounded-lg shadow border-t-4 border-blue-500">
            <h3 className="text-gray-500 text-sm font-semibold uppercase">{stat.status}</h3>
            <p className="text-3xl font-bold text-gray-800 mt-2">{stat.count}</p>
          </div>
        ))}
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">Recent Tasks</h2>
          <Link to="/maintenance/tasks" className="text-blue-600 hover:underline text-sm">View All</Link>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="border-b bg-gray-50">
                <th className="p-3 text-sm font-semibold text-gray-600">Complaint #</th>
                <th className="p-3 text-sm font-semibold text-gray-600">Title</th>
                <th className="p-3 text-sm font-semibold text-gray-600">Status</th>
                <th className="p-3 text-sm font-semibold text-gray-600">Date Assigned</th>
              </tr>
            </thead>
            <tbody>
              {data.tasks.map(task => (
                <tr key={task.id} className="border-b hover:bg-gray-50">
                  <td className="p-3 text-sm font-medium">{task.complaint_number}</td>
                  <td className="p-3 text-sm">
                    <Link to={`/maintenance/tasks/${task.id}`} className="text-blue-600 hover:underline">
                      {task.title}
                    </Link>
                  </td>
                  <td className="p-3 text-sm">
                    <span className="px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800">
                      {task.status}
                    </span>
                  </td>
                  <td className="p-3 text-sm text-gray-500">
                    {new Date(task.assigned_at).toLocaleDateString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {data.tasks.length === 0 && (
            <div className="p-4 text-center text-gray-500">No tasks assigned yet.</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MaintenanceDashboard;
