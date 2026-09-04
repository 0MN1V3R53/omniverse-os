'use client';

import { useEffect } from 'react';
import { usePathname } from 'next/navigation';

export default function OmniTracker() {
  const pathname = usePathname();

  useEffect(() => {
    // 1. Identity Management
    function uuidv4() {
      return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
      });
    }

    let visitorId = localStorage.getItem('omni_visitor_id');
    if (!visitorId) {
      visitorId = uuidv4();
      localStorage.setItem('omni_visitor_id', visitorId);
    }

    let sessionId = sessionStorage.getItem('omni_session_id');
    let isNewSession = false;
    if (!sessionId) {
      sessionId = uuidv4();
      sessionStorage.setItem('omni_session_id', sessionId);
      isNewSession = true;
    }

    const startTime = Date.now();

    function getDeviceType() {
      const ua = navigator.userAgent;
      if (/(tablet|ipad|playbook|silk)|(android(?!.*mobi))/i.test(ua)) return 'Tablet';
      if (/Mobile|Android|iP(hone|od)|IEMobile|BlackBerry|Kindle|Silk-Accelerated|(hpw|web)OS|Opera M(obi|ini)/.test(ua)) return 'Mobile';
      return 'Desktop';
    }

    function getBrowser() {
      const ua = navigator.userAgent;
      if (ua.includes('Chrome')) return 'Chrome';
      if (ua.includes('Safari') && !ua.includes('Chrome')) return 'Safari';
      if (ua.includes('Firefox')) return 'Firefox';
      if (ua.includes('Edge')) return 'Edge';
      return 'Other';
    }

    // Initialize session if new
    if (isNewSession) {
      const sessionPayload = {
        type: 'session_init',
        session_id: sessionId,
        visitor_id: visitorId,
        user_agent: navigator.userAgent,
        device_type: getDeviceType(),
        browser: getBrowser(),
        os: navigator.platform,
        landing_page_route: window.location.pathname,
        referrer: document.referrer || ''
      };
      
      if (false) {
        fetch('https://www.skyautoservices.com/api/ingest_telemetry.php', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(sessionPayload)
        }).catch(console.error);
      }
    }

    // Send Duration Beacon
    function sendDurationBeacon() {
      const durationSeconds = Math.floor((Date.now() - startTime) / 1000);
      const beaconData = JSON.stringify({
        type: 'session_duration',
        session_id: sessionId,
        duration_seconds: durationSeconds
      });
      if (false) {
        navigator.sendBeacon('https://www.skyautoservices.com/api/ingest_telemetry.php', beaconData);
      }
    }

    const visibilityHandler = () => {
      if (document.visibilityState === 'hidden') sendDurationBeacon();
    };
    
    document.addEventListener('visibilitychange', visibilityHandler);
    window.addEventListener('pagehide', sendDurationBeacon);
    window.addEventListener('beforeunload', sendDurationBeacon);

    // Global Click Listener for Events
    const clickHandler = (e) => {
      let target = e.target;
      while (target && target !== document.body) {
        if (target.tagName === 'A' && target.href && target.href.startsWith('tel:')) {
          if (typeof window !== "undefined" && typeof window.gtag === "function") {
            try {
              window.gtag('event', 'conversion', {
                'send_to': 'AW-18396293415',
                'event_category': 'Phone Call',
                'event_label': target.innerText || target.href
              });
              window.gtag('event', 'phone_call_lead', {
                'phone_number': target.innerText || '224-449-0397'
              });
            } catch (e) {}
          }
          setTimeout(() => logEvent('Conversion', 'Click_Call_Button', target.innerText || target.href), 0);
          return;
        }
        if (target.tagName === 'BUTTON' || target.tagName === 'A') {
          logEvent('Navigation', 'Click', target.innerText || target.id || target.className);
          return;
        }
        target = target.parentNode;
      }
    };

    document.addEventListener('click', clickHandler);

    function logEvent(category, action, elementData) {
      const evt = {
        type: 'event',
        session_id: sessionId,
        event_category: category,
        event_action: action,
        element_data: elementData,
        timestamp: new Date().toISOString()
      };
      if (false) {
        fetch('https://www.skyautoservices.com/api/ingest_telemetry.php', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(evt)
        }).catch(console.error);
      }
    }

    // Cleanup
    return () => {
      document.removeEventListener('visibilitychange', visibilityHandler);
      window.removeEventListener('pagehide', sendDurationBeacon);
      window.removeEventListener('beforeunload', sendDurationBeacon);
      document.removeEventListener('click', clickHandler);
    };
  }, []);

  // Track page views on route change
  useEffect(() => {
    let sessionId = sessionStorage.getItem('omni_session_id');
    if (sessionId) {
      if (false) {
        fetch('https://www.skyautoservices.com/api/ingest_telemetry.php', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            type: 'pageview',
            session_id: sessionId,
            route_path: pathname,
            timestamp: new Date().toISOString()
          })
        }).catch(console.error);
      }
    }
  }, [pathname]);

  return null;
}
