import React, { useEffect, useState } from 'react';
import api from '../../utils/api';
import LoadingSpinner from '../../components/common/LoadingSpinner';

const LocationsPage = () => {
  const [locations, setLocations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newLoc, setNewLoc] = useState({ name: '', building: '' });

  useEffect(() => {
    fetchLocations();
  }, []);

  const fetchLocations = async () => {
    try {
      const res = await api.get('/locations');
      setLocations(res.data);
    } catch (error) {
      console.error("Error fetching locations", error);
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = async (e) => {
    e.preventDefault();
    try {
      await api.post('/locations', newLoc);
      setNewLoc({ name: '', building: '' });
      fetchLocations();
    } catch (error) {
      console.error("Error adding location", error);
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Manage Locations</h1>
      
      <div className="bg-white shadow-sm rounded-lg border border-gray-100 p-6 mb-6">
        <h2 className="text-lg font-medium mb-4">Add New Location</h2>
        <form onSubmit={handleAdd} className="flex gap-4 items-end">
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 mb-1">Name / Room</label>
            <input required type="text" className="w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary sm:text-sm py-2 px-3 border" value={newLoc.name} onChange={e => setNewLoc({...newLoc, name: e.target.value})} />
          </div>
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 mb-1">Building</label>
            <input type="text" className="w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary sm:text-sm py-2 px-3 border" value={newLoc.building} onChange={e => setNewLoc({...newLoc, building: e.target.value})} />
          </div>
          <button type="submit" className="px-4 py-2 bg-primary text-white rounded-md hover:bg-blue-800">Add</button>
        </form>
      </div>

      <div className="bg-white shadow-sm rounded-lg border border-gray-100 overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Building</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {locations.map(loc => (
              <tr key={loc.id}>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{loc.name}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{loc.building}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default LocationsPage;
