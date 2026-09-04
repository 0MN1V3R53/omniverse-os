(function() {
    if (typeof window === 'undefined') return;

    // Helper: UUID v4 generator
    function uuidv4() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    // 1. Identity Management
    let visitorId = localStorage.getItem('omni_visitor_id');
    if (!visitorId) {
        visitorId = uuidv4();
        localStorage.setItem('omni_visitor_id', visitorId);
    }

    let sessionId = sessionStorage.getItem('omni_session_id');
    if (!sessionId) {
        sessionId = uuidv4();
        sessionStorage.setItem('omni_session_id', sessionId);
    }

    const startTime = Date.now();
    let events = [];

    // Helper: Determine Device Type
    function getDeviceType() {
        const ua = navigator.userAgent;
        if (/(tablet|ipad|playbook|silk)|(android(?!.*mobi))/i.test(ua)) {
            return 'Tablet';
        }
        if (/Mobile|Android|iP(hone|od)|IEMobile|BlackBerry|Kindle|Silk-Accelerated|(hpw|web)OS|Opera M(obi|ini)/.test(ua)) {
            return 'Mobile';
        }
        return 'Desktop';
    }

    // Prepare initial session payload
    const sessionPayload = {
        type: 'session_init',
        session_id: sessionId,
        visitor_id: visitorId,
        user_agent: navigator.userAgent,
        device_type: getDeviceType(),
        browser: (function() {
            const ua = navigator.userAgent;
            if (ua.includes('Chrome')) return 'Chrome';
            if (ua.includes('Safari')) return 'Safari';
            if (ua.includes('Firefox')) return 'Firefox';
            if (ua.includes('Edge')) return 'Edge';
            return 'Other';
        })(),
        os: navigator.platform,
        landing_page_route: window.location.pathname,
        referrer: document.referrer || '',
        screen_resolution: `${window.screen.width}x${window.screen.height}`
    };

    // Initialize session on server
    if (false) {
      fetch('/api/ingest_telemetry.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(sessionPayload)
      }).catch(console.error);
    }

    // 2. Event Listeners (The Funnel)
    document.addEventListener('click', function(e) {
        let target = e.target;
        while (target && target !== document.body) {
            if (target.tagName === 'A' && target.href && target.href.startsWith('tel:')) {
                setTimeout(() => {
                    logEvent('Conversion', 'Click_Call_Button', target.innerText || target.href);
                    // Ping save_call.php natively so Safari doesn't block the call
                    fetch('/api/save_call.php', { method: 'POST', body: JSON.stringify({ session_id: sessionId }) }).catch(function(){});
                }, 0);
                return;
            }
            if (target.tagName === 'BUTTON' || target.tagName === 'A') {
                logEvent('Navigation', 'Click', target.innerText || target.id || target.className);
                return;
            }
            target = target.parentNode;
        }
    });

    // We can also let the global click listener track general X/Y
    document.addEventListener('click', function(e) {
        if (!e.target.closest('a') && !e.target.closest('button')) {
            logEvent('Interaction', 'Click_Coords', `${e.clientX},${e.clientY}`);
        }
    });

    function logEvent(category, action, elementData) {
        const evt = {
            type: 'event',
            session_id: sessionId,
            event_category: category,
            event_action: action,
            element_data: elementData,
            timestamp: new Date().toISOString()
        };
        events.push(evt);

        // Send immediately to avoid losing it
        if (false) {
          fetch('/api/ingest_telemetry.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(evt)
          }).catch(console.error);
        }
    }

    // 3. Session Duration (sendBeacon)
    function sendDurationBeacon() {
        const durationSeconds = Math.floor((Date.now() - startTime) / 1000);
        const beaconData = JSON.stringify({
            type: 'session_duration',
            session_id: sessionId,
            duration_seconds: durationSeconds
        });
      if (false) {
        navigator.sendBeacon('/api/ingest_telemetry.php', beaconData);
      }
    }

    document.addEventListener('visibilitychange', function() {
        if (document.visibilityState === 'hidden') {
            sendDurationBeacon();
        }
    });
    window.addEventListener('pagehide', sendDurationBeacon);
    window.addEventListener('beforeunload', sendDurationBeacon);
})();
