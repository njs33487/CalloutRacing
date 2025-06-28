import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { userAPI } from '../services/api';
import { 
  MagnifyingGlassIcon,
  UserPlusIcon,
  UserMinusIcon,
  CheckIcon,
  XMarkIcon,
  ChatBubbleLeftIcon,
  MapPinIcon,
  TruckIcon,
  TrophyIcon
} from '@heroicons/react/24/outline';

interface User {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  profile: {
    id: number;
    bio: string;
    location: string;
    car_make: string;
    car_model: string;
    car_year: number;
    profile_picture: string;
    wins: number;
    losses: number;
    total_races: number;
    win_rate: number;
  };
}

interface Friendship {
  id: number;
  sender: {
    id: number;
    username: string;
    first_name: string;
    last_name: string;
    profile: {
      profile_picture: string;
      location: string;
      car_make: string;
      car_model: string;
    };
  };
  receiver: {
    id: number;
    username: string;
    first_name: string;
    last_name: string;
    profile: {
      profile_picture: string;
      location: string;
      car_make: string;
      car_model: string;
    };
  };
  status: 'pending' | 'accepted' | 'declined' | 'blocked';
  created_at: string;
}

export default function Friends() {
  const { user: authUser } = useAuth();
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<User[]>([]);
  const [friends, setFriends] = useState<User[]>([]);
  const [pendingRequests, setPendingRequests] = useState<Friendship[]>([]);
  const [sentRequests, setSentRequests] = useState<Friendship[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'friends' | 'requests' | 'search'>('friends');

  useEffect(() => {
    loadFriendsData();
  }, []);

  const loadFriendsData = async () => {
    try {
      setIsLoading(true);
      await Promise.all([
        loadFriends(),
        loadPendingRequests(),
        loadSentRequests()
      ]);
    } catch (error) {
      console.error('Error loading friends data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadFriends = async () => {
    try {
      const response = await userAPI.getFriends();
      setFriends(response.data);
    } catch (error) {
      console.error('Error loading friends:', error);
    }
  };

  const loadPendingRequests = async () => {
    try {
      const response = await userAPI.getPendingRequests();
      setPendingRequests(response.data);
    } catch (error) {
      console.error('Error loading pending requests:', error);
    }
  };

  const loadSentRequests = async () => {
    try {
      const response = await userAPI.getSentRequests();
      setSentRequests(response.data);
    } catch (error) {
      console.error('Error loading sent requests:', error);
    }
  };

  const searchUsers = async (query: string) => {
    if (query.trim().length < 2) {
      setSearchResults([]);
      return;
    }

    try {
      const response = await userAPI.searchUsers(query);
      setSearchResults(response.data);
    } catch (error) {
      console.error('Error searching users:', error);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    searchUsers(searchQuery);
  };

  const sendFriendRequest = async (userId: number) => {
    try {
      await userAPI.sendFriendRequest(userId);
      await loadSentRequests();
      // Remove from search results
      setSearchResults(prev => prev.filter(user => user.id !== userId));
    } catch (error) {
      console.error('Error sending friend request:', error);
      alert('Failed to send friend request. Please try again.');
    }
  };

  const acceptFriendRequest = async (friendshipId: number) => {
    try {
      await userAPI.acceptFriendRequest(friendshipId);
      await Promise.all([loadFriends(), loadPendingRequests()]);
    } catch (error) {
      console.error('Error accepting friend request:', error);
      alert('Failed to accept friend request. Please try again.');
    }
  };

  const declineFriendRequest = async (friendshipId: number) => {
    try {
      await userAPI.declineFriendRequest(friendshipId);
      await loadPendingRequests();
    } catch (error) {
      console.error('Error declining friend request:', error);
      alert('Failed to decline friend request. Please try again.');
    }
  };

  const removeFriend = async (userId: number) => {
    if (window.confirm('Are you sure you want to remove this friend?')) {
      try {
        await userAPI.removeFriend(userId);
        await loadFriends();
      } catch (error) {
        console.error('Error removing friend:', error);
        alert('Failed to remove friend. Please try again.');
      }
    }
  };

  const cancelFriendRequest = async (friendshipId: number) => {
    try {
      await userAPI.cancelFriendRequest(friendshipId);
      await loadSentRequests();
    } catch (error) {
      console.error('Error canceling friend request:', error);
      alert('Failed to cancel friend request. Please try again.');
    }
  };

  const getOtherUser = (friendship: Friendship) => {
    return friendship.sender.id === authUser?.id ? friendship.receiver : friendship.sender;
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Friends</h1>
        <p className="text-gray-600">Connect with other racers and manage your friendships</p>
      </div>

      {/* Search Bar */}
      <div className="mb-8">
        <form onSubmit={handleSearch} className="flex gap-4">
          <div className="flex-1 relative">
            <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search for racers by username, name, or location..."
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>
          <button
            type="submit"
            className="bg-primary-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-primary-700"
          >
            Search
          </button>
        </form>
      </div>

      {/* Tabs */}
      <div className="mb-6">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            <button
              onClick={() => setActiveTab('friends')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'friends'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Friends ({friends.length})
            </button>
            <button
              onClick={() => setActiveTab('requests')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'requests'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Requests ({pendingRequests.length})
            </button>
            <button
              onClick={() => setActiveTab('search')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'search'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Search Results ({searchResults.length})
            </button>
          </nav>
        </div>
      </div>

      {/* Friends Tab */}
      {activeTab === 'friends' && (
        <div>
          {friends.length === 0 ? (
            <div className="text-center py-12">
              <UserPlusIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No friends yet</h3>
              <p className="text-gray-600">Start connecting with other racers to build your network!</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {friends.map((friend) => (
                <div key={friend.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <div className="flex items-center mb-4">
                    <div className="w-12 h-12 rounded-full bg-gray-200 mr-3 overflow-hidden">
                      {friend.profile.profile_picture ? (
                        <img 
                          src={friend.profile.profile_picture} 
                          alt="Profile" 
                          className="w-full h-full object-cover"
                        />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center text-sm font-medium text-gray-600">
                          {friend.first_name[0]}
                        </div>
                      )}
                    </div>
                    <div className="flex-1">
                      <h3 className="font-medium text-gray-900">
                        {friend.first_name} {friend.last_name}
                      </h3>
                      <p className="text-sm text-gray-600">@{friend.username}</p>
                    </div>
                    <button
                      onClick={() => removeFriend(friend.id)}
                      className="text-red-500 hover:text-red-700"
                      title="Remove friend"
                    >
                      <UserMinusIcon className="w-5 h-5" />
                    </button>
                  </div>
                  
                  {friend.profile.location && (
                    <div className="flex items-center text-sm text-gray-600 mb-2">
                      <MapPinIcon className="w-4 h-4 mr-1" />
                      <span>{friend.profile.location}</span>
                    </div>
                  )}
                  
                  {(friend.profile.car_make || friend.profile.car_model) && (
                    <div className="flex items-center text-sm text-gray-600 mb-3">
                      <TruckIcon className="w-4 h-4 mr-1" />
                      <span>
                        {friend.profile.car_year} {friend.profile.car_make} {friend.profile.car_model}
                      </span>
                    </div>
                  )}
                  
                  <div className="flex items-center justify-between text-sm">
                    <div className="flex items-center text-gray-600">
                      <TrophyIcon className="w-4 h-4 mr-1" />
                      <span>{friend.profile.wins} wins</span>
                    </div>
                    <span className="text-gray-500">
                      {friend.profile.win_rate.toFixed(1)}% win rate
                    </span>
                  </div>
                  
                  <div className="mt-4 flex space-x-2">
                    <button className="flex-1 bg-primary-600 text-white py-2 px-3 rounded text-sm font-medium hover:bg-primary-700">
                      <ChatBubbleLeftIcon className="w-4 h-4 inline mr-1" />
                      Message
                    </button>
                    <button className="flex-1 bg-gray-100 text-gray-700 py-2 px-3 rounded text-sm font-medium hover:bg-gray-200">
                      View Profile
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Requests Tab */}
      {activeTab === 'requests' && (
        <div className="space-y-6">
          {/* Pending Requests */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">Pending Requests</h3>
            {pendingRequests.length === 0 ? (
              <p className="text-gray-600">No pending friend requests</p>
            ) : (
              <div className="space-y-4">
                {pendingRequests.map((friendship) => {
                  const requester = getOtherUser(friendship);
                  return (
                    <div key={friendship.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center">
                          <div className="w-10 h-10 rounded-full bg-gray-200 mr-3 overflow-hidden">
                            {requester.profile.profile_picture ? (
                              <img 
                                src={requester.profile.profile_picture} 
                                alt="Profile" 
                                className="w-full h-full object-cover"
                              />
                            ) : (
                              <div className="w-full h-full flex items-center justify-center text-sm font-medium text-gray-600">
                                {requester.first_name[0]}
                              </div>
                            )}
                          </div>
                          <div>
                            <h4 className="font-medium text-gray-900">
                              {requester.first_name} {requester.last_name}
                            </h4>
                            <p className="text-sm text-gray-600">@{requester.username}</p>
                            {requester.profile.location && (
                              <p className="text-sm text-gray-500">{requester.profile.location}</p>
                            )}
                          </div>
                        </div>
                        <div className="flex space-x-2">
                          <button
                            onClick={() => acceptFriendRequest(friendship.id)}
                            className="bg-green-500 text-white p-2 rounded-full hover:bg-green-600"
                            title="Accept request"
                          >
                            <CheckIcon className="w-4 h-4" />
                          </button>
                          <button
                            onClick={() => declineFriendRequest(friendship.id)}
                            className="bg-red-500 text-white p-2 rounded-full hover:bg-red-600"
                            title="Decline request"
                          >
                            <XMarkIcon className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          {/* Sent Requests */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">Sent Requests</h3>
            {sentRequests.length === 0 ? (
              <p className="text-gray-600">No sent friend requests</p>
            ) : (
              <div className="space-y-4">
                {sentRequests.map((friendship) => {
                  const recipient = getOtherUser(friendship);
                  return (
                    <div key={friendship.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center">
                          <div className="w-10 h-10 rounded-full bg-gray-200 mr-3 overflow-hidden">
                            {recipient.profile.profile_picture ? (
                              <img 
                                src={recipient.profile.profile_picture} 
                                alt="Profile" 
                                className="w-full h-full object-cover"
                              />
                            ) : (
                              <div className="w-full h-full flex items-center justify-center text-sm font-medium text-gray-600">
                                {recipient.first_name[0]}
                              </div>
                            )}
                          </div>
                          <div>
                            <h4 className="font-medium text-gray-900">
                              {recipient.first_name} {recipient.last_name}
                            </h4>
                            <p className="text-sm text-gray-600">@{recipient.username}</p>
                            <p className="text-sm text-gray-500">Request sent {new Date(friendship.created_at).toLocaleDateString()}</p>
                          </div>
                        </div>
                        <button
                          onClick={() => cancelFriendRequest(friendship.id)}
                          className="text-red-500 hover:text-red-700"
                          title="Cancel request"
                        >
                          <XMarkIcon className="w-5 h-5" />
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Search Results Tab */}
      {activeTab === 'search' && (
        <div>
          {searchResults.length === 0 ? (
            <div className="text-center py-12">
              <MagnifyingGlassIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No results found</h3>
              <p className="text-gray-600">Try searching with different keywords</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {searchResults.map((user) => (
                <div key={user.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <div className="flex items-center mb-4">
                    <div className="w-12 h-12 rounded-full bg-gray-200 mr-3 overflow-hidden">
                      {user.profile.profile_picture ? (
                        <img 
                          src={user.profile.profile_picture} 
                          alt="Profile" 
                          className="w-full h-full object-cover"
                        />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center text-sm font-medium text-gray-600">
                          {user.first_name[0]}
                        </div>
                      )}
                    </div>
                    <div className="flex-1">
                      <h3 className="font-medium text-gray-900">
                        {user.first_name} {user.last_name}
                      </h3>
                      <p className="text-sm text-gray-600">@{user.username}</p>
                    </div>
                  </div>
                  
                  {user.profile.location && (
                    <div className="flex items-center text-sm text-gray-600 mb-2">
                      <MapPinIcon className="w-4 h-4 mr-1" />
                      <span>{user.profile.location}</span>
                    </div>
                  )}
                  
                  {(user.profile.car_make || user.profile.car_model) && (
                    <div className="flex items-center text-sm text-gray-600 mb-3">
                      <TruckIcon className="w-4 h-4 mr-1" />
                      <span>
                        {user.profile.car_year} {user.profile.car_make} {user.profile.car_model}
                      </span>
                    </div>
                  )}
                  
                  <div className="flex items-center justify-between text-sm mb-4">
                    <div className="flex items-center text-gray-600">
                      <TrophyIcon className="w-4 h-4 mr-1" />
                      <span>{user.profile.wins} wins</span>
                    </div>
                    <span className="text-gray-500">
                      {user.profile.win_rate.toFixed(1)}% win rate
                    </span>
                  </div>
                  
                  <button
                    onClick={() => sendFriendRequest(user.id)}
                    className="w-full bg-primary-600 text-white py-2 px-3 rounded text-sm font-medium hover:bg-primary-700 flex items-center justify-center"
                  >
                    <UserPlusIcon className="w-4 h-4 mr-1" />
                    Add Friend
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
} 