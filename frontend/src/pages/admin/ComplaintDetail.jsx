import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import api from '../../utils/api';
import StatusBadge from '../../components/common/StatusBadge';
import PriorityBadge from '../../components/common/PriorityBadge';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import { formatDate } from '../../utils/helpers';
import { FiArrowLeft, FiCheck, FiX, FiUserPlus } from 'react-icons/fi';
import Modal from '../../components/common/Modal';

const AdminComplaintDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [complaint, setComplaint] = useState(null);
  const [loading, setLoading] = useState(true);
  const [staffList, setStaffList] = useState([]);
  
  // Modals state
  const [isAssignModalOpen, setAssignModalOpen] = useState(false);
  const [selectedStaff, setSelectedStaff] = useState('');
  
  // Remarks state
  const [remarks, setRemarks] = useState('');

  useEffect(() => {
    fetchComplaint();
  }, [id]);

  const fetchComplaint = async () => {
    try {
      const res = await api.get(`/complaints/${id}`);
      setComplaint(res.data);
    } catch (error) {
      console.error("Error fetching complaint", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchStaff = async () => {
    try {
      const res = await api.get('/users?role=MAINTENANCE_STAFF');
      setStaffList(res.data || []);
    } catch (error) {
      console.error("Error fetching staff", error);
    }
  };

  const handleUpdateStatus = async (status) => {
    try {
      await api.patch(`/complaints/${id}/status`, { status, remarks });
      setRemarks('');
      fetchComplaint();
    } catch (error) {
      console.error("Error updating status", error);
    }
  };

  const handleAssign = async (e) => {
    e.preventDefault();
    if (!selectedStaff) return;
    try {
      await api.post(`/complaints/${id}/assign`, { assigneeId: selectedStaff });
      setAssignModalOpen(false);
      fetchComplaint();
    } catch (error) {
      console.error("Error assigning complaint", error);
    }
  };

  if (loading) return <LoadingSpinner />;
  if (!complaint) return <div className="p-6 text-center text-gray-500">Complaint not found</div>;

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <div className="flex items-center">
          <Link to="/admin/complaints" className="text-gray-500 hover:text-gray-700 mr-4">
            <FiArrowLeft className="w-5 h-5" />
          </Link>
          <h1 className="text-2xl font-bold text-gray-900">Manage Complaint #{complaint.id}</h1>
        </div>
        
        {/* Admin Actions */}
        <div className="flex space-x-2">
          {complaint.status === 'NEW' && (
            <>
              <button onClick={() => handleUpdateStatus('VERIFIED')} className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded-md text-sm font-medium flex items-center">
                <FiCheck className="mr-1" /> Verify
              </button>
              <button onClick={() => handleUpdateStatus('REJECTED')} className="bg-red-600 hover:bg-red-700 text-white px-3 py-2 rounded-md text-sm font-medium flex items-center">
                <FiX className="mr-1" /> Reject
              </button>
            </>
          )}
          {(complaint.status === 'VERIFIED' || complaint.status === 'NEW') && (
            <button onClick={() => { fetchStaff(); setAssignModalOpen(true); }} className="bg-purple-600 hover:bg-purple-700 text-white px-3 py-2 rounded-md text-sm font-medium flex items-center">
              <FiUserPlus className="mr-1" /> Assign Staff
            </button>
          )}
          {complaint.status === 'RESOLVED' && (
            <button onClick={() => handleUpdateStatus('CLOSED')} className="bg-green-600 hover:bg-green-700 text-white px-3 py-2 rounded-md text-sm font-medium flex items-center">
              <FiCheck className="mr-1" /> Close Complaint
            </button>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white shadow-sm rounded-lg border border-gray-100 p-6">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h2 className="text-xl font-bold text-gray-900 mb-1">{complaint.title}</h2>
                <p className="text-sm text-gray-500">Reported by {complaint.user?.name} ({complaint.user?.email})</p>
              </div>
              <div className="flex flex-col items-end space-y-2">
                <PriorityBadge priority={complaint.priority} />
                <StatusBadge status={complaint.status} />
              </div>
            </div>

            <div className="py-4 border-t border-b border-gray-100 my-4 grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm font-medium text-gray-500">Category</p>
                <p className="mt-1 text-sm text-gray-900">{complaint.category?.name || 'N/A'}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500">Location</p>
                <p className="mt-1 text-sm text-gray-900">{complaint.location?.name || 'N/A'}</p>
              </div>
            </div>

            <div>
              <p className="text-sm font-medium text-gray-500 mb-2">Description</p>
              <p className="text-sm text-gray-900 whitespace-pre-wrap">{complaint.description}</p>
            </div>
            
            {complaint.assignment && (
              <div className="mt-6 bg-purple-50 p-4 rounded-md border border-purple-100">
                <h3 className="text-sm font-bold text-purple-900 mb-1">Current Assignment</h3>
                <p className="text-sm text-purple-800">Assigned to: {complaint.assignment.assignee?.name}</p>
                <p className="text-sm text-purple-800">Assigned on: {formatDate(complaint.assignment.createdAt)}</p>
              </div>
            )}
          </div>
          
          <div className="bg-white shadow-sm rounded-lg border border-gray-100 p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Add Remarks (Optional for Status Change)</h3>
            <textarea
              className="w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary sm:text-sm py-2 px-3 border"
              rows="3"
              placeholder="Enter remarks for the next status update..."
              value={remarks}
              onChange={(e) => setRemarks(e.target.value)}
            ></textarea>
          </div>
        </div>

        {/* Sidebar: History */}
        <div className="space-y-6">
          <div className="bg-white shadow-sm rounded-lg border border-gray-100 p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Updates & History</h3>
            <div className="flow-root">
              <ul className="-mb-8">
                {complaint.history && complaint.history.map((event, eventIdx) => (
                  <li key={event.id}>
                    <div className="relative pb-8">
                      {eventIdx !== complaint.history.length - 1 ? (
                        <span className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200" aria-hidden="true" />
                      ) : null}
                      <div className="relative flex space-x-3">
                        <div>
                          <span className="h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center ring-8 ring-white">
                            <div className="w-2.5 h-2.5 bg-primary rounded-full" />
                          </span>
                        </div>
                        <div className="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4">
                          <div>
                            <p className="text-sm text-gray-500">
                              <StatusBadge status={event.status} /> by {event.updatedBy?.name}
                            </p>
                            {event.remarks && (
                              <p className="mt-1 text-sm text-gray-900">{event.remarks}</p>
                            )}
                          </div>
                          <div className="text-right text-xs whitespace-nowrap text-gray-500">
                            {formatDate(event.createdAt)}
                          </div>
                        </div>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>

      <Modal isOpen={isAssignModalOpen} onClose={() => setAssignModalOpen(false)} title="Assign Maintenance Staff">
        <form onSubmit={handleAssign}>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">Select Staff</label>
            <select
              required
              className="w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary sm:text-sm py-2 px-3 border"
              value={selectedStaff}
              onChange={(e) => setSelectedStaff(e.target.value)}
            >
              <option value="">-- Select Staff --</option>
              {staffList.map(staff => (
                <option key={staff.id} value={staff.id}>{staff.name} ({staff.department || 'Maintenance'})</option>
              ))}
            </select>
          </div>
          <div className="flex justify-end space-x-3 mt-5">
            <button type="button" onClick={() => setAssignModalOpen(false)} className="px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
              Cancel
            </button>
            <button type="submit" className="px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary hover:bg-blue-800">
              Assign
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default AdminComplaintDetail;
