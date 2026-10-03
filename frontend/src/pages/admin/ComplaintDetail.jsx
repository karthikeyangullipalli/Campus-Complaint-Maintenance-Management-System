import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../../utils/api';

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
      const res = await api.get(`/complaints/${id}`);
      setComplaint(res.data.data);
    } catch (error) {
      console.error('Error fetching complaint:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchStaff = async () => {
    try {
      const res = await api.get('/users?role=MAINTENANCE');
      setStaffList(res.data.data || []);
    } catch (error) {
      console.error('Error fetching staff:', error);
    }
  };

  const handleStatusChange = async (new_status) => {
    try {
      await api.put(`/complaints/${id}/status`, { new_status, remarks });
      setRemarks('');
      fetchComplaint();
    } catch (error) {
      console.error('Error updating status:', error);
      alert(error.response?.data?.message || 'Failed to update status');
    }
  };

  const handleAssign = async () => {
    if (!selectedStaff) return;
    try {
      await api.post(`/complaints/${id}/assign`, { 
        maintenance_staff_id: selectedStaff, 
        notes: remarks 
      });
      setRemarks('');
      setSelectedStaff('');
      fetchComplaint();
    } catch (error) {
      console.error('Error assigning staff:', error);
      alert(error.response?.data?.message || 'Failed to assign staff');
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
              <p className="text-sm text-gray-500 mt-1">Complaint #{complaint.complaint_number}</p>
            </div>
            <span className="px-3 py-1 text-sm font-semibold rounded-full bg-blue-100 text-blue-800">
              {complaint.status}
            </span>
          </div>

          <div className="grid grid-cols-2 gap-4 text-sm mb-6">
            <div><span className="font-semibold text-gray-600">Reported By:</span> {complaint.user_name}</div>
            <div><span className="font-semibold text-gray-600">Category:</span> {complaint.category_name}</div>
            <div><span className="font-semibold text-gray-600">Location:</span> {complaint.location_name}</div>
            <div><span className="font-semibold text-gray-600">Priority:</span> {complaint.priority}</div>
            <div><span className="font-semibold text-gray-600">Assigned Staff:</span> {complaint.assigned_staff || 'None'}</div>
            <div><span className="font-semibold text-gray-600">Date Filed:</span> {new Date(complaint.created_at).toLocaleString()}</div>
          </div>

          <div className="mb-6">
            <h3 className="font-semibold text-lg mb-2">Description</h3>
            <p className="text-gray-700 whitespace-pre-wrap">{complaint.description}</p>
          </div>

          {complaint.image_path && (
            <div className="mb-6">
              <h3 className="font-semibold text-lg mb-2">Attached Image</h3>
              <img 
                src={complaint.image_path} 
                alt="Complaint attachment" 
                className="max-h-80 rounded border shadow-sm object-contain"
              />
            </div>
          )}
        </div>

        {/* History */}
        {complaint.updates && complaint.updates.length > 0 && (
          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <h3 className="font-semibold text-lg mb-4">Audit Trail</h3>
            <div className="space-y-4">
              {complaint.updates.map((update, idx) => (
                <div key={idx} className="border-l-2 border-indigo-500 pl-4 py-1">
                  <p className="text-sm text-gray-800">
                    <span className="font-semibold">{update.updated_by_name || 'System'}</span> changed status to 
                    <span className="font-semibold px-1">{update.new_status}</span>
                  </p>
                  {update.remarks && <p className="text-sm text-gray-600 mt-1 italic">"{update.remarks}"</p>}
                  <p className="text-xs text-gray-400 mt-1">{new Date(update.created_at).toLocaleString()}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Admin Action Sidebar */}
      <div className="w-full md:w-80">
        <div className="bg-white rounded-lg shadow p-6 sticky top-6">
          <h2 className="text-lg font-bold text-gray-900 mb-4">Admin Actions</h2>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">Remarks</label>
            <textarea 
              rows="3" 
              className="w-full p-2 border rounded text-sm"
              placeholder="Add verification, rejection, or closure notes..."
              value={remarks}
              onChange={(e) => setRemarks(e.target.value)}
            ></textarea>
          </div>

          <div className="space-y-3">
            {complaint.status === 'NEW' && (
              <>
                <button 
                  onClick={() => handleStatusChange('VERIFIED')}
                  className="w-full py-2 bg-blue-600 text-white font-medium rounded hover:bg-blue-700"
                >
                  Verify Complaint
                </button>
                <button 
                  onClick={() => handleStatusChange('REJECTED')}
                  className="w-full py-2 bg-red-600 text-white font-medium rounded hover:bg-red-700"
                >
                  Reject Complaint
                </button>
              </>
            )}

            {(complaint.status === 'VERIFIED' || complaint.status === 'REOPENED') && (
              <div className="pt-2 border-t">
                <label className="block text-sm font-medium text-gray-700 mb-1">Assign Maintenance Staff</label>
                <select 
                  className="w-full p-2 border rounded text-sm mb-3 bg-white"
                  value={selectedStaff}
                  onChange={(e) => setSelectedStaff(e.target.value)}
                >
                  <option value="">Select Staff</option>
                  {staffList.map(staff => (
                    <option key={staff.id} value={staff.id}>{staff.name} ({staff.email})</option>
                  ))}
                </select>
                <button 
                  onClick={handleAssign}
                  disabled={!selectedStaff}
                  className="w-full py-2 bg-indigo-600 text-white font-medium rounded hover:bg-indigo-700 disabled:opacity-50"
                >
                  Assign Staff
                </button>
              </div>
            )}

            {complaint.status === 'RESOLVED' && (
              <button 
                onClick={() => handleStatusChange('CLOSED')}
                className="w-full py-2 bg-green-600 text-white font-medium rounded hover:bg-green-700"
              >
                Close Complaint
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminComplaintDetail;
