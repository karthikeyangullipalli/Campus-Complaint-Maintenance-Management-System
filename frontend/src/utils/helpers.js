export const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric', month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit'
  }).format(date);
};

export const getStatusColor = (status) => {
  switch (status) {
    case 'NEW': return 'bg-gray-100 text-gray-800';
    case 'VERIFIED': return 'bg-blue-100 text-blue-800';
    case 'ASSIGNED': return 'bg-purple-100 text-purple-800';
    case 'IN_PROGRESS': return 'bg-yellow-100 text-yellow-800';
    case 'RESOLVED': return 'bg-green-100 text-green-800';
    case 'CLOSED': return 'bg-green-200 text-green-900';
    case 'REJECTED': return 'bg-red-100 text-red-800';
    case 'REOPENED': return 'bg-orange-100 text-orange-800';
    default: return 'bg-gray-100 text-gray-800';
  }
};

export const getPriorityColor = (priority) => {
  switch (priority) {
    case 'LOW': return 'bg-green-100 text-green-800';
    case 'MEDIUM': return 'bg-yellow-100 text-yellow-800';
    case 'HIGH': return 'bg-orange-100 text-orange-800';
    case 'CRITICAL': return 'bg-red-100 text-red-800';
    default: return 'bg-gray-100 text-gray-800';
  }
};

export const formatStatus = (status) => {
  if (!status) return '';
  return status.replace(/_/g, ' ').replace(/\w\S*/g, (w) => (w.replace(/^\w/, (c) => c.toUpperCase())));
};
