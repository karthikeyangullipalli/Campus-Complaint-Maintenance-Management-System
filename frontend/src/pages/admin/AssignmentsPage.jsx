import React, { useEffect, useState } from 'react';
import api from '../../utils/api';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import { formatDate } from '../../utils/helpers';
import StatusBadge from '../../components/common/StatusBadge';
import { Link } from 'react-router-dom';

const AssignmentsPage = () => {
  const [assignments, setAssignments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAssignments();
  }, []);

  const fetchAssignments = async () => {
    try {
      const res = await api.get('/assignments'); // Assuming this endpoint exists, or would filter assignments
      // For now we might not have a dedicated endpoint, so let's just fetch all complaints that have assignments
      const compRes = await api.get('/complaints');
      const assigned = compRes.data.complaints.filter(c => c.assignment);
      setAssignments(assigned);
    } catch (error) {
      console.error("Error fetching assignments", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Staff Assignments</h1>
      
      <div className="bg-white shadow-sm rounded-lg border border-gray-100 overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Complaint</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Staff Assigned</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Assigned By</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {assignments.map(complaint => (
              <tr key={complaint.id}>
                <td className="px-6 py-4 whitespace-nowrap">
                  <Link to={`/admin/complaints/${complaint.id}`} className="text-sm font-medium text-primary hover:underline">
                    #{complaint.id} - {complaint.title}
                  </Link>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{complaint.assignment?.assignee?.name}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{complaint.assignment?.assignedBy?.name}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{formatDate(complaint.assignment?.createdAt)}</td>
                <td className="px-6 py-4 whitespace-nowrap"><StatusBadge status={complaint.status} /></td>
              </tr>
            ))}
            {assignments.length === 0 && (
              <tr>
                <td colSpan="5" className="px-6 py-4 text-center text-sm text-gray-500">No active assignments found.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AssignmentsPage;
