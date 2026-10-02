import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AssignmentsPage = () => {
  const [assignments, setAssignments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAssignments();
  }, []);

  const fetchAssignments = async () => {
    try {
      const res = await axios.get('/api/assignments');
      setAssignments(res.data.data || []);
    } catch (error) {
      console.error('Error fetching assignments:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">All Assignments</h1>
      
      <div className="bg-white rounded shadow overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-gray-50 border-b">
              <th className="p-4 font-semibold text-sm text-gray-600">Complaint #</th>
              <th className="p-4 font-semibold text-sm text-gray-600">Title</th>
              <th className="p-4 font-semibold text-sm text-gray-600">Staff Assigned</th>
              <th className="p-4 font-semibold text-sm text-gray-600">Assigned By</th>
              <th className="p-4 font-semibold text-sm text-gray-600">Assigned At</th>
              <th className="p-4 font-semibold text-sm text-gray-600">Status</th>
            </tr>
          </thead>
          <tbody>
            {assignments.map(assignment => (
              <tr key={assignment.id} className="border-b hover:bg-gray-50">
                <td className="p-4 text-sm font-medium text-gray-900">{assignment.complaint_number}</td>
                <td className="p-4 text-sm text-gray-700">{assignment.complaint_title}</td>
                <td className="p-4 text-sm text-gray-700">{assignment.staff_name}</td>
                <td className="p-4 text-sm text-gray-700">{assignment.assigned_by_name}</td>
                <td className="p-4 text-sm text-gray-700">{new Date(assignment.assigned_at).toLocaleString()}</td>
                <td className="p-4 text-sm text-gray-700">
                  <span className="px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800">
                    {assignment.complaint_status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {assignments.length === 0 && (
          <div className="p-4 text-center text-gray-500">No assignments found.</div>
        )}
      </div>
    </div>
  );
};

export default AssignmentsPage;
