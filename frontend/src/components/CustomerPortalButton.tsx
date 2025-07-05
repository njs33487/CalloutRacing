import React, { useState } from 'react';
import axios from 'axios';
import { API_URL } from '../services/api';

const CustomerPortalButton: React.FC = () => {
  const [loading, setLoading] = useState(false);

  const handleManageBilling = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/subscriptions/customer-portal/`, {}, {
        headers: {
          'X-CSRFToken': document.cookie.split('csrftoken=')[1]?.split(';')[0] || '',
        },
        withCredentials: true,
      });
      
      // Redirect to the customer portal URL
      window.location.href = response.data.url;
    } catch (error) {
      console.error("Error creating customer portal session:", error);
      alert("Failed to open billing portal. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      onClick={handleManageBilling}
      disabled={loading}
      className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 disabled:opacity-50 transition-colors"
    >
      {loading ? 'Loading...' : 'Manage Billing'}
    </button>
  );
};

export default CustomerPortalButton; 