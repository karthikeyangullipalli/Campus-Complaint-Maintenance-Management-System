import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';

const AdminComplaintDetail = () => {
  const { id } = useParams();
  const [complaint, setComplaint] = useState(null);
  const [loading, setLoading] = useState(true);
  const [staffList, setStaffList] = useState([]);
  
  // Action states
  const [remarks, setRemarks] = useState('');
  const [selectedStaff, setSelectedStaff] = useState('');
  
  useEffect(() => {
    fetchComplaint();
    fetchStaff();
  }, [id]);

  const fetchComplaint = async () => {
    try {
      const res = await axios.get(`/api/complaints/${id}`);
      setComplaint(res.data.data);
    } catch (error) {
      console.error('Error fetching complaint:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchStaff = async () => {
    try {
      const res = await axios.get('/api/users?role=MAINTENANCE');
      setStaffList(res.data.data || []);
    } catch (error) {
      console.error('Error fetching staff:', error);
    }
  };

  const handleStatusChange = async (new_status) => {
    try {
      await axios.put(`/api/complaints/${id}/status`, { new_status, remarks });
      setRemarks('');
      fetchComplaint();
    } catch (error) {
      console.error('Error updating status:', error);
    }
  };

  const handleAssign = async () => {
    if (!selectedStaff) return;
    try {
      await axios.post(`/api/complaints/${id}/assign`, { 
        maintenance_staff_id: selectedStaff, 
        notes: remarks 
      });
      setRemarks('');
      setSelectedStaff('');
      fetchComplaint();
    } catch (error) {
      console.error('Error assigning staff:', error);
    }
  };

  if (loading) return <div className="p-6">Loading...</div>;
  if (!complaint) return <div className="p-6">Complaint not found.</div>;

  return (
    <div className="p-6 max-w-5xl mx-auto flex flex-col md:flex-row gap-6">
      <div className="flex-1">
        <Link to="/admin/complaints" className="text-blue-600 hover:underline mb-4 inline-block">&larr; Back</Link>
        
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">{complaint.title}</h1>
              <p className="text-sm text-gray-500 mt-1">#{complaint.complaint_number} • By: {complaint.user_name}</p>
            </div>
            <span className="px-3 py-1 text-sm font-semibold rounded-full bg-indigo-100 text-indigo-800">
              {complaint.status}
            </span>
          </div>

          <div className="grid grid-cols-2 gap-4 text-sm mb-6">
            <div><span className="font-semibold">Category:</span> {complaint.category_name}</div>
            <div><span className="font-semibold">Location:</span> {complaint.location_name}</div>
            <div><span className="font-semibold">Date:</span> {new Date(complaint.created_at).toLocaleString()}</div>
          </div>
          <div className="mb-4">
            <h3 className="font-semibold text-lg mb-2">Description</h3>
            <p className="text-gray-700 whitespace-pre-wrap">{complaint.description}</p>
          </div>
        </div>

        {/* History */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="font-semibold text-lg mb-4">History</h3>
          <div className="space-y-4">
            {(complaint.updates || []).map((update, idx) => (
              <div key={idx} className="border-l-2 border-gray-300 pl-4 py-1">
                <p className="text-sm text-gray-800">
                  <span className="font-semibold">{update.updated_by_name}</span>: 
                  <span className="px-1 text-gray-500">{update.old_status} &rarr; {update.new_status}</span>
                </p>
                {update.remarks && <p className="text-sm text-gray-600 mt-1">"{update.remarks}"</p>}
                <p className="text-xs text-gray-400 mt-1">{new Date(update.created_at).toLocaleString()}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Admin Actions Sidebar */}
      <div className="w-full md:w-80 space-y-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="font-semibold text-lg mb-4">Actions</h3>
          
          <div className="mb-4">
            <label className="block text-sm text-gray-700 mb-1">Remarks / Notes</label>
            <textarea 
              className="w-full p-2 border rounded text-sm" 
              rows="3" 
              value={remarks}
              onChange={(e) => setRemarks(e.target.value)}
              placeholder="Add notes for this action..."
            />
          </div>

          <div className="space-y-2">
            {complaint.status === 'PENDING' && (
              <>
                <button onClick={() => handleStatusChange('VERIFIED')} className="w-full py-2 bg-green-600 text-white rounded hover:bg-green-700">Verify Complaint</button>
                <button onClick={() => handleStatusChange('REJECTED')} className="w-full py-2 bg-red-600 text-white rounded hover:bg-red-700">Reject Complaint</button>
              </>
            )}
            
            {(complaint.status === 'VERIFIED' || complaint.status === 'REOPENED') && (
              <div className="mt-4 pt-4 border-t">
                <label className="block text-sm text-gray-700 mb-1">Assign to Maintenance</label>
                <select 
                  className="w-full p-2 border rounded text-sm mb-2"
                  value={selectedStaff}
                  onChange={(e) => setSelectedStaff(e.target.value)}
                >
                  <option value="">Select Staff...</option>
                  {staffList.map(staff => (
                    <option key={staff.id} value={staff.id}>{staff.name} - {staff.department || 'General'}</option>
                  ))}
                </select>
                <button 
                  onClick={handleAssign} 
                  disabled={!selectedStaff}
                  className="w-full py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
                >
                  Assign Task
                </button>
              </div>
            )}

            {complaint.status === 'RESOLVED' && (
              <button onClick={() => handleStatusChange('CLOSED')} className="w-full py-2 bg-gray-800 text-white rounded hover:bg-gray-900 mt-4">Close Complaint</button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminComplaintDetail;
