import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../../utils/api';
import StatsCard from '../../components/common/StatsCard';
import StatusBadge from '../../components/common/StatusBadge';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import { formatDate } from '../../utils/helpers';
import { FiFileText, FiAlertCircle, FiCheckSquare, FiArchive } from 'react-icons/fi';

const AdminDashboard = () => {
  const [stats, setStats] = useState(null);
  const [recentComplaints, setRecentComplaints] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const [statsRes, complaintsRes] = await Promise.all([
          api.get('/dashboard/admin'),
          api.get('/complaints?limit=10')
        ]);
        setStats(statsRes.data);
        setRecentComplaints(complaintsRes.data.complaints || []);
      } catch (error) {
        console.error("Error fetching admin dashboard", error);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  if (loading) return <LoadingSpinner />;

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Admin Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatsCard title="Total Complaints" value={stats?.total || 0} icon={FiFileText} />
        <StatsCard title="New & Unverified" value={(stats?.byStatus?.NEW || 0)} icon={FiAlertCircle} colorClass="text-red-600 bg-red-100" />
        <StatsCard title="In Progress" value={(stats?.byStatus?.IN_PROGRESS || 0)} icon={FiCheckSquare} colorClass="text-yellow-600 bg-yellow-100" />
        <StatsCard title="Resolved/Closed" value={(stats?.byStatus?.RESOLVED || 0) + (stats?.byStatus?.CLOSED || 0)} icon={FiArchive} colorClass="text-green-600 bg-green-100" />
      </div>

      <div className="bg-white shadow-sm rounded-lg border border-gray-100 overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center">
          <h2 className="text-lg font-medium text-gray-900">Recent Complaints</h2>
          <Link to="/admin/complaints" className="text-sm text-primary hover:underline">View all</Link>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Title</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {recentComplaints.map(complaint => (
                <tr key={complaint.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">#{complaint.id}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <Link to={`/admin/complaints/${complaint.id}`} className="text-sm font-medium text-primary hover:underline">
                      {complaint.title}
                    </Link>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap"><StatusBadge status={complaint.status} /></td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{formatDate(complaint.createdAt)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
