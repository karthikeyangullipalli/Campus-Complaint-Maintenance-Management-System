import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { FiFileText, FiClock, FiCheckCircle, FiInbox } from 'react-icons/fi';
import api from '../../utils/api';
import StatsCard from '../../components/common/StatsCard';
import StatusBadge from '../../components/common/StatusBadge';
import PriorityBadge from '../../components/common/PriorityBadge';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import { formatDate } from '../../utils/helpers';

// Helper to sum counts from byStatus array [{status, count}, ...]
const sumStatuses = (byStatus, statuses) => {
  if (!Array.isArray(byStatus)) return 0;
  return byStatus
    .filter(s => statuses.includes(s.status))
    .reduce((acc, s) => acc + Number(s.count), 0);
};

const StudentDashboard = () => {
  const [dashData, setDashData] = useState(null);
  const [recentComplaints, setRecentComplaints] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        // GET /api/dashboard/student → { success, data: { byStatus: [{status,count}], total, open, recent } }
        const dashRes = await api.get('/dashboard/student');
        const d = dashRes.data.data || {};
        setDashData(d);
        setRecentComplaints(d.recent || []);
      } catch (error) {
        console.error('Error fetching dashboard data', error);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  if (loading) return <LoadingSpinner />;

  const byStatus = dashData?.byStatus || [];
  const total    = dashData?.total || 0;
  const pending  = sumStatuses(byStatus, ['NEW', 'VERIFIED', 'ASSIGNED']);
  const inProg   = sumStatuses(byStatus, ['IN_PROGRESS']);
  const resolved = sumStatuses(byStatus, ['RESOLVED', 'CLOSED']);

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">My Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatsCard title="Total Complaints"  value={total}    icon={FiFileText}    colorClass="text-blue-600 bg-blue-100" />
        <StatsCard title="Pending"           value={pending}  icon={FiInbox}       colorClass="text-yellow-600 bg-yellow-100" />
        <StatsCard title="In Progress"       value={inProg}   icon={FiClock}       colorClass="text-orange-600 bg-orange-100" />
        <StatsCard title="Resolved / Closed" value={resolved} icon={FiCheckCircle} colorClass="text-green-600 bg-green-100" />
      </div>

      <div className="bg-white shadow-sm rounded-lg border border-gray-100 overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center">
          <h2 className="text-lg font-medium text-gray-900">Recent Complaints</h2>
          <Link to="/student/complaints" className="text-sm text-blue-700 hover:underline">View all</Link>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Complaint #</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Title</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {recentComplaints.length === 0 ? (
                <tr>
                  <td colSpan="5" className="px-6 py-8 text-center text-sm text-gray-500">
                    No complaints yet.{' '}
                    <Link to="/student/complaints/new" className="text-blue-700 hover:underline">File your first complaint</Link>
                  </td>
                </tr>
              ) : (
                recentComplaints.map(c => (
                  <tr key={c.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-xs font-mono text-gray-500">{c.complaint_number}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <Link to={`/student/complaints/${c.id}`} className="text-sm font-medium text-blue-700 hover:underline">
                        {c.title}
                      </Link>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{c.category_name || '—'}</td>
                    <td className="px-6 py-4 whitespace-nowrap"><StatusBadge status={c.status} /></td>
                    {/* MySQL returns snake_case: created_at */}
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{formatDate(c.created_at)}</td>
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
