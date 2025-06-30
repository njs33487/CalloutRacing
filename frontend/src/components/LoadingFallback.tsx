interface LoadingFallbackProps {
  message?: string;
  size?: 'sm' | 'md' | 'lg';
  fullScreen?: boolean;
}

export default function LoadingFallback({ 
  message = 'Loading...', 
  size = 'md',
  fullScreen = false 
}: LoadingFallbackProps) {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12'
  };

  const spinner = (
    <div className="flex flex-col items-center justify-center space-y-4">
      <div className={`animate-spin rounded-full border-b-2 border-primary-600 ${sizeClasses[size]}`}></div>
      <p className="text-gray-600 text-sm">{message}</p>
    </div>
  );

  if (fullScreen) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-lg shadow-lg p-8">
          {spinner}
        </div>
      </div>
    );
  }

  return (
    <div className="flex items-center justify-center p-8">
      {spinner}
    </div>
  );
}

// Specialized loading components
export function PageLoadingFallback() {
  return <LoadingFallback message="Loading page..." size="lg" fullScreen />;
}

export function ComponentLoadingFallback() {
  return <LoadingFallback message="Loading..." size="md" />;
}

export function ButtonLoadingFallback() {
  return <LoadingFallback message="" size="sm" />;
} 