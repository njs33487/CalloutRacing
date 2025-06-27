import { useState } from 'react'
import { Link } from 'react-router-dom'
import { ShoppingBagIcon, PlusIcon, CurrencyDollarIcon } from '@heroicons/react/24/outline'

export default function Marketplace() {
  const [items] = useState([
    {
      id: 1,
      title: 'Turbocharger Kit - GT35R',
      category: 'Parts',
      price: 2500,
      condition: 'Like New',
      seller: 'TurboKing',
      location: 'Los Angeles, CA',
      description: 'Complete turbo kit with all necessary components'
    },
    {
      id: 2,
      title: '2018 Mustang GT',
      category: 'Car',
      price: 45000,
      condition: 'Good',
      seller: 'SpeedDemon',
      location: 'Miami, FL',
      description: 'Modified Mustang with performance upgrades'
    }
  ])

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

      {/* Marketplace Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {items.map((item) => (
          <div key={item.id} className="card hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center">
                <ShoppingBagIcon className="h-6 w-6 text-primary-600 mr-2" />
                <h3 className="text-lg font-semibold text-gray-900">
                  {item.title}
                </h3>
              </div>
              <span className="px-2 py-1 text-xs rounded-full font-medium bg-green-100 text-green-800">
                {item.category}
              </span>
            </div>
            
            <div className="space-y-3">
              <div className="flex items-center text-sm text-gray-600">
                <CurrencyDollarIcon className="h-4 w-4 mr-2" />
                <span className="font-semibold text-green-600">${item.price.toLocaleString()}</span>
              </div>
              
              <div className="text-sm">
                <span className="text-gray-600">Condition: </span>
                <span className="font-medium">{item.condition}</span>
              </div>
              
              <div className="text-sm">
                <span className="text-gray-600">Seller: </span>
                <span className="font-medium">{item.seller}</span>
              </div>
              
              <div className="text-sm text-gray-600">
                📍 {item.location}
              </div>
              
              <p className="text-sm text-gray-700">{item.description}</p>
            </div>
            
            <div className="mt-4 pt-4 border-t border-gray-200">
              <button className="w-full btn-secondary text-sm">
                View Details
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {items.length === 0 && (
        <div className="text-center py-12">
          <ShoppingBagIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No items for sale</h3>
          <p className="text-gray-600 mb-6">Be the first to list an item in the marketplace!</p>
          <Link
            to="/app/marketplace/create"
            className="btn-primary inline-flex items-center"
          >
            <PlusIcon className="h-4 w-4 mr-2" />
            List Your First Item
          </Link>
        </div>
      )}
    </div>
  )
} 