import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../../utils/api';
import StatusBadge from '../../components/common/StatusBadge';
import PriorityBadge from '../../components/common/PriorityBadge';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import { formatDate } from '../../utils/helpers';
import { FiArrowLeft, FiCheckCircle, FiPlay } from 'react-icons/fi';

const TaskDetail = () => {
  const { id } = useParams();
  const [task, setTask] = useState(null);
  const [loading, setLoading] = useState(true);
  const [remarks, setRemarks] = useState('');
  const [updating, setUpdating] = useState(false);

  useEffect(() => {
    fetchTask();
  }, [id]);

  const fetchTask = async () => {
    try {
      const res = await api.get(`/complaints/${id}`);
      setTask(res.data);
    } catch (error) {
      console.error("Error fetching task", error);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateStatus = async (status) => {
    setUpdating(true);
    try {
      await api.patch(`/complaints/${id}/status`, { status, remarks });
      setRemarks('');
      fetchTask();
    } catch (error) {
      console.error("Error updating status", error);
    } finally {
      setUpdating(false);
    }
  };

  if (loading) return <LoadingSpinner />;
  if (!task) return <div className="p-6 text-center text-gray-500">Task not found</div>;

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <div className="flex items-center">
          <Link to="/maintenance/tasks" className="text-gray-500 hover:text-gray-700 mr-4">
            <FiArrowLeft className="w-5 h-5" />
          </Link>
          <h1 className="text-2xl font-bold text-gray-900">Task #{task.id}</h1>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white shadow-sm rounded-lg border border-gray-100 p-6">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h2 className="text-xl font-bold text-gray-900 mb-1">{task.title}</h2>
                <p className="text-sm text-gray-500">Reported by {task.user?.name}</p>
              </div>
              <div className="flex flex-col items-end space-y-2">
                <PriorityBadge priority={task.priority} />
                <StatusBadge status={task.status} />
              </div>
            </div>

            <div className="py-4 border-t border-b border-gray-100 my-4 grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm font-medium text-gray-500">Location</p>
                <p className="mt-1 text-sm text-gray-900">{task.location?.name || 'N/A'}</p>
                <p className="text-xs text-gray-500">{task.location?.building}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500">Category</p>
                <p className="mt-1 text-sm text-gray-900">{task.category?.name || 'N/A'}</p>
              </div>
            </div>

            <div>
              <p className="text-sm font-medium text-gray-500 mb-2">Description</p>
              <p className="text-sm text-gray-900 whitespace-pre-wrap">{task.description}</p>
            </div>
          </div>
          
          {/* Action Area */}
          {(task.status === 'ASSIGNED' || task.status === 'IN_PROGRESS') && (
            <div className="bg-white shadow-sm rounded-lg border border-gray-100 p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Update Task Status</h3>
              
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Work Notes / Remarks</label>
                <textarea
                  className="w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary sm:text-sm py-2 px-3 border"
                  rows="3"
                  placeholder="Enter details about work done or what's needed next..."
                  value={remarks}
                  onChange={(e) => setRemarks(e.target.value)}
                ></textarea>
              </div>

              <div className="flex space-x-3">
                {task.status === 'ASSIGNED' && (
                  <button 
                    onClick={() => handleUpdateStatus('IN_PROGRESS')}
                    disabled={updating}
                    className="flex-1 bg-yellow-500 hover:bg-yellow-600 text-white py-2 px-4 rounded-md font-medium flex justify-center items-center"
                  >
                    <FiPlay className="mr-2" /> Start Work (Mark In Progress)
                  </button>
                )}
                {task.status === 'IN_PROGRESS' && (
                  <button 
                    onClick={() => handleUpdateStatus('RESOLVED')}
                    disabled={updating}
                    className="flex-1 bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-md font-medium flex justify-center items-center"
                  >
                    <FiCheckCircle className="mr-2" /> Mark as Resolved
                  </button>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Sidebar: History */}
        <div className="space-y-6">
          <div className="bg-white shadow-sm rounded-lg border border-gray-100 p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Task History</h3>
            <div className="flow-root">
              <ul className="-mb-8">
                {task.history && task.history.map((event, eventIdx) => (
                  <li key={event.id}>
                    <div className="relative pb-8">
                      {eventIdx !== task.history.length - 1 ? (
                        <span className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200" aria-hidden="true" />
                      ) : null}
                      <div className="relative flex space-x-3">
                        <div>
                          <span className="h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center ring-8 ring-white">
                            <div className="w-2.5 h-2.5 bg-primary rounded-full" />
                          </span>
                        </div>
                        <div className="min-w-0 flex-1 pt-1.5 flex flex-col">
                          <div className="flex justify-between space-x-4">
                            <p className="text-sm text-gray-500">
                              <StatusBadge status={event.status} />
                            </p>
                            <div className="text-right text-xs whitespace-nowrap text-gray-500">
                              {formatDate(event.createdAt)}
                            </div>
                          </div>
                          {event.remarks && (
                            <p className="mt-2 text-sm text-gray-900 bg-gray-50 p-2 rounded border border-gray-100">{event.remarks}</p>
                          )}
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
    </div>
  );
};

export default TaskDetail;
