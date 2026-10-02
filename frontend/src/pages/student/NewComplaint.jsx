import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../utils/api';
import LoadingSpinner from '../../components/common/LoadingSpinner';

const NewComplaint = () => {
  const [categories, setCategories] = useState([]);
  const [locations, setLocations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [image, setImage] = useState(null);

  const [formData, setFormData] = useState({
    title: '',
    category_id: '',
    location_id: '',
    description: '',
    priority: 'MEDIUM'
  });

  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [catRes, locRes] = await Promise.all([
          api.get('/categories'),
          api.get('/locations')
        ]);
        // API returns { success, count, data: [...] }
        setCategories(catRes.data.data || []);
        setLocations(locRes.data.data || []);
      } catch (err) {
        console.error('Failed to load form data', err);
        setError('Failed to load categories and locations. Please try again later.');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleImageChange = (e) => {
    setImage(e.target.files[0] || null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');

    try {
      // Use FormData to support optional image upload
      const payload = new FormData();
      payload.append('title', formData.title);
      payload.append('category_id', formData.category_id);
      payload.append('location_id', formData.location_id);
      payload.append('description', formData.description);
      payload.append('priority', formData.priority);
      if (image) payload.append('image', image);

      const res = await api.post('/complaints', payload, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      // Backend returns { success, complaintId, complaint_number }
      navigate(`/student/complaints/${res.data.complaintId}`);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to submit complaint');
      setSubmitting(false);
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">File a New Complaint</h1>

      <div className="bg-white shadow-sm rounded-lg border border-gray-100 p-6">
        {error && (
          <div className="mb-4 bg-red-50 border-l-4 border-red-400 p-4 text-sm text-red-700">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Title */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Title <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              name="title"
              required
              maxLength={255}
              className="w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm py-2 px-3"
              placeholder="Brief summary of the issue"
              value={formData.title}
              onChange={handleChange}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Category */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Category <span className="text-red-500">*</span>
              </label>
              <select
                name="category_id"
                required
                className="w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm py-2 px-3"
                value={formData.category_id}
                onChange={handleChange}
              >
                <option value="">Select a category</option>
                {categories.map(c => (
                  <option key={c.id} value={c.id}>{c.name}</option>
                ))}
              </select>
            </div>

            {/* Location — uses display_name from API (CONCAT of building/floor/room) */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Location <span className="text-red-500">*</span>
              </label>
              <select
                name="location_id"
                required
                className="w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm py-2 px-3"
                value={formData.location_id}
                onChange={handleChange}
              >
                <option value="">Select a location</option>
                {locations.map(l => (
                  <option key={l.id} value={l.id}>
                    {l.display_name || `${l.building}${l.floor ? ` - ${l.floor}` : ''}${l.room ? `, ${l.room}` : ''}`}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Priority */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Priority</label>
            <select
              name="priority"
              className="w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm py-2 px-3"
              value={formData.priority}
              onChange={handleChange}
            >
              <option value="LOW">Low — Routine / cosmetic issue</option>
              <option value="MEDIUM">Medium — Needs attention soon</option>
              <option value="HIGH">High — Urgent, affects work/study</option>
              <option value="CRITICAL">Critical — Immediate safety hazard</option>
            </select>
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description <span className="text-red-500">*</span>
            </label>
            <textarea
              name="description"
              required
              rows={4}
              className="w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm py-2 px-3"
              placeholder="Provide detailed information about the problem (location specifics, when it started, severity...)"
              value={formData.description}
              onChange={handleChange}
            />
          </div>

          {/* Image Upload (optional) */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Attach Image <span className="text-gray-400">(optional, max 5MB)</span>
            </label>
            <input
              type="file"
              accept="image/jpeg,image/png,image/gif"
              onChange={handleImageChange}
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
            />
          </div>

          <div className="flex justify-end space-x-3 pt-2">
            <button
              type="button"
              onClick={() => navigate('/student/complaints')}
              className="px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-700 hover:bg-blue-800 disabled:opacity-50"
            >
              {submitting ? 'Submitting...' : 'Submit Complaint'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default NewComplaint;
