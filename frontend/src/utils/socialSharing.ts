// Social sharing utilities for CalloutRacing

export interface ShareData {
  title: string;
  description: string;
  url: string;
  image?: string;
  type: 'event' | 'callout';
}

export const shareToFacebook = (data: ShareData) => {
  const shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(data.url)}`;
  window.open(shareUrl, '_blank', 'width=600,height=400');
};

export const shareToTwitter = (data: ShareData) => {
  const text = `${data.title} - ${data.description}`;
  const shareUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(data.url)}`;
  window.open(shareUrl, '_blank', 'width=600,height=400');
};

export const shareToWhatsApp = (data: ShareData) => {
  const text = `${data.title} - ${data.description} ${data.url}`;
  const shareUrl = `https://wa.me/?text=${encodeURIComponent(text)}`;
  window.open(shareUrl, '_blank');
};

export const copyToClipboard = async (url: string): Promise<boolean> => {
  try {
    await navigator.clipboard.writeText(url);
    return true;
  } catch (error) {
    console.error('Failed to copy to clipboard:', error);
    return false;
  }
};

export const generateShareUrl = (type: 'event' | 'callout', id: number): string => {
  const baseUrl = window.location.origin;
  return `${baseUrl}/share/${type}/${id}`;
};

export const generateEventShareData = (event: any): ShareData => {
  const shareUrl = generateShareUrl('event', event.id);
  
  return {
    title: event.title,
    description: `${event.description.substring(0, 100)}... - Join us at ${event.track?.name || 'TBD'} on ${new Date(event.start_date).toLocaleDateString()}`,
    url: shareUrl,
            image: event.images?.[0]?.image || '/android-chrome-192x192.png',
    type: 'event'
  };
};

export const generateCalloutShareData = (callout: any): ShareData => {
  const shareUrl = generateShareUrl('callout', callout.id);
  
  const challengerName = `${callout.challenger.first_name} ${callout.challenger.last_name}`;
  const challengedName = `${callout.challenged.first_name} ${callout.challenged.last_name}`;
  
  return {
    title: `Race Challenge: ${challengerName} vs ${challengedName}`,
    description: `${callout.race_type.replace('_', ' ').toUpperCase()} race at ${callout.track?.name || callout.street_location || 'TBD'} - ${callout.message.substring(0, 100)}...`,
    url: shareUrl,
            image: callout.images?.[0]?.image || '/android-chrome-192x192.png',
    type: 'callout'
  };
};

export const updateMetaTags = (data: ShareData) => {
  // Update Open Graph meta tags
  const ogTitle = document.querySelector('meta[property="og:title"]');
  if (ogTitle) ogTitle.setAttribute('content', data.title);
  
  const ogDescription = document.querySelector('meta[property="og:description"]');
  if (ogDescription) ogDescription.setAttribute('content', data.description);
  
  const ogUrl = document.querySelector('meta[property="og:url"]');
  if (ogUrl) ogUrl.setAttribute('content', data.url);
  
  const ogImage = document.querySelector('meta[property="og:image"]');
  if (ogImage && data.image) ogImage.setAttribute('content', data.image);
  
  const ogType = document.querySelector('meta[property="og:type"]');
  if (ogType) ogType.setAttribute('content', 'website');
  
  // Update Twitter Card meta tags
  const twitterCard = document.querySelector('meta[name="twitter:card"]');
  if (twitterCard) twitterCard.setAttribute('content', 'summary_large_image');
  
  const twitterTitle = document.querySelector('meta[name="twitter:title"]');
  if (twitterTitle) twitterTitle.setAttribute('content', data.title);
  
  const twitterDescription = document.querySelector('meta[name="twitter:description"]');
  if (twitterDescription) twitterDescription.setAttribute('content', data.description);
  
  const twitterImage = document.querySelector('meta[name="twitter:image"]');
  if (twitterImage && data.image) twitterImage.setAttribute('content', data.image);
  
  // Update page title
  document.title = data.title;
}; 