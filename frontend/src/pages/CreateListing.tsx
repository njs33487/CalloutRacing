import { useState } from 'react';

export default function CreateListing() {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: 'parts',
    price: '',
    condition: 'good',
    location: '',
    contact_phone: '',
    contact_email: '',
    is_negotiable: false,
    trade_offered: false,
    trade_description: ''
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleCheckboxChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.checked });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Submit logic here
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Create Listing</h1>
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="space-y-6">
          <div>
            <label htmlFor="title" className="block mb-2">Item Title</label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded"
              required
            />
          </div>
          <div>
            <label htmlFor="description" className="block mb-2">Description</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded"
              required
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="category" className="block mb-2">Category</label>
              <select
                id="category"
                name="category"
                value={formData.category}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
                required
              >
                <option value="car">Car</option>
                <option value="parts">Parts</option>
                <option value="wheels">Wheels & Tires</option>
                <option value="electronics">Electronics</option>
                <option value="tools">Tools</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div>
              <label htmlFor="condition" className="block mb-2">Condition</label>
              <select
                id="condition"
                name="condition"
                value={formData.condition}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
                required
              >
                <option value="new">New</option>
                <option value="like_new">Like New</option>
                <option value="good">Good</option>
                <option value="fair">Fair</option>
                <option value="poor">Poor</option>
              </select>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="price" className="block mb-2">Price ($)</label>
              <input
                type="number"
                id="price"
                name="price"
                value={formData.price}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
                min="0"
                step="0.01"
                required
              />
            </div>
            <div>
              <label htmlFor="location" className="block mb-2">Location</label>
              <input
                type="text"
                id="location"
                name="location"
                value={formData.location}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
                required
              />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="contact_phone" className="block mb-2">Contact Phone (Optional)</label>
              <input
                type="tel"
                id="contact_phone"
                name="contact_phone"
                value={formData.contact_phone}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
              />
            </div>
            <div>
              <label htmlFor="contact_email" className="block mb-2">Contact Email (Optional)</label>
              <input
                type="email"
                id="contact_email"
                name="contact_email"
                value={formData.contact_email}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
              />
            </div>
          </div>
          <div className="space-y-4">
            <div className="flex items-center">
              <input
                type="checkbox"
                id="is_negotiable"
                name="is_negotiable"
                checked={formData.is_negotiable}
                onChange={handleCheckboxChange}
                className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
              <label htmlFor="is_negotiable" className="ml-2 block text-sm text-gray-900">
                Price is negotiable
              </label>
            </div>
            <div className="flex items-center">
              <input
                type="checkbox"
                id="trade_offered"
                name="trade_offered"
                checked={formData.trade_offered}
                onChange={handleCheckboxChange}
                className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
              <label htmlFor="trade_offered" className="ml-2 block text-sm text-gray-900">
                Trade offers accepted
              </label>
            </div>
          </div>
          {formData.trade_offered && (
            <div>
              <label htmlFor="trade_description" className="block mb-2">Trade Description</label>
              <textarea
                id="trade_description"
                name="trade_description"
                value={formData.trade_description}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
              />
            </div>
          )}
          <div className="flex space-x-4">
            <button type="button" className="flex-1 bg-gray-200 py-2 rounded">Cancel</button>
            <button type="submit" className="flex-1 bg-blue-600 text-white py-2 rounded">Create Listing</button>
          </div>
        </div>
      </form>
    </div>
  );
} 