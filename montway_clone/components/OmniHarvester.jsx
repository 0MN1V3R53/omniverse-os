'use client';

import { useEffect, useRef } from 'react';

export default function OmniHarvester() {
  const batchQueue = useRef([]);
  const visitorId = useRef('');
  const sessionId = useRef('');

  useEffect(() => {
    // 1. Identity Management
    let vid = localStorage.getItem('panopticon_vid');
    if (!vid) {
      vid = 'v_' + crypto.randomUUID();
      localStorage.setItem('panopticon_vid', vid);
    }
    visitorId.current = vid;

    let sid = sessionStorage.getItem('panopticon_sid');
    if (!sid) {
      sid = 's_' + crypto.randomUUID();
      sessionStorage.setItem('panopticon_sid', sid);
    }
    sessionId.current = sid;

    // Helper to add events to batch
    const logEvent = (department, eventType, targetElement, payload = {}) => {
      batchQueue.current.push({
        timestamp: new Date().toISOString(),
        department,
        event_type: eventType,
        target_element: targetElement,
        json_payload: JSON.stringify(payload)
      });
    };

    // 2. Global Event Listeners
    const handleClick = (e) => {
      let target = e.target;
      let depth = 0;
      // Find nearest meaningful element
      while (target && target !== document.body && depth < 3) {
        if (target.tagName === 'A' || target.tagName === 'BUTTON' || target.onclick) break;
        target = target.parentElement;
        depth++;
      }
      
      const tag = target?.tagName || 'UNKNOWN';
      const text = target?.innerText?.trim().substring(0, 50) || '';
      const id = target?.id || '';
      
      const targetStr = `${tag}${id ? '#' + id : ''}${text ? ' ("' + text + '")' : ''}`;
      
      // Determine department
      let dept = 'UX_Behavior_Dept';
      if (target?.tagName === 'A' && target.href?.includes('tel:')) dept = 'Sales_CRM_Dept';
      if (targetStr.toLowerCase().includes('quote')) dept = 'Sales_CRM_Dept';

      logEvent(dept, 'Click', targetStr, {
        x: e.clientX,
        y: e.clientY
      });
    };

    const handleFocusIn = (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') {
        const id = e.target.id || e.target.name || 'unknown_input';
        logEvent('UX_Behavior_Dept', 'Focus', `INPUT#${id}`, {
          type: e.target.type
        });
      }
    };

    // Scroll tracking
    const scrollMilestones = new Set();
    const handleScroll = () => {
      const scrollY = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const scrollPercent = docHeight > 0 ? (scrollY / docHeight) * 100 : 0;

      [25, 50, 100].forEach(milestone => {
        if (scrollPercent >= milestone && !scrollMilestones.has(milestone)) {
          scrollMilestones.add(milestone);
          logEvent('UX_Behavior_Dept', 'ScrollDepth', `Milestone_${milestone}%`, { percent: milestone });
        }
      });
    };

    document.addEventListener('click', handleClick);
    document.addEventListener('focusin', handleFocusIn);
    window.addEventListener('scroll', handleScroll, { passive: true });

    // Initial page view event
    logEvent('SEO_Acquisition_Dept', 'PageView', window.location.pathname, {
      referrer: document.referrer,
      userAgent: navigator.userAgent
    });

    // 3. Data Transmission (5 seconds interval)
    const flushBatch = () => {
      if (batchQueue.current.length === 0) return;
      
      const payload = {
        visitor_id: visitorId.current,
        session_id: sessionId.current,
        url: window.location.href,
        referrer: document.referrer,
        user_agent: navigator.userAgent,
        events: [...batchQueue.current]
      };
      
      batchQueue.current = []; // Clear queue

      // Determine correct API URL depending on environment
      // Assumes Hostinger or local backend is reachable at the same host /api
      const endpoint = 'https://www.skyautoservices.com/api/ingest_stream.php'; 
      // Using fetch with keepalive or sendBeacon
      if (false) {
        try {
          navigator.sendBeacon(endpoint, JSON.stringify(payload));
        } catch (err) {
          fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
            keepalive: true
          }).catch(e => console.error(e));
        }
      }
    };

    const intervalId = setInterval(flushBatch, 5000);

    const handleBeforeUnload = () => {
      flushBatch();
    };
    window.addEventListener('beforeunload', handleBeforeUnload);

    return () => {
      document.removeEventListener('click', handleClick);
      document.removeEventListener('focusin', handleFocusIn);
      window.removeEventListener('scroll', handleScroll);
      window.removeEventListener('beforeunload', handleBeforeUnload);
      clearInterval(intervalId);
    };
  }, []);

  return null; // Headless component
}
