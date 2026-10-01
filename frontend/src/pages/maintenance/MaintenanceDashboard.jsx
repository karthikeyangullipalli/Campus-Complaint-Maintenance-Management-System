import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../../utils/api';
import StatsCard from '../../components/common/StatsCard';
import StatusBadge from '../../components/common/StatusBadge';
import PriorityBadge from '../../components/common/PriorityBadge';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import { formatDate } from '../../utils/helpers';
import { FiTool, FiCheckCircle, FiClock, FiList } from 'react-icons/fi';

const MaintenanceDashboard = () => {
  const [stats, setStats] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const [statsRes, tasksRes] = await Promise.all([
          api.get('/dashboard/maintenance'),
          api.get('/complaints/assigned')
        ]);
        setStats(statsRes.data);
        setTasks(tasksRes.data.complaints || []);
      } catch (error) {
        console.error("Error fetching maintenance dashboard", error);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  if (loading) return <LoadingSpinner />;

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Maintenance Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <StatsCard title="Assigned Tasks" value={stats?.totalAssigned || 0} icon={FiList} colorClass="text-purple-600 bg-purple-100" />
        <StatsCard title="In Progress" value={stats?.inProgress || 0} icon={FiTool} colorClass="text-yellow-600 bg-yellow-100" />
        <StatsCard title="Resolved" value={stats?.resolved || 0} icon={FiCheckCircle} colorClass="text-green-600 bg-green-100" />
      </div>

      <div className="bg-white shadow-sm rounded-lg border border-gray-100 overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center">
          <h2 className="text-lg font-medium text-gray-900">Current Tasks</h2>
          <Link to="/maintenance/tasks" className="text-sm text-primary hover:underline">View all</Link>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Title</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Priority</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {tasks.slice(0, 5).map(task => (
                <tr key={task.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">#{task.id}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <Link to={`/maintenance/tasks/${task.id}`} className="text-sm font-medium text-primary hover:underline">
                      {task.title}
                    </Link>
                    <div className="text-xs text-gray-500">{task.location?.name}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap"><PriorityBadge priority={task.priority} /></td>
                  <td className="px-6 py-4 whitespace-nowrap"><StatusBadge status={task.status} /></td>
                </tr>
              ))}
              {tasks.length === 0 && (
                <tr>
                  <td colSpan="4" className="px-6 py-4 text-center text-sm text-gray-500">No tasks assigned.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default MaintenanceDashboard;
