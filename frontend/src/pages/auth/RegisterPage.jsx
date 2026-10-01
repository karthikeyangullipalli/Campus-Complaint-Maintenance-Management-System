import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../../utils/api';

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    role: 'STUDENT',
    department: '',
    phone: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      return setError('Passwords do not match');
    }
    setError('');
    setLoading(true);
    try {
      await api.post('/auth/register', formData);
      navigate('/login', { state: { message: 'Registration successful. Please login.' } });
    } catch (err) {
      setError(err.response?.data?.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Create an account
        </h2>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10 border border-gray-100">
          <form className="space-y-4" onSubmit={handleSubmit}>
            {error && <div className="text-sm text-red-600 bg-red-50 p-2 rounded">{error}</div>}
            
            <div>
              <label className="block text-sm font-medium text-gray-700">Name</label>
              <input type="text" name="name" required className="mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-primary focus:border-primary sm:text-sm" onChange={handleChange} />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Email</label>
              <input type="email" name="email" required className="mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-primary focus:border-primary sm:text-sm" onChange={handleChange} />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Role</label>
              <select name="role" value={formData.role} onChange={handleChange} className="mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-primary focus:border-primary sm:text-sm">
                <option value="STUDENT">Student</option>
                <option value="FACULTY">Faculty</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Department</label>
              <input type="text" name="department" className="mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-primary focus:border-primary sm:text-sm" onChange={handleChange} />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Phone</label>
              <input type="text" name="phone" className="mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-primary focus:border-primary sm:text-sm" onChange={handleChange} />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Password</label>
              <input type="password" name="password" required className="mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-primary focus:border-primary sm:text-sm" onChange={handleChange} />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Confirm Password</label>
              <input type="password" name="confirmPassword" required className="mt-1 block w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-primary focus:border-primary sm:text-sm" onChange={handleChange} />
            </div>

            <div>
              <button type="submit" disabled={loading} className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:opacity-50">
                {loading ? 'Registering...' : 'Register'}
              </button>
            </div>
          </form>

          <div className="mt-6 text-center">
            <Link to="/login" className="font-medium text-primary hover:text-blue-800">
              Already have an account? Sign in
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;
