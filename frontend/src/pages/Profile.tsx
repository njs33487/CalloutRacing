import { useState } from 'react';

export default function Profile() {
  const [editForm, setEditForm] = useState({
    bio: '',
    location: '',
    car_make: '',
    car_model: '',
    car_year: '',
    car_mods: ''
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setEditForm({ ...editForm, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Submit logic here
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Edit Profile</h1>
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="space-y-6">
          <div>
            <label htmlFor="bio" className="block mb-2">Bio</label>
            <textarea
              id="bio"
              name="bio"
              value={editForm.bio}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded"
              placeholder="Tell us about yourself..."
            />
          </div>
          <div>
            <label htmlFor="location" className="block mb-2">Location</label>
            <input
              type="text"
              id="location"
              name="location"
              value={editForm.location}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded"
              placeholder="City, State"
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="car_make" className="block mb-2">Car Make</label>
              <input
                type="text"
                id="car_make"
                name="car_make"
                value={editForm.car_make}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
                placeholder="e.g., Ford"
              />
            </div>
            <div>
              <label htmlFor="car_model" className="block mb-2">Car Model</label>
              <input
                type="text"
                id="car_model"
                name="car_model"
                value={editForm.car_model}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
                placeholder="e.g., Mustang"
              />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="car_year" className="block mb-2">Car Year</label>
              <input
                type="number"
                id="car_year"
                name="car_year"
                value={editForm.car_year}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
                placeholder="e.g., 2020"
                min="1900"
                max="2030"
              />
            </div>
            <div>
              <label htmlFor="car_mods" className="block mb-2">Modifications</label>
              <input
                type="text"
                id="car_mods"
                name="car_mods"
                value={editForm.car_mods}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
                placeholder="e.g., Turbo, Exhaust"
              />
            </div>
          </div>
          <div className="flex space-x-4">
            <button type="button" className="flex-1 bg-gray-200 py-2 rounded">Cancel</button>
            <button type="submit" className="flex-1 bg-blue-600 text-white py-2 rounded">Save Changes</button>
          </div>
        </div>
      </form>
    </div>
  );
} 