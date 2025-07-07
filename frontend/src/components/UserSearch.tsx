import React, { useState, useEffect, useCallback } from 'react';
import { Search, User } from 'lucide-react';
import { api } from '../services/api';
import { User as UserType } from '../types';

interface UserSearchProps {
  onUserSelect?: (user: UserType) => void;
  placeholder?: string;
  showProfile?: boolean;
}

const UserSearch: React.FC<UserSearchProps> = ({ 
  onUserSelect, 
  placeholder = "Search users...",
  showProfile = true 
}) => {
  const [query, setQuery] = useState('');
  const [users, setUsers] = useState<UserType[]>([]);
  const [loading, setLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);

  const searchUsers = useCallback(async (searchQuery: string) => {
    if (searchQuery.length < 2) {
      setUsers([]);
      setShowResults(false);
      return;
    }

    try {
      setLoading(true);
      const response = await api.get(`/racing/search-users/?q=${encodeURIComponent(searchQuery)}`);
      setUsers(response.data.results || []);
      setShowResults(true);
    } catch (error) {
      console.error('Error searching users:', error);
      setUsers([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const debounceTimer = setTimeout(() => {
      searchUsers(query);
    }, 300);

    return () => clearTimeout(debounceTimer);
  }, [query, searchUsers]);

  const handleUserSelect = (user: UserType) => {
    if (onUserSelect) {
      onUserSelect(user);
    }
    setShowResults(false);
    setQuery('');
  };

  const handleClickOutside = (e: React.MouseEvent) => {
    if (!(e.target as Element).closest('.user-search-container')) {
      setShowResults(false);
    }
  };

  useEffect(() => {
    document.addEventListener('click', handleClickOutside as any);
    return () => document.removeEventListener('click', handleClickOutside as any);
  }, []);

  return (
    <div className="user-search-container relative">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={placeholder}
          className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        {loading && (
          <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500"></div>
          </div>
        )}
      </div>

      {showResults && users.length > 0 && (
        <div className="absolute z-50 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-60 overflow-y-auto">
          {users.map((user) => (
            <div
              key={user.id}
              onClick={() => handleUserSelect(user)}
              className="p-3 hover:bg-gray-50 cursor-pointer border-b border-gray-100 last:border-b-0"
            >
              <div className="flex items-center space-x-3">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                    <User className="w-4 h-4 text-white" />
                  </div>
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center space-x-2">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {user.username}
                    </p>
                    {user.first_name && user.last_name && (
                      <span className="text-xs text-gray-500">
                        {user.first_name} {user.last_name}
                      </span>
                    )}
                  </div>
                  {showProfile && (
                    <div className="mt-1">
                      <p className="text-xs text-gray-500">{user.email}</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {showResults && query.length >= 2 && users.length === 0 && !loading && (
        <div className="absolute z-50 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg p-3">
          <p className="text-sm text-gray-500 text-center">No users found</p>
        </div>
      )}
    </div>
  );
};

export default UserSearch; 