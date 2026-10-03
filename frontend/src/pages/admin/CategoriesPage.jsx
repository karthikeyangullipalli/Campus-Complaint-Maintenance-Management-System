import React, { useState, useEffect } from 'react';
import api from '../../utils/api';

const CategoriesPage = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [formData, setFormData] = useState({ name: '', description: '' });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      const res = await api.get('/categories');
      setCategories(res.data.data || []);
    } catch (error) {
      console.error('Error fetching categories:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingId) {
        await api.put(`/categories/${editingId}`, formData);
      } else {
        await api.post('/categories', formData);
      }
      setFormData({ name: '', description: '' });
      setEditingId(null);
      fetchCategories();
    } catch (error) {
      console.error('Error saving category:', error);
      alert(error.response?.data?.message || 'Error saving category');
    }
  };

  const handleEdit = (cat) => {
    setEditingId(cat.id);
    setFormData({ name: cat.name, description: cat.description || '' });
  };

  return (
    <div className="p-6 max-w-6xl mx-auto flex flex-col md:flex-row gap-6">
      <div className="flex-1">
        <h1 className="text-2xl font-bold text-gray-800 mb-6">Manage Categories</h1>
        
        {loading ? (
          <div>Loading...</div>
        ) : (
          <div className="bg-white rounded shadow overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-gray-50 border-b">
                  <th className="p-4 font-semibold text-sm text-gray-600">Name</th>
                  <th className="p-4 font-semibold text-sm text-gray-600">Description</th>
                  <th className="p-4 font-semibold text-sm text-gray-600">Action</th>
                </tr>
              </thead>
              <tbody>
                {categories.map(cat => (
                  <tr key={cat.id} className="border-b hover:bg-gray-50">
                    <td className="p-4 text-sm font-medium text-gray-900">{cat.name}</td>
                    <td className="p-4 text-sm text-gray-700">{cat.description}</td>
                    <td className="p-4 text-sm text-blue-600">
                      <button onClick={() => handleEdit(cat)} className="hover:underline">Edit</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="w-full md:w-80">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="font-semibold text-lg mb-4">{editingId ? 'Edit Category' : 'Add Category'}</h3>
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
              <input 
                type="text" required
                className="w-full p-2 border rounded text-sm"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              />
            </div>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
              <textarea 
                rows="3"
                className="w-full p-2 border rounded text-sm"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              ></textarea>
            </div>
            <div className="flex gap-2">
              <button type="submit" className="flex-1 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                {editingId ? 'Update' : 'Add'}
              </button>
              {editingId && (
                <button type="button" onClick={() => { setEditingId(null); setFormData({name:'', description:''}); }} className="px-4 py-2 bg-gray-300 text-gray-800 rounded hover:bg-gray-400">
                  Cancel
                </button>
              )}
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default CategoriesPage;
