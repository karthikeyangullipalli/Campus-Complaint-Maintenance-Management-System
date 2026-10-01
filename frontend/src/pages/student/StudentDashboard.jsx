import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { FiFileText, FiClock, FiCheckCircle, FiInbox } from 'react-icons/fi';
import api from '../../utils/api';
import StatsCard from '../../components/common/StatsCard';
import StatusBadge from '../../components/common/StatusBadge';
import PriorityBadge from '../../components/common/PriorityBadge';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import { formatDate } from '../../utils/helpers';

const StudentDashboard = () => {
  const [stats, setStats] = useState(null);
  const [recentComplaints, setRecentComplaints] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const [statsRes, complaintsRes] = await Promise.all([
          api.get('/dashboard/student'),
          api.get('/complaints?limit=5')
        ]);
        setStats(statsRes.data);
        setRecentComplaints(complaintsRes.data.complaints || []);
      } catch (error) {
        console.error("Error fetching dashboard data", error);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  if (loading) return <LoadingSpinner />;

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Student Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatsCard title="Total Complaints" value={stats?.total || 0} icon={FiFileText} colorClass="text-blue-600 bg-blue-100" />
        <StatsCard title="Pending" value={(stats?.byStatus?.NEW || 0) + (stats?.byStatus?.VERIFIED || 0) + (stats?.byStatus?.ASSIGNED || 0)} icon={FiInbox} colorClass="text-yellow-600 bg-yellow-100" />
        <StatsCard title="In Progress" value={stats?.byStatus?.IN_PROGRESS || 0} icon={FiClock} colorClass="text-orange-600 bg-orange-100" />
        <StatsCard title="Resolved" value={(stats?.byStatus?.RESOLVED || 0) + (stats?.byStatus?.CLOSED || 0)} icon={FiCheckCircle} colorClass="text-green-600 bg-green-100" />
      </div>

      <div className="bg-white shadow-sm rounded-lg border border-gray-100 overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center">
          <h2 className="text-lg font-medium text-gray-900">Recent Complaints</h2>
          <Link to="/student/complaints" className="text-sm text-primary hover:underline">View all</Link>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Title</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {recentComplaints.length === 0 ? (
                <tr>
                  <td colSpan="4" className="px-6 py-4 text-center text-sm text-gray-500">No complaints found.</td>
                </tr>
              ) : (
                recentComplaints.map(complaint => (
                  <tr key={complaint.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <Link to={`/student/complaints/${complaint.id}`} className="text-sm font-medium text-primary hover:underline">
                        {complaint.title}
                      </Link>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{complaint.category?.name || 'N/A'}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <StatusBadge status={complaint.status} />
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{formatDate(complaint.createdAt)}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default StudentDashboard;
