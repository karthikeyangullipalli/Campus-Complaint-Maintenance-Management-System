import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const AdminComplaints = () => {
  const [complaints, setComplaints] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  useEffect(() => {
    fetchComplaints();
  }, []);

  const fetchComplaints = async () => {
    try {
      const res = await axios.get('/api/complaints');
      setComplaints(res.data.data || []);
    } catch (error) {
      console.error('Error fetching complaints:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredComplaints = complaints.filter(c => {
    const matchesSearch = c.title?.toLowerCase().includes(searchTerm.toLowerCase()) || 
                          c.complaint_number?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          c.user_name?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === '' || c.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Manage Complaints</h1>

      <div className="flex flex-col md:flex-row gap-4 mb-6">
        <input 
          type="text" 
          placeholder="Search by title, number, or user..." 
          className="w-full md:w-1/2 p-2 border rounded"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <select 
          className="w-full md:w-1/4 p-2 border rounded bg-white"
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
        >
          <option value="">All Statuses</option>
          <option value="PENDING">PENDING</option>
          <option value="VERIFIED">VERIFIED</option>
          <option value="ASSIGNED">ASSIGNED</option>
          <option value="IN_PROGRESS">IN_PROGRESS</option>
          <option value="RESOLVED">RESOLVED</option>
          <option value="CLOSED">CLOSED</option>
          <option value="REJECTED">REJECTED</option>
          <option value="REOPENED">REOPENED</option>
        </select>
      </div>

      {loading ? (
        <div>Loading...</div>
      ) : (
        <div className="bg-white rounded shadow overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-gray-50 border-b">
                <th className="p-4 font-semibold text-sm text-gray-600">Complaint #</th>
                <th className="p-4 font-semibold text-sm text-gray-600">Title</th>
                <th className="p-4 font-semibold text-sm text-gray-600">User</th>
                <th className="p-4 font-semibold text-sm text-gray-600">Category</th>
                <th className="p-4 font-semibold text-sm text-gray-600">Status</th>
                <th className="p-4 font-semibold text-sm text-gray-600">Date</th>
                <th className="p-4 font-semibold text-sm text-gray-600">Action</th>
              </tr>
            </thead>
            <tbody>
              {filteredComplaints.map(complaint => (
                <tr key={complaint.id} className="border-b hover:bg-gray-50">
                  <td className="p-4 text-sm font-medium text-gray-900">{complaint.complaint_number}</td>
                  <td className="p-4 text-sm text-gray-700">{complaint.title}</td>
                  <td className="p-4 text-sm text-gray-700">{complaint.user_name}</td>
                  <td className="p-4 text-sm text-gray-700">{complaint.category_name}</td>
                  <td className="p-4 text-sm text-gray-700">
                    <span className="px-2 py-1 text-xs rounded-full bg-indigo-100 text-indigo-800">
                      {complaint.status}
                    </span>
                  </td>
                  <td className="p-4 text-sm text-gray-700">{new Date(complaint.created_at).toLocaleDateString()}</td>
                  <td className="p-4 text-sm text-blue-600 hover:underline">
                    <Link to={`/admin/complaints/${complaint.id}`}>Manage</Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {filteredComplaints.length === 0 && (
            <div className="p-4 text-center text-gray-500">No complaints found.</div>
          )}
        </div>
      )}
    </div>
  );
};

export default AdminComplaints;
