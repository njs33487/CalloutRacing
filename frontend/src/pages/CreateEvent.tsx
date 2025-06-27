import { useState } from 'react';

export default function CreateEvent() {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    event_type: 'race',
    track: '',
    start_date: '',
    end_date: '',
    max_participants: '',
    entry_fee: ''
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
      <h1 className="text-3xl font-bold mb-6">Create Event</h1>
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="space-y-6">
          <div>
            <label htmlFor="title" className="block mb-2">Event Title</label>
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
          <div>
            <label htmlFor="event_type" className="block mb-2">Event Type</label>
            <select
              id="event_type"
              name="event_type"
              value={formData.event_type}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded"
              required
            >
              <option value="race">Race Event</option>
              <option value="meet">Car Meet</option>
              <option value="show">Car Show</option>
              <option value="test">Test & Tune</option>
            </select>
          </div>
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
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="start_date" className="block mb-2">Start Date & Time</label>
              <input
                type="datetime-local"
                id="start_date"
                name="start_date"
                value={formData.start_date}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
                required
              />
            </div>
            <div>
              <label htmlFor="end_date" className="block mb-2">End Date & Time</label>
              <input
                type="datetime-local"
                id="end_date"
                name="end_date"
                value={formData.end_date}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
                required
              />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="max_participants" className="block mb-2">Max Participants (Optional)</label>
              <input
                type="number"
                id="max_participants"
                name="max_participants"
                value={formData.max_participants}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
                min="1"
              />
            </div>
            <div>
              <label htmlFor="entry_fee" className="block mb-2">Entry Fee (Optional)</label>
              <input
                type="number"
                id="entry_fee"
                name="entry_fee"
                value={formData.entry_fee}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
                min="0"
                step="0.01"
              />
            </div>
          </div>
          <div className="flex space-x-4">
            <button type="button" className="flex-1 bg-gray-200 py-2 rounded">Cancel</button>
            <button type="submit" className="flex-1 bg-blue-600 text-white py-2 rounded">Create Event</button>
          </div>
        </div>
      </form>
    </div>
  );
} 