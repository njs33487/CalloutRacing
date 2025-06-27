import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { ShoppingBagIcon, PlusIcon, CurrencyDollarIcon } from '@heroicons/react/24/outline'
import { api } from '../services/api'
import { MarketplaceItem } from '../types'

export default function Marketplace() {
  const [categoryFilter, setCategoryFilter] = useState<string>('all');

  // Fetch marketplace items from API
  const { data: itemsData, isLoading, error } = useQuery({
    queryKey: ['marketplace', categoryFilter],
    queryFn: () => {
      const params = new URLSearchParams();
      if (categoryFilter !== 'all') {
        params.append('category', categoryFilter);
      }
      return api.get(`/marketplace/?${params.toString()}`).then(res => res.data);
    }
  });

  const items = itemsData?.results || [];

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

  if (error) {
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
              <div className="flex items-center text-sm text-gray-600">
                <CurrencyDollarIcon className="h-4 w-4 mr-2" />
                <span className="font-semibold text-green-600">${item.price.toLocaleString()}</span>
                {item.is_negotiable && (
                  <span className="ml-2 text-xs text-gray-500">(Negotiable)</span>
                )}
              </div>
              
              <div className="text-sm">
                <span className="text-gray-600">Condition: </span>
                <span className="font-medium">{getConditionDisplay(item.condition)}</span>
              </div>
              
              <div className="text-sm">
                <span className="text-gray-600">Seller: </span>
                <span className="font-medium">{item.seller.first_name || item.seller.username}</span>
              </div>
              
              <div className="text-sm text-gray-600">
                📍 {item.location}
              </div>
              
              <p className="text-sm text-gray-700 line-clamp-2">{item.description}</p>
              
              {item.trade_offered && (
                <div className="text-sm text-blue-600">
                  💱 Trade offers accepted
                </div>
              )}
              
              <div className="flex justify-between text-xs text-gray-500">
                <span>{item.views} views</span>
                <span>{formatDate(item.created_at)}</span>
              </div>
            </div>
            
            <div className="mt-4 pt-4 border-t border-gray-200">
              <Link
                to={`/app/marketplace/${item.id}`}
                className="w-full btn-secondary text-sm text-center block"
              >
                View Details
              </Link>
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {items.length === 0 && (
        <div className="text-center py-12">
          <ShoppingBagIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            {categoryFilter === 'all' ? 'No items for sale' : `No ${getCategoryDisplay(categoryFilter)} items`}
          </h3>
          <p className="text-gray-600 mb-6">
            {categoryFilter === 'all' 
              ? 'Be the first to list an item in the marketplace!'
              : `No ${getCategoryDisplay(categoryFilter)} items found.`
            }
          </p>
          {categoryFilter === 'all' && (
            <Link
              to="/app/marketplace/create"
              className="btn-primary inline-flex items-center"
            >
              <PlusIcon className="h-4 w-4 mr-2" />
              List Your First Item
            </Link>
          )}
        </div>
      )}
    </div>
  )
} 