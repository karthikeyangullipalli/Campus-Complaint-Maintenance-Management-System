import React, { useState, useEffect } from 'react';
import api from '../../utils/api';

const LocationsPage = () => {
  const [locations, setLocations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [formData, setFormData] = useState({ building: '', floor: '', room: '', description: '' });

  useEffect(() => {
    fetchLocations();
  }, []);

  const fetchLocations = async () => {
    try {
      const res = await api.get('/locations');
      setLocations(res.data.data || []);
    } catch (error) {
      console.error('Error fetching locations:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/locations', formData);
      setFormData({ building: '', floor: '', room: '', description: '' });
      fetchLocations();
    } catch (error) {
      console.error('Error saving location:', error);
      alert(error.response?.data?.message || 'Error saving location');
    }
  };

  return (
    <div className="p-6 max-w-6xl mx-auto flex flex-col md:flex-row gap-6">
      <div className="flex-1">
        <h1 className="text-2xl font-bold text-gray-800 mb-6">Manage Locations</h1>
        
        {loading ? (
          <div>Loading...</div>
        ) : (
          <div className="bg-white rounded shadow overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-gray-50 border-b">
                  <th className="p-4 font-semibold text-sm text-gray-600">Location Name</th>
                  <th className="p-4 font-semibold text-sm text-gray-600">Building</th>
                  <th className="p-4 font-semibold text-sm text-gray-600">Floor</th>
                  <th className="p-4 font-semibold text-sm text-gray-600">Room</th>
                </tr>
              </thead>
              <tbody>
                {locations.map(loc => (
                  <tr key={loc.id} className="border-b hover:bg-gray-50">
                    <td className="p-4 text-sm font-medium text-gray-900">
                      {loc.display_name || `${loc.building} ${loc.floor ? '- Flr ' + loc.floor : ''} ${loc.room ? '- Rm ' + loc.room : ''}`}
                    </td>
                    <td className="p-4 text-sm text-gray-700">{loc.building}</td>
                    <td className="p-4 text-sm text-gray-700">{loc.floor || '-'}</td>
                    <td className="p-4 text-sm text-gray-700">{loc.room || '-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="w-full md:w-80">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="font-semibold text-lg mb-4">Add Location</h3>
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">Building *</label>
              <input 
                type="text" required
                className="w-full p-2 border rounded text-sm"
                value={formData.building}
                onChange={(e) => setFormData({ ...formData, building: e.target.value })}
              />
            </div>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">Floor</label>
              <input 
                type="text"
                className="w-full p-2 border rounded text-sm"
                value={formData.floor}
                onChange={(e) => setFormData({ ...formData, floor: e.target.value })}
              />
            </div>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">Room</label>
              <input 
                type="text"
                className="w-full p-2 border rounded text-sm"
                value={formData.room}
                onChange={(e) => setFormData({ ...formData, room: e.target.value })}
              />
            </div>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
              <textarea 
                rows="2"
                className="w-full p-2 border rounded text-sm"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              ></textarea>
            </div>
            <button type="submit" className="w-full py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
              Add Location
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default LocationsPage;
