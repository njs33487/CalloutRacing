import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { ShoppingBagIcon, PlusIcon, CurrencyDollarIcon, TrashIcon, PencilIcon, PhoneIcon, EnvelopeIcon, MapPinIcon } from '@heroicons/react/24/outline'
import { marketplaceAPI } from '../services/api'
import { MarketplaceItem } from '../types'
import { useAuth } from '../contexts/AuthContext'
import AdDisplay from '../components/AdDisplay'

export default function Marketplace() {
  const { user: authUser } = useAuth();
  const queryClient = useQueryClient();
  const [categoryFilter, setCategoryFilter] = useState<string>('all');
  const [showDeleteConfirm, setShowDeleteConfirm] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // Fetch marketplace items from API
  const { data: itemsData, isLoading, error: fetchError } = useQuery({
    queryKey: ['marketplace', categoryFilter],
    queryFn: () => {
      const params = new URLSearchParams();
      if (categoryFilter !== 'all') {
        params.append('category', categoryFilter);
      }
      return marketplaceAPI.list().then(res => res.data);
    }
  });

  const items = itemsData?.results || [];

  // Mutations for CRUD operations
  const deleteMutation = useMutation({
    mutationFn: (itemId: number) => marketplaceAPI.delete(itemId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['marketplace'] });
      setShowDeleteConfirm(null);
      setSuccess('Item deleted successfully!');
    },
    onError: (error) => {
      console.error('Error deleting item:', error);
      setError('Failed to delete item. Please try again.');
    }
  });

  // Clear messages after 5 seconds
  useState(() => {
    if (error || success) {
      const timer = setTimeout(() => {
        setError(null);
        setSuccess(null);
      }, 5000);
      return () => clearTimeout(timer);
    }
  });

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  }

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'car':
        return 'bg-blue-100 text-blue-800'
      case 'parts':
        return 'bg-green-100 text-green-800'
      case 'wheels':
        return 'bg-purple-100 text-purple-800'
      case 'electronics':
        return 'bg-yellow-100 text-yellow-800'
      case 'tools':
        return 'bg-red-100 text-red-800'
      case 'other':
        return 'bg-gray-100 text-gray-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getCategoryDisplay = (category: string) => {
    switch (category) {
      case 'car':
        return 'Car'
      case 'parts':
        return 'Parts'
      case 'wheels':
        return 'Wheels & Tires'
      case 'electronics':
        return 'Electronics'
      case 'tools':
        return 'Tools'
      case 'other':
        return 'Other'
      default:
        return category
    }
  }

  const getConditionDisplay = (condition: string) => {
    switch (condition) {
      case 'new':
        return 'New'
      case 'like_new':
        return 'Like New'
      case 'good':
        return 'Good'
      case 'fair':
        return 'Fair'
      case 'poor':
        return 'Poor'
      default:
        return condition
    }
  }

  const isItemOwner = (item: MarketplaceItem) => {
    return authUser && item.seller.id === authUser.id;
  };

  const canDeleteItem = (item: MarketplaceItem) => {
    return isItemOwner(item);
  };

  const handleDeleteItem = (itemId: number) => {
    deleteMutation.mutate(itemId);
  };

  const handleContactSeller = (item: MarketplaceItem) => {
    // This could open a contact modal or redirect to messaging
    if (item.contact_phone) {
      window.open(`tel:${item.contact_phone}`, '_blank');
    } else if (item.contact_email) {
      window.open(`mailto:${item.contact_email}`, '_blank');
    }
  };

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Marketplace</h1>
            <p className="text-gray-600">Buy, sell, and trade cars, parts, and racing equipment</p>
          </div>
          <Link
            to="/app/marketplace/create"
            className="btn-primary inline-flex items-center"
          >
            <PlusIcon className="h-4 w-4 mr-2" />
            List Item
          </Link>
        </div>
        
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      </div>
    );
  }

  if (fetchError) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Marketplace</h1>
            <p className="text-gray-600">Buy, sell, and trade cars, parts, and racing equipment</p>
          </div>
          <Link
            to="/app/marketplace/create"
            className="btn-primary inline-flex items-center"
          >
            <PlusIcon className="h-4 w-4 mr-2" />
            List Item
          </Link>
        </div>
        
        <div className="text-center py-12">
          <div className="text-red-600 mb-4">
            <ShoppingBagIcon className="h-12 w-12 mx-auto" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">Error Loading Marketplace</h3>
          <p className="text-gray-600">Unable to load marketplace items. Please try again later.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Error/Success Messages */}
      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          </div>
        </div>
      )}

      {success && (
        <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-green-800">{success}</p>
            </div>
          </div>
        </div>
      )}

      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Marketplace</h1>
          <p className="text-gray-600">Buy, sell, and trade cars, parts, and racing equipment</p>
        </div>
        <Link
          to="/app/marketplace/create"
          className="btn-primary inline-flex items-center"
        >
          <PlusIcon className="h-4 w-4 mr-2" />
          List Item
        </Link>
      </div>

      {/* Filter */}
      <div className="flex space-x-2">
        {['all', 'car', 'parts', 'wheels', 'electronics', 'tools', 'other'].map((category) => (
          <button
            key={category}
            onClick={() => setCategoryFilter(category)}
            className={`px-3 py-1 rounded-full text-sm font-medium ${
              categoryFilter === category
                ? 'bg-primary-100 text-primary-800'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {category === 'all' ? 'All Items' : getCategoryDisplay(category)}
          </button>
        ))}
      </div>

      {/* Ad Display */}
      <AdDisplay adSlot="YOUR_MARKETPLACE_AD_SLOT_ID" />

      {/* Marketplace Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {items.map((item: MarketplaceItem) => (
          <div key={item.id} className="card hover:shadow-md transition-shadow">
            {/* Item Image */}
            <div className="mb-4 h-48 bg-gray-100 rounded-lg overflow-hidden">
              {item.images && item.images.length > 0 ? (
                <img
                  src={item.images.find(img => img.is_primary)?.image || item.images[0].image}
                  alt={item.title}
                  className="w-full h-full object-cover"
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center">
                  <ShoppingBagIcon className="h-16 w-16 text-gray-400" />
                </div>
              )}
            </div>
            
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center">
                <ShoppingBagIcon className="h-6 w-6 text-primary-600 mr-2" />
                <h3 className="text-lg font-semibold text-gray-900">
                  {item.title}
                </h3>
              </div>
              <span className={`px-2 py-1 text-xs rounded-full font-medium ${getCategoryColor(item.category)}`}>
                {getCategoryDisplay(item.category)}
              </span>
            </div>
            
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center text-sm text-gray-600">
                  <CurrencyDollarIcon className="h-4 w-4 mr-2" />
                  <span className="font-semibold text-green-600">${item.price}</span>
                </div>
                <span className="text-xs text-gray-500">
                  {getConditionDisplay(item.condition)}
                </span>
              </div>
              
              <div className="flex items-center text-sm text-gray-600">
                <MapPinIcon className="h-4 w-4 mr-2" />
                {item.location}
              </div>
              
              <p className="text-sm text-gray-700 line-clamp-2">{item.description}</p>
              
              <div className="flex items-center justify-between text-xs text-gray-500">
                <span>Seller: {item.seller.first_name} {item.seller.last_name}</span>
                <span>{item.views} views</span>
              </div>
              
              <div className="text-xs text-gray-500">
                Listed: {formatDate(item.created_at)}
              </div>
            </div>
            
            {/* Action Buttons */}
            <div className="mt-4 pt-4 border-t border-gray-200">
              <div className="flex items-center justify-between">
                <Link
                  to={`/app/marketplace/${item.id}`}
                  className="text-primary-600 hover:text-primary-700 font-medium text-sm"
                >
                  View Details
                </Link>
                
                <div className="flex space-x-2">
                  {!isItemOwner(item) && (item.contact_phone || item.contact_email) && (
                    <button
                      onClick={() => handleContactSeller(item)}
                      className="bg-blue-600 text-white px-3 py-1 rounded-lg hover:bg-blue-700 text-sm"
                    >
                      {item.contact_phone ? (
                        <PhoneIcon className="h-4 w-4" />
                      ) : (
                        <EnvelopeIcon className="h-4 w-4" />
                      )}
                    </button>
                  )}
                  
                  {canDeleteItem(item) && (
                    <button
                      onClick={() => setShowDeleteConfirm(item.id)}
                      className="bg-gray-600 text-white p-2 rounded-lg hover:bg-gray-700"
                      title="Delete Item"
                    >
                      <TrashIcon className="h-4 w-4" />
                    </button>
                  )}
                  
                  {isItemOwner(item) && (
                    <Link
                      to={`/app/marketplace/${item.id}/edit`}
                      className="bg-blue-600 text-white p-2 rounded-lg hover:bg-blue-700"
                      title="Edit Item"
                    >
                      <PencilIcon className="h-4 w-4" />
                    </Link>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {items.length === 0 && (
        <div className="text-center py-12">
          <ShoppingBagIcon className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Items Found</h3>
          <p className="text-gray-600 mb-6">
            {categoryFilter === 'all' 
              ? "No items have been listed yet. Be the first to list something!"
              : `No ${getCategoryDisplay(categoryFilter)} items found.`
            }
          </p>
          {categoryFilter === 'all' && (
            <Link
              to="/app/marketplace/create"
              className="btn-primary inline-flex items-center"
            >
              <PlusIcon className="h-4 w-4 mr-2" />
              List First Item
            </Link>
          )}
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Delete Item</h3>
            <p className="text-gray-600 mb-6">Are you sure you want to delete this item? This action cannot be undone.</p>
            <div className="flex space-x-3">
              <button
                onClick={() => handleDeleteItem(showDeleteConfirm)}
                disabled={deleteMutation.isPending}
                className="flex-1 bg-red-600 text-white py-2 px-4 rounded-md hover:bg-red-700 transition-colors disabled:opacity-50"
              >
                {deleteMutation.isPending ? 'Deleting...' : 'Delete'}
              </button>
              <button
                onClick={() => setShowDeleteConfirm(null)}
                className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400 transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
} 