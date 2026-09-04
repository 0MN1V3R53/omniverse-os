"use client";
import { useEffect } from 'react';

export default function ClientTelemetry() {
  useEffect(() => {
    // Generate or retrieve persistent Session ID
    let sessionId = localStorage.getItem('omni_session_id');
    if (!sessionId) {
      sessionId = 'SESS-' + Date.now() + '-' + Math.floor(Math.random() * 1000000);
      localStorage.setItem('omni_session_id', sessionId);
    }
    
    // Store in window for save_quote and save_call to access
    window.OMNI_SESSION_ID = sessionId;

    const sessionStart = Date.now();
    let clicks = [];

    const sendTelemetry = (eventType, extraData = {}) => {
      const payload = {
        session_id: sessionId,
        event_type: eventType,
        user_agent: navigator.userAgent,
        screen_resolution: `${window.screen.width}x${window.screen.height}`,
        device_type: /Mobi|Android/i.test(navigator.userAgent) ? 'Mobile' : 'Desktop',
        page_url: window.location.href,
        session_duration_sec: Math.floor((Date.now() - sessionStart) / 1000),
        clicks: clicks,
        ...extraData
      };

      if (navigator.sendBeacon && (eventType === 'beforeunload' || eventType === 'visibilitychange')) {
        navigator.sendBeacon('https://www.skyautoservices.com/api/telemetry.php', JSON.stringify(payload));
      } else {
        fetch('https://www.skyautoservices.com/api/telemetry.php', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
          keepalive: true
        }).catch(err => console.error('Telemetry Error:', err));
      }
      
      clicks = [];
    };

    const clickHandler = (e) => {
      const target = e.target.closest('a, button, input') || e.target;
      const isTel = target.tagName === 'A' && target.href?.includes('tel:');
      const isQuote = target.closest('form');
      
      clicks.push({
        x: e.clientX,
        y: e.clientY,
        tag: target.tagName,
        id: target.id || 'none',
        text: target.innerText?.trim().substring(0, 50) || target.value || 'none',
        is_call: !!isTel,
        is_quote: !!isQuote,
        timestamp: new Date().toISOString()
      });

      if (clicks.length >= 5 || isTel) {
        setTimeout(() => sendTelemetry('click_batch'), 0);
      }
    };

    const visibilityHandler = () => {
      if (document.visibilityState === 'hidden') sendTelemetry('visibilitychange');
    };
    const unloadHandler = () => sendTelemetry('beforeunload');

    document.addEventListener('click', clickHandler);
    document.addEventListener('visibilitychange', visibilityHandler);
    window.addEventListener('beforeunload', unloadHandler);

    sendTelemetry('page_load');

    return () => {
      document.removeEventListener('click', clickHandler);
      document.removeEventListener('visibilitychange', visibilityHandler);
      window.removeEventListener('beforeunload', unloadHandler);
    };
  }, []);

  return null;
}
