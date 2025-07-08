import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

interface SEOHeadProps {
  title?: string;
  description?: string;
  keywords?: string;
  image?: string;
  url?: string;
  type?: 'website' | 'article' | 'event';
  structuredData?: object;
}

const SEOHead: React.FC<SEOHeadProps> = ({
  title = 'CalloutRacing - Ultimate Racing Community Platform',
  description = 'Join the ultimate racing community! Find drag racing events, challenge other racers, discover tracks and hotspots, buy/sell cars, and connect with car enthusiasts nationwide.',
  keywords = 'racing, drag racing, car community, racing events, car meets, race tracks, car enthusiasts, automotive, motorsports, racing platform, car marketplace, racing hotspots',
  image = '/android-chrome-192x192.png',
  url,
  type = 'website',
  structuredData
}) => {
  const location = useLocation();
  const currentUrl = url || `https://calloutracing.com${location.pathname}`;

  useEffect(() => {
    // Update document title
    document.title = title;

    // Update meta tags
    updateMetaTag('name', 'description', description);
    updateMetaTag('name', 'keywords', keywords);
    updateMetaTag('property', 'og:title', title);
    updateMetaTag('property', 'og:description', description);
    updateMetaTag('property', 'og:url', currentUrl);
    updateMetaTag('property', 'og:image', `https://calloutracing.com${image}`);
    updateMetaTag('property', 'og:type', type);
    updateMetaTag('name', 'twitter:title', title);
    updateMetaTag('name', 'twitter:description', description);
    updateMetaTag('name', 'twitter:image', `https://calloutracing.com${image}`);

    // Update canonical URL
    updateCanonicalUrl(currentUrl);

    // Add structured data if provided
    if (structuredData) {
      addStructuredData(structuredData);
    }

    // Cleanup function
    return () => {
      // Remove any added structured data on unmount
      const existingScript = document.querySelector('script[data-seo-structured]');
      if (existingScript) {
        existingScript.remove();
      }
    };
  }, [title, description, keywords, image, currentUrl, type, structuredData]);

  const updateMetaTag = (attribute: string, value: string, content: string) => {
    let meta = document.querySelector(`meta[${attribute}="${value}"]`) as HTMLMetaElement;
    if (!meta) {
      meta = document.createElement('meta');
      meta.setAttribute(attribute, value);
      document.head.appendChild(meta);
    }
    meta.setAttribute('content', content);
  };

  const updateCanonicalUrl = (url: string) => {
    let canonical = document.querySelector('link[rel="canonical"]') as HTMLLinkElement;
    if (!canonical) {
      canonical = document.createElement('link');
      canonical.setAttribute('rel', 'canonical');
      document.head.appendChild(canonical);
    }
    canonical.setAttribute('href', url);
  };

  const addStructuredData = (data: object) => {
    // Remove existing structured data
    const existingScript = document.querySelector('script[data-seo-structured]');
    if (existingScript) {
      existingScript.remove();
    }

    // Add new structured data
    const script = document.createElement('script');
    script.setAttribute('type', 'application/ld+json');
    script.setAttribute('data-seo-structured', 'true');
    script.textContent = JSON.stringify(data);
    document.head.appendChild(script);
  };

  return null; // This component doesn't render anything
};

export default SEOHead;

// Predefined SEO configurations for different pages
export const SEOConfigs = {
  home: {
    title: 'CalloutRacing - Ultimate Racing Community Platform | Find Events, Challenge Racers',
    description: 'Join the ultimate racing community! Find drag racing events, challenge other racers, discover tracks and hotspots, buy/sell cars, and connect with car enthusiasts nationwide.',
    keywords: 'racing, drag racing, car community, racing events, car meets, race tracks, car enthusiasts, automotive, motorsports, racing platform, car marketplace, racing hotspots',
    structuredData: {
      '@context': 'https://schema.org',
      '@type': 'WebSite',
      'name': 'CalloutRacing',
      'url': 'https://calloutracing.com',
      'description': 'Ultimate racing community platform for finding events, challenging racers, and connecting with car enthusiasts',
      'potentialAction': {
        '@type': 'SearchAction',
        'target': 'https://calloutracing.com/search?q={search_term_string}',
        'query-input': 'required name=search_term_string'
      }
    }
  },
  callouts: {
    title: 'Racing Callouts - Challenge Racers | CalloutRacing',
    description: 'Find and create racing callouts. Challenge other racers, set up races, and compete in the ultimate racing community.',
    keywords: 'racing callouts, challenge racers, drag racing challenges, race setup, racing competition',
    structuredData: {
      '@context': 'https://schema.org',
      '@type': 'ItemList',
      'name': 'Racing Callouts',
      'description': 'Active racing challenges and callouts'
    }
  },
  events: {
    title: 'Racing Events - Find Drag Racing Events | CalloutRacing',
    description: 'Discover upcoming racing events, drag racing competitions, and car meets near you. Join the racing community.',
    keywords: 'racing events, drag racing events, car meets, racing competitions, motorsports events',
    structuredData: {
      '@context': 'https://schema.org',
      '@type': 'ItemList',
      'name': 'Racing Events',
      'description': 'Upcoming racing events and competitions'
    }
  },
  tracks: {
    title: 'Race Tracks - Find Racing Tracks Near You | CalloutRacing',
    description: 'Discover race tracks, drag strips, and racing facilities near you. Find the perfect track for your next race.',
    keywords: 'race tracks, drag strips, racing facilities, track locations, racing venues',
    structuredData: {
      '@context': 'https://schema.org',
      '@type': 'ItemList',
      'name': 'Race Tracks',
      'description': 'Racing tracks and facilities'
    }
  },
  marketplace: {
    title: 'Racing Marketplace - Buy Sell Racing Cars | CalloutRacing',
    description: 'Buy and sell racing cars, parts, and equipment in the racing community marketplace. Find your next race car.',
    keywords: 'racing marketplace, buy racing cars, sell racing cars, racing parts, automotive marketplace',
    structuredData: {
      '@context': 'https://schema.org',
      '@type': 'ItemList',
      'name': 'Racing Marketplace',
      'description': 'Racing cars, parts, and equipment for sale'
    }
  },
  social: {
    title: 'Racing Social Network - Connect with Racers | CalloutRacing',
    description: 'Connect with fellow racers, share racing content, and build your racing network in the ultimate racing social platform.',
    keywords: 'racing social network, connect with racers, racing community, car enthusiasts social',
    structuredData: {
      '@context': 'https://schema.org',
      '@type': 'ItemList',
      'name': 'Racing Social Feed',
      'description': 'Racing community social content'
    }
  }
}; 