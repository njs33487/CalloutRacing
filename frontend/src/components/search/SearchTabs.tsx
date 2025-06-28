interface SearchTabsProps {
  activeTab: 'all' | 'users' | 'events' | 'marketplace' | 'tracks' | 'callouts';
  setActiveTab: (tab: 'all' | 'users' | 'events' | 'marketplace' | 'tracks' | 'callouts') => void;
  resultCounts: {
    all: number;
    users: number;
    events: number;
    marketplace: number;
    tracks: number;
    callouts: number;
  };
}

export default function SearchTabs({ activeTab, setActiveTab, resultCounts }: SearchTabsProps) {
  const tabs = [
    { id: 'all', label: 'All', count: resultCounts.all },
    { id: 'users', label: 'Users', count: resultCounts.users },
    { id: 'events', label: 'Events', count: resultCounts.events },
    { id: 'marketplace', label: 'Marketplace', count: resultCounts.marketplace },
    { id: 'tracks', label: 'Tracks', count: resultCounts.tracks },
    { id: 'callouts', label: 'Callouts', count: resultCounts.callouts },
  ] as const;

  return (
    <div className="border-b border-gray-200 mb-6">
      <nav className="-mb-px flex space-x-8">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`py-2 px-1 border-b-2 font-medium text-sm whitespace-nowrap ${
              activeTab === tab.id
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            {tab.label}
            {tab.count > 0 && (
              <span className="ml-2 bg-gray-100 text-gray-900 py-0.5 px-2.5 rounded-full text-xs">
                {tab.count}
              </span>
            )}
          </button>
        ))}
      </nav>
    </div>
  );
} 