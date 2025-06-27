import { useState } from 'react';

export default function CreateCallout() {
  const [formData, setFormData] = useState({
    challenged: '',
    race_type: 'quarter_mile',
    location_type: 'track',
    track: '',
    street_location: '',
    wager_amount: '',
    scheduled_date: '',
    car_details: '',
    message: ''
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Submit logic here
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Create Callout</h1>
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="space-y-6">
          <div>
            <label htmlFor="challenged" className="block mb-2">Challenge User</label>
            <input
              type="text"
              id="challenged"
              name="challenged"
              value={formData.challenged}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded"
              required
            />
          </div>
          <div>
            <label htmlFor="race_type" className="block mb-2">Race Type</label>
            <select
              id="race_type"
              name="race_type"
              value={formData.race_type}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded"
            >
              <option value="quarter_mile">Quarter Mile</option>
              <option value="eighth_mile">Eighth Mile</option>
              <option value="roll_race">Roll Race</option>
              <option value="dig_race">Dig Race</option>
            </select>
          </div>
          <div>
            <label htmlFor="location_type" className="block mb-2">Location Type</label>
            <select
              id="location_type"
              name="location_type"
              value={formData.location_type}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded"
            >
              <option value="track">Track</option>
              <option value="street">Street</option>
            </select>
          </div>
          {formData.location_type === 'track' ? (
            <div>
              <label htmlFor="track" className="block mb-2">Track</label>
              <input
                type="text"
                id="track"
                name="track"
                value={formData.track}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
              />
            </div>
          ) : (
            <div>
              <label htmlFor="street_location" className="block mb-2">Street Location</label>
              <input
                type="text"
                id="street_location"
                name="street_location"
                value={formData.street_location}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
              />
            </div>
          )}
          <div>
            <label htmlFor="wager_amount" className="block mb-2">Wager (Optional)</label>
            <input
              type="number"
              id="wager_amount"
              name="wager_amount"
              value={formData.wager_amount}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded"
              min="0"
              step="0.01"
            />
          </div>
          <div>
            <label htmlFor="scheduled_date" className="block mb-2">Scheduled Date (Optional)</label>
            <input
              type="datetime-local"
              id="scheduled_date"
              name="scheduled_date"
              value={formData.scheduled_date}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded"
            />
          </div>
          <div>
            <label htmlFor="car_details" className="block mb-2">Car Details (Optional)</label>
            <textarea
              id="car_details"
              name="car_details"
              value={formData.car_details}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded"
            />
          </div>
          <div>
            <label htmlFor="message" className="block mb-2">Message</label>
            <textarea
              id="message"
              name="message"
              value={formData.message}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded"
              required
            />
          </div>
          <div className="flex space-x-4">
            <button type="button" className="flex-1 bg-gray-200 py-2 rounded">Cancel</button>
            <button type="submit" className="flex-1 bg-blue-600 text-white py-2 rounded">Create Callout</button>
          </div>
        </div>
      </form>
    </div>
  );
} 