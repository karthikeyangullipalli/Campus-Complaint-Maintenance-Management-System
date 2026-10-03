import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../../utils/api';

const ComplaintList = () => {
  const [complaints, setComplaints] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchComplaints();
  }, []);

  const fetchComplaints = async () => {
    try {
      const res = await api.get('/complaints');
      setComplaints(res.data.data || []);
    } catch (error) {
      console.error('Error fetching complaints:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredComplaints = complaints.filter(c => 
    c.title?.toLowerCase().includes(searchTerm.toLowerCase()) || 
    c.complaint_number?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-800">My Complaints</h1>
        <Link to="/student/complaints/new" className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
          New Complaint
        </Link>
      </div>

      <div className="mb-4">
        <input 
          type="text" 
          placeholder="Search by title or number..." 
          className="w-full md:w-1/3 p-2 border rounded"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
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
                  <td className="p-4 text-sm text-gray-700">{complaint.category_name}</td>
                  <td className="p-4 text-sm text-gray-700">
                    <span className="px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800">
                      {complaint.status}
                    </span>
                  </td>
                  <td className="p-4 text-sm text-gray-700">{new Date(complaint.created_at).toLocaleDateString()}</td>
                  <td className="p-4 text-sm text-blue-600 hover:underline">
                    <Link to={`/student/complaints/${complaint.id}`}>View</Link>
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

export default ComplaintList;
