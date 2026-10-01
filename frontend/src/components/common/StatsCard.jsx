import React from 'react';

const StatsCard = ({ title, value, icon: Icon, colorClass = "text-blue-600 bg-blue-100" }) => {
  return (
    <div className="bg-white rounded-xl shadow-sm p-6 flex items-center border border-gray-100">
      <div className={`p-4 rounded-full mr-4 ${colorClass}`}>
        <Icon className="w-6 h-6" />
      </div>
      <div>
        <p className="text-sm font-medium text-gray-500 uppercase tracking-wider">{title}</p>
        <p className="text-3xl font-bold text-gray-900">{value}</p>
      </div>
    </div>
  );
};

export default StatsCard;
