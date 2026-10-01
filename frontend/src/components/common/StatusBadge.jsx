import React from 'react';
import { getStatusColor, formatStatus } from '../../utils/helpers';

const StatusBadge = ({ status }) => {
  return (
    <span className={`px-2.5 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(status)}`}>
      {formatStatus(status)}
    </span>
  );
};

export default StatusBadge;
