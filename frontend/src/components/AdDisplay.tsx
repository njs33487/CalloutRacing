import React, { useEffect } from 'react';

interface AdDisplayProps {
  adSlot: string;
  adFormat?: string; // 'auto', 'fluid', 'rectangle', etc.
  adLayout?: string; // 'in-article', 'display', etc.
}

const AdDisplay: React.FC<AdDisplayProps> = ({ adSlot, adFormat = 'auto', adLayout }) => {
  useEffect(() => {
    // Only load AdSense script once globally
    if (!(window as any).adsbygoogle) {
      const script = document.createElement('script');
      script.src = `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=YOUR_ADSENSE_CLIENT_ID`;
      script.async = true;
      script.crossOrigin = "anonymous";
      document.head.appendChild(script);
      (window as any).adsbygoogle = (window as any).adsbygoogle || [];
    }
    try {
      ((window as any).adsbygoogle = (window as any).adsbygoogle || []).push({});
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error("Error pushing ad to AdSense:", e);
    }
  }, [adSlot]);

  return (
    <div style={{ textAlign: 'center', margin: '20px 0' }}>
      <ins
        className="adsbygoogle"
        style={{ display: 'block' }}
        data-ad-client="YOUR_ADSENSE_CLIENT_ID"
        data-ad-slot={adSlot}
        data-ad-format={adFormat}
        data-full-width-responsive="true"
        data-ad-layout={adLayout}
      ></ins>
    </div>
  );
};

export default AdDisplay; 