import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';

const ComplaintDetail = () => {
  const { id } = useParams();
  const [complaint, setComplaint] = useState(null);
  const [loading, setLoading] = useState(true);
  const [feedback, setFeedback] = useState({ rating: 5, comments: '' });
  const [feedbackSubmitting, setFeedbackSubmitting] = useState(false);

  useEffect(() => {
    fetchComplaint();
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

  const handleFeedbackSubmit = async (e) => {
    e.preventDefault();
    setFeedbackSubmitting(true);
    try {
      await axios.post(`/api/complaints/${id}/feedback`, feedback);
      fetchComplaint(); // Refresh
    } catch (error) {
      console.error('Error submitting feedback:', error);
    } finally {
      setFeedbackSubmitting(false);
    }
  };

  if (loading) return <div className="p-6">Loading...</div>;
  if (!complaint) return <div className="p-6">Complaint not found.</div>;

  const needsFeedback = (complaint.status === 'RESOLVED' || complaint.status === 'CLOSED') && !complaint.feedback_id;

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <Link to="/student/complaints" className="text-blue-600 hover:underline mb-4 inline-block">&larr; Back to List</Link>
      
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
          <div><span className="font-semibold text-gray-600">Category:</span> {complaint.category_name}</div>
          <div><span className="font-semibold text-gray-600">Location:</span> {complaint.location_name}</div>
          <div><span className="font-semibold text-gray-600">Priority:</span> {complaint.priority || 'Normal'}</div>
          <div><span className="font-semibold text-gray-600">Date Filed:</span> {new Date(complaint.created_at).toLocaleString()}</div>
          <div><span className="font-semibold text-gray-600">Last Updated:</span> {new Date(complaint.updated_at).toLocaleString()}</div>
        </div>

        <div className="mb-6">
          <h3 className="font-semibold text-lg mb-2">Description</h3>
          <p className="text-gray-700 whitespace-pre-wrap">{complaint.description}</p>
        </div>
      </div>

      {complaint.updates && complaint.updates.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h3 className="font-semibold text-lg mb-4">Complaint History</h3>
          <div className="space-y-4">
            {complaint.updates.map((update, idx) => (
              <div key={idx} className="border-l-2 border-blue-500 pl-4 py-1">
                <p className="text-sm text-gray-800">
                  <span className="font-semibold">{update.updated_by_name || 'System'}</span> changed status from 
                  <span className="font-semibold px-1">{update.old_status}</span> to 
                  <span className="font-semibold px-1">{update.new_status}</span>
                </p>
                {update.remarks && <p className="text-sm text-gray-600 mt-1 italic">"{update.remarks}"</p>}
                <p className="text-xs text-gray-400 mt-1">{new Date(update.created_at).toLocaleString()}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {needsFeedback && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="font-semibold text-lg mb-4">Provide Feedback</h3>
          <form onSubmit={handleFeedbackSubmit}>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">Rating (1-5)</label>
              <input 
                type="number" min="1" max="5" required
                className="w-full md:w-32 p-2 border rounded"
                value={feedback.rating}
                onChange={(e) => setFeedback({ ...feedback, rating: parseInt(e.target.value) })}
              />
            </div>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">Comments</label>
              <textarea 
                rows="3" required
                className="w-full p-2 border rounded"
                value={feedback.comments}
                onChange={(e) => setFeedback({ ...feedback, comments: e.target.value })}
              ></textarea>
            </div>
            <button 
              type="submit" 
              disabled={feedbackSubmitting}
              className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50"
            >
              Submit Feedback
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default ComplaintDetail;
