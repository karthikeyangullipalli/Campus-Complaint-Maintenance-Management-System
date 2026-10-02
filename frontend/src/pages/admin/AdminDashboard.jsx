import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../../utils/api';
import StatsCard from '../../components/common/StatsCard';
import StatusBadge from '../../components/common/StatusBadge';
import PriorityBadge from '../../components/common/PriorityBadge';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import { formatDate } from '../../utils/helpers';
import { FiFileText, FiAlertCircle, FiCheckSquare, FiArchive, FiAlertTriangle } from 'react-icons/fi';

const sumStatuses = (byStatus, statuses) => {
  if (!Array.isArray(byStatus)) return 0;
  return byStatus
    .filter(s => statuses.includes(s.status))
    .reduce((acc, s) => acc + Number(s.count), 0);
};

const AdminDashboard = () => {
  const [dashData, setDashData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        // GET /api/dashboard/admin → { success, data: { byStatus, byCategory, byPriority, criticalOpen, recent } }
        const res = await api.get('/dashboard/admin');
        setDashData(res.data.data || {});
      } catch (error) {
        console.error('Error fetching admin dashboard', error);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  if (loading) return <LoadingSpinner />;

  const byStatus   = dashData?.byStatus || [];
  const byCategory = dashData?.byCategory || [];
  const recent     = dashData?.recent || [];

  const totalComplaints = byStatus.reduce((acc, s) => acc + Number(s.count), 0);
  const newCount        = sumStatuses(byStatus, ['NEW']);
  const inProgCount     = sumStatuses(byStatus, ['IN_PROGRESS', 'ASSIGNED', 'VERIFIED']);
  const resolvedCount   = sumStatuses(byStatus, ['RESOLVED', 'CLOSED']);

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Admin Dashboard</h1>

      {/* Stats Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
        <StatsCard title="Total"       value={totalComplaints}            icon={FiFileText}      colorClass="text-blue-600 bg-blue-100" />
        <StatsCard title="New"         value={newCount}                   icon={FiAlertCircle}   colorClass="text-red-600 bg-red-100" />
        <StatsCard title="Active"      value={inProgCount}                icon={FiCheckSquare}   colorClass="text-yellow-600 bg-yellow-100" />
        <StatsCard title="Closed"      value={resolvedCount}              icon={FiArchive}       colorClass="text-green-600 bg-green-100" />
        <StatsCard title="High/Critical Open" value={dashData?.criticalOpen || 0} icon={FiAlertTriangle} colorClass="text-orange-600 bg-orange-100" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Complaints by Status */}
        <div className="bg-white shadow-sm rounded-lg border border-gray-100 p-6">
          <h2 className="text-base font-semibold text-gray-900 mb-4">Complaints by Status</h2>
          <div className="space-y-2">
            {byStatus.map(s => (
              <div key={s.status} className="flex items-center justify-between">
                <StatusBadge status={s.status} />
                <span className="text-sm font-semibold text-gray-700">{s.count}</span>
              </div>
            ))}
            {byStatus.length === 0 && <p className="text-sm text-gray-400">No data</p>}
          </div>
        </div>

        {/* Complaints by Category */}
        <div className="bg-white shadow-sm rounded-lg border border-gray-100 p-6">
          <h2 className="text-base font-semibold text-gray-900 mb-4">Complaints by Category</h2>
          <div className="space-y-2">
            {byCategory.map(c => (
              <div key={c.name} className="flex items-center justify-between">
                <span className="text-sm text-gray-600">{c.name}</span>
                <span className="text-sm font-semibold text-gray-700">{c.count}</span>
              </div>
            ))}
            {byCategory.length === 0 && <p className="text-sm text-gray-400">No data</p>}
          </div>
        </div>
      </div>

      {/* Recent Complaints */}
      <div className="bg-white shadow-sm rounded-lg border border-gray-100 overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center">
          <h2 className="text-lg font-medium text-gray-900">Recent Complaints (Last 10)</h2>
          <Link to="/admin/complaints" className="text-sm text-blue-700 hover:underline">View all</Link>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Complaint #</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Title</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Submitted By</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Category</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {recent.length === 0 ? (
                <tr>
                  <td colSpan="6" className="px-6 py-8 text-center text-sm text-gray-500">No complaints yet.</td>
                </tr>
              ) : (
                recent.map(c => (
                  <tr key={c.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-xs font-mono text-gray-400">{c.complaint_number}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <Link to={`/admin/complaints/${c.id}`} className="text-sm font-medium text-blue-700 hover:underline">
                        {c.title}
                      </Link>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{c.user_name}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{c.category_name || '—'}</td>
                    <td className="px-6 py-4 whitespace-nowrap"><StatusBadge status={c.status} /></td>
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

export default AdminDashboard;
