import React from 'react';
import { getPriorityColor } from '../../utils/helpers';

const PriorityBadge = ({ priority }) => {
  return (
    <span className={`px-2.5 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${getPriorityColor(priority)}`}>
      {priority}
    </span>
  );
};

export default PriorityBadge;
