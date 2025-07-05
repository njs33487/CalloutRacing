import React from 'react';

interface Part {
  id: number;
  name: string;
  description: string;
  price: number;
  affiliate_link?: string;
  condition: string;
  location: string;
}

interface PartListingProps {
  part: Part;
}

const PartListing: React.FC<PartListingProps> = ({ part }) => {
  return (
    <div className="part-card bg-white rounded-lg shadow-md p-6 border border-gray-200">
      <h3 className="text-lg font-semibold text-gray-900 mb-2">{part.name}</h3>
      <p className="text-gray-600 mb-3">{part.description}</p>
      <div className="flex justify-between items-center mb-4">
        <span className="text-2xl font-bold text-primary-600">${part.price}</span>
        <span className="text-sm text-gray-500">{part.condition}</span>
      </div>
      <div className="space-y-2">
        <p className="text-sm text-gray-500">Location: {part.location}</p>
        {part.affiliate_link && (
          <a 
            href={part.affiliate_link} 
            target="_blank" 
            rel="noopener noreferrer" 
            className="inline-block bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
          >
            Buy New (Affiliate Link)
          </a>
        )}
        <button className="w-full bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 transition-colors">
          Contact Seller
        </button>
      </div>
    </div>
  );
};

export default PartListing; 