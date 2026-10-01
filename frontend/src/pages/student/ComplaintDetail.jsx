import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../../utils/api';
import StatusBadge from '../../components/common/StatusBadge';
import PriorityBadge from '../../components/common/PriorityBadge';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import { formatDate } from '../../utils/helpers';
import { FiArrowLeft, FiMessageSquare } from 'react-icons/fi';

const ComplaintDetail = () => {
  const { id } = useParams();
  const [complaint, setComplaint] = useState(null);
  const [loading, setLoading] = useState(true);
  const [feedback, setFeedback] = useState('');
  const [rating, setRating] = useState(5);
  const [feedbackSubmitting, setFeedbackSubmitting] = useState(false);

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

  const handleFeedbackSubmit = async (e) => {
    e.preventDefault();
    setFeedbackSubmitting(true);
    try {
      await api.post(`/complaints/${id}/feedback`, { rating, comments: feedback });
      fetchComplaint(); // Refresh
    } catch (error) {
      console.error("Error submitting feedback", error);
    } finally {
      setFeedbackSubmitting(false);
    }
  };

  if (loading) return <LoadingSpinner />;
  if (!complaint) return <div className="p-6 text-center text-gray-500">Complaint not found</div>;

  return (
    <div>
      <div className="mb-6 flex items-center">
        <Link to="/student/complaints" className="text-gray-500 hover:text-gray-700 mr-4">
          <FiArrowLeft className="w-5 h-5" />
        </Link>
        <h1 className="text-2xl font-bold text-gray-900">Complaint Details</h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          {/* Main Info */}
          <div className="bg-white shadow-sm rounded-lg border border-gray-100 p-6">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h2 className="text-xl font-bold text-gray-900 mb-1">{complaint.title}</h2>
                <p className="text-sm text-gray-500">ID: #{complaint.id} • Filed on {formatDate(complaint.createdAt)}</p>
              </div>
              <div className="flex space-x-2">
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
          </div>

          {/* Feedback Form (if resolved and no feedback yet) */}
          {(complaint.status === 'RESOLVED' || complaint.status === 'CLOSED') && !complaint.feedback && (
            <div className="bg-white shadow-sm rounded-lg border border-gray-100 p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
                <FiMessageSquare className="mr-2" /> Provide Feedback
              </h3>
              <form onSubmit={handleFeedbackSubmit}>
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-1">Rating (1-5)</label>
                  <select
                    value={rating}
                    onChange={(e) => setRating(Number(e.target.value))}
                    className="w-full sm:w-32 border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary sm:text-sm py-2 px-3 border"
                  >
                    {[5,4,3,2,1].map(num => <option key={num} value={num}>{num} Stars</option>)}
                  </select>
                </div>
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-1">Comments</label>
                  <textarea
                    value={feedback}
                    onChange={(e) => setFeedback(e.target.value)}
                    rows="3"
                    className="w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary sm:text-sm py-2 px-3 border"
                    placeholder="How was the service?"
                  ></textarea>
                </div>
                <button
                  type="submit"
                  disabled={feedbackSubmitting}
                  className="px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary hover:bg-blue-800 disabled:opacity-50"
                >
                  Submit Feedback
                </button>
              </form>
            </div>
          )}

          {/* Display existing feedback */}
          {complaint.feedback && (
             <div className="bg-blue-50 shadow-sm rounded-lg border border-blue-100 p-6">
               <h3 className="text-lg font-medium text-blue-900 mb-2">Your Feedback</h3>
               <p className="text-sm text-blue-800 font-bold mb-1">Rating: {complaint.feedback.rating}/5</p>
               <p className="text-sm text-blue-800">{complaint.feedback.comments}</p>
             </div>
          )}
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
                              Status changed to <StatusBadge status={event.status} />
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
    </div>
  );
};

export default ComplaintDetail;
