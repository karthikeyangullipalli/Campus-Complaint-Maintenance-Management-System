import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../../utils/api';

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
      const res = await api.get(`/complaints/${id}`);
      setTask(res.data.data);
      setNewStatus(res.data.data?.status || '');
    } catch (error) {
      console.error('Error fetching task:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      await api.put(`/complaints/${id}/status`, { new_status: newStatus, remarks });
      setRemarks('');
      fetchTask();
    } catch (error) {
      console.error('Error updating status:', error);
      alert(error.response?.data?.message || 'Error updating status');
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
            <div><span className="font-semibold text-gray-600">Priority:</span> {task.priority}</div>
            <div><span className="font-semibold text-gray-600">Date Filed:</span> {new Date(task.created_at).toLocaleString()}</div>
          </div>

          <div className="mb-6">
            <h3 className="font-semibold text-lg mb-2">Description</h3>
            <p className="text-gray-700 whitespace-pre-wrap">{task.description}</p>
          </div>

          {task.image_path && (
            <div className="mb-6">
              <h3 className="font-semibold text-lg mb-2">Attached Image</h3>
              <img 
                src={task.image_path} 
                alt="Task attachment" 
                className="max-h-80 rounded border shadow-sm object-contain"
              />
            </div>
          )}
        </div>

        {task.updates && task.updates.length > 0 && (
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="font-semibold text-lg mb-4">Task Updates & Remarks</h3>
            <div className="space-y-4">
              {task.updates.map((update, idx) => (
                <div key={idx} className="border-l-2 border-green-500 pl-4 py-1">
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
        <div className="bg-white rounded-lg shadow p-6 sticky top-6">
          <h2 className="text-lg font-bold text-gray-900 mb-4">Update Progress</h2>
          <form onSubmit={handleUpdate}>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
              <select 
                className="w-full p-2 border rounded text-sm bg-white"
                value={newStatus}
                onChange={(e) => setNewStatus(e.target.value)}
              >
                <option value="ASSIGNED">ASSIGNED</option>
                <option value="IN_PROGRESS">IN_PROGRESS</option>
                <option value="RESOLVED">RESOLVED</option>
              </select>
            </div>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">Work Remarks</label>
              <textarea 
                rows="4" 
                className="w-full p-2 border rounded text-sm"
                placeholder="Details of repair work completed or current issue..."
                value={remarks}
                onChange={(e) => setRemarks(e.target.value)}
              ></textarea>
            </div>

            <button type="submit" className="w-full py-2 bg-green-600 text-white font-medium rounded hover:bg-green-700">
              Submit Update
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default TaskDetail;
