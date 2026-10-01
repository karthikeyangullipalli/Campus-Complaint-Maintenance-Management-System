import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../../utils/api';
import StatusBadge from '../../components/common/StatusBadge';
import PriorityBadge from '../../components/common/PriorityBadge';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import { formatDate } from '../../utils/helpers';
import { FiSearch, FiFilter } from 'react-icons/fi';

const ComplaintList = () => {
  const [complaints, setComplaints] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  useEffect(() => {
    fetchComplaints();
  }, [statusFilter]);

  const fetchComplaints = async () => {
    setLoading(true);
    try {
      const res = await api.get(`/complaints${statusFilter ? `?status=${statusFilter}` : ''}`);
      setComplaints(res.data.complaints || []);
    } catch (error) {
      console.error("Error fetching complaints", error);
    } finally {
      setLoading(false);
    }
  };

  const filteredComplaints = complaints.filter(c => 
    c.title.toLowerCase().includes(searchTerm.toLowerCase()) || 
    c.id.toString().includes(searchTerm)
  );

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">My Complaints</h1>
        <Link to="/student/complaints/new" className="bg-primary hover:bg-blue-800 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors">
          File New Complaint
        </Link>
      </div>

      <div className="bg-white shadow-sm rounded-lg border border-gray-100 mb-6 p-4 flex flex-col sm:flex-row gap-4 justify-between">
        <div className="relative flex-1 max-w-md">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <FiSearch className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            className="focus:ring-primary focus:border-primary block w-full pl-10 sm:text-sm border-gray-300 rounded-md py-2 border"
            placeholder="Search by title or ID..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <div className="flex items-center space-x-2">
          <FiFilter className="text-gray-400" />
          <select 
            className="border-gray-300 rounded-md text-sm py-2 pl-3 pr-10 focus:ring-primary focus:border-primary border"
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <option value="">All Statuses</option>
            <option value="NEW">New</option>
            <option value="IN_PROGRESS">In Progress</option>
            <option value="RESOLVED">Resolved</option>
            <option value="CLOSED">Closed</option>
          </select>
        </div>
      </div>

      {loading ? <LoadingSpinner /> : (
        <div className="bg-white shadow-sm rounded-lg border border-gray-100 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Title</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Location</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Priority</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredComplaints.length === 0 ? (
                  <tr>
                    <td colSpan="7" className="px-6 py-4 text-center text-sm text-gray-500">No complaints found.</td>
                  </tr>
                ) : (
                  filteredComplaints.map(complaint => (
                    <tr key={complaint.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">#{complaint.id}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <Link to={`/student/complaints/${complaint.id}`} className="text-sm font-medium text-primary hover:underline">
                          {complaint.title}
                        </Link>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{complaint.category?.name || 'N/A'}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{complaint.location?.name || 'N/A'}</td>
                      <td className="px-6 py-4 whitespace-nowrap"><PriorityBadge priority={complaint.priority} /></td>
                      <td className="px-6 py-4 whitespace-nowrap"><StatusBadge status={complaint.status} /></td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{formatDate(complaint.createdAt)}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default ComplaintList;
