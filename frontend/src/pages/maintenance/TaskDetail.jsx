import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';

const TaskDetail = () => {
  const { id } = useParams();
  const [task, setTask] = useState(null);
  const [loading, setLoading] = useState(true);
  const [remarks, setRemarks] = useState('');
  const [newStatus, setNewStatus] = useState('');

  useEffect(() => {
    fetchTask();
  }, [id]);

  const fetchTask = async () => {
    try {
      const res = await axios.get(`/api/complaints/${id}`);
      setTask(res.data.data);
      setNewStatus(res.data.data.status);
    } catch (error) {
      console.error('Error fetching task:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      await axios.put(`/api/complaints/${id}/status`, { new_status: newStatus, remarks });
      setRemarks('');
      fetchTask();
    } catch (error) {
      console.error('Error updating status:', error);
    }
  };

  if (loading) return <div className="p-6">Loading...</div>;
  if (!task) return <div className="p-6">Task not found.</div>;

  return (
    <div className="p-6 max-w-5xl mx-auto flex flex-col md:flex-row gap-6">
      <div className="flex-1">
        <Link to="/maintenance/tasks" className="text-blue-600 hover:underline mb-4 inline-block">&larr; Back to Tasks</Link>
        
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">{task.title}</h1>
              <p className="text-sm text-gray-500 mt-1">Complaint #{task.complaint_number}</p>
            </div>
            <span className="px-3 py-1 text-sm font-semibold rounded-full bg-blue-100 text-blue-800">
              {task.status}
            </span>
          </div>

          <div className="grid grid-cols-2 gap-4 text-sm mb-6">
            <div><span className="font-semibold text-gray-600">Category:</span> {task.category_name}</div>
            <div><span className="font-semibold text-gray-600">Location:</span> {task.location_name}</div>
            <div><span className="font-semibold text-gray-600">Priority:</span> {task.priority || 'Normal'}</div>
            <div><span className="font-semibold text-gray-600">Date Filed:</span> {new Date(task.created_at).toLocaleString()}</div>
          </div>

          <div className="mb-6">
            <h3 className="font-semibold text-lg mb-2">Description</h3>
            <p className="text-gray-700 whitespace-pre-wrap">{task.description}</p>
          </div>
        </div>

        {task.updates && task.updates.length > 0 && (
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="font-semibold text-lg mb-4">Task History</h3>
            <div className="space-y-4">
              {task.updates.map((update, idx) => (
                <div key={idx} className="border-l-2 border-blue-500 pl-4 py-1">
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

      <div className="w-full md:w-80">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="font-semibold text-lg mb-4">Update Status</h3>
          <form onSubmit={handleUpdate}>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">New Status</label>
              <select 
                className="w-full p-2 border rounded text-sm"
                value={newStatus}
                onChange={(e) => setNewStatus(e.target.value)}
              >
                <option value="ASSIGNED">ASSIGNED</option>
                <option value="IN_PROGRESS">IN_PROGRESS</option>
                <option value="RESOLVED">RESOLVED</option>
              </select>
            </div>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">Remarks / Fix Details</label>
              <textarea 
                rows="3" 
                required={newStatus === 'RESOLVED'}
                className="w-full p-2 border rounded text-sm"
                value={remarks}
                onChange={(e) => setRemarks(e.target.value)}
                placeholder="Describe what was done..."
              ></textarea>
            </div>
            <button 
              type="submit" 
              className="w-full py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Update Task
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default TaskDetail;
