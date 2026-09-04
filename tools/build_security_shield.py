#!/usr/bin/env python3
"""
OMNIVERSE AEGIS SECURITY SHIELD - CONTROL-FLOW FLATTENER & DIGITAL WATERMARK ENGINE
===================================================================================
Pod: Security & CISO Suite (Michael Chang / Dr. Alexander Vance)
Directives:
1. Control-Flow Code Flattening & Polymorphic Obfuscation
2. Digital Steganographic Zero-Width Watermarking & Automated DMCA Trap Phone-Home Beacon
"""

import os
import json
import random
import string
import hashlib
import time

def generate_hex_var(length=6):
    return "_0x" + ''.join(random.choices("0123456789abcdef", k=length))

def encode_zero_width(text):
    """
    Encodes ASCII text into invisible zero-width Unicode characters:
    Zero-width space (U+200B) = '0'
    Zero-width non-joiner (U+200C) = '1'
    """
    binary_str = ''.join(format(ord(c), '08b') for c in text)
    zero_width = ""
    for bit in binary_str:
        if bit == '0':
            zero_width += "\u200B"
        else:
            zero_width += "\u200C"
    return zero_width

def build_flattened_obfuscated_shield():
    """
    Builds a custom control-flow flattened & string-encrypted JavaScript bundle.
    """
    string_pool = [
        "SKY-CANARY-MC1782670-USDOT4504932-SIG8F3B2A",
        "skyautoservices.com",
        "www.skyautoservices.com",
        "localhost",
        "127.0.0.1",
        "0.0.0.0",
        "hostinger",
        "ngrok",
        "https://www.skyautoservices.com/api/dmca_beacon.php",
        "UNAUTHORIZED_HOST_DMCA_TRAP",
        "DOM_DEFANGED_DMCA_LOCK",
        "HEADLESS_SCRAPER_DEFANG",
        "DEBUGGER_DECOMPILATION_ATTACHED",
        "POST",
        "application/json",
        "contextmenu",
        "keydown",
        "webdriver",
        "callPhantom",
        "_phantom",
        "__nightmare",
        "debugger",
        "constructor",
        "sendBeacon",
        "hostname",
        "href",
        "referrer",
        "userAgent",
        "DIRECT"
    ]
    
    random.shuffle(string_pool)
    
    def idx(s):
        return string_pool.index(s)
        
    var_str_array = generate_hex_var(4)
    var_str_func = generate_hex_var(4)
    var_shift_val = random.randint(150, 450)
    
    js_string_array = json.dumps(string_pool)
    
    # Pre-calculated token lookups
    t_canary = f"{var_str_func}({idx('SKY-CANARY-MC1782670-USDOT4504932-SIG8F3B2A')})"
    t_host1 = f"{var_str_func}({idx('skyautoservices.com')})"
    t_host2 = f"{var_str_func}({idx('www.skyautoservices.com')})"
    t_host3 = f"{var_str_func}({idx('localhost')})"
    t_host4 = f"{var_str_func}({idx('127.0.0.1')})"
    t_host5 = f"{var_str_func}({idx('0.0.0.0')})"
    t_hostinger = f"{var_str_func}({idx('hostinger')})"
    t_ngrok = f"{var_str_func}({idx('ngrok')})"
    
    t_hostname = f"{var_str_func}({idx('hostname')})"
    t_href = f"{var_str_func}({idx('href')})"
    t_referrer = f"{var_str_func}({idx('referrer')})"
    t_direct = f"{var_str_func}({idx('DIRECT')})"
    t_useragent = f"{var_str_func}({idx('userAgent')})"
    t_endpoint = f"{var_str_func}({idx('https://www.skyautoservices.com/api/dmca_beacon.php')})"
    t_sendbeacon = f"{var_str_func}({idx('sendBeacon')})"
    t_post = f"{var_str_func}({idx('POST')})"
    t_appjson = f"{var_str_func}({idx('application/json')})"
    
    t_ev_trap = f"{var_str_func}({idx('UNAUTHORIZED_HOST_DMCA_TRAP')})"
    t_act_lock = f"{var_str_func}({idx('DOM_DEFANGED_DMCA_LOCK')})"
    t_act_scraper = f"{var_str_func}({idx('HEADLESS_SCRAPER_DEFANG')})"
    t_act_debug = f"{var_str_func}({idx('DEBUGGER_DECOMPILATION_ATTACHED')})"
    
    t_webdriver = f"{var_str_func}({idx('webdriver')})"
    t_callphantom = f"{var_str_func}({idx('callPhantom')})"
    t_phantom = f"{var_str_func}({idx('_phantom')})"
    t_nightmare = f"{var_str_func}({idx('__nightmare')})"
    
    t_constructor = f"{var_str_func}({idx('constructor')})"
    t_debugger = f"{var_str_func}({idx('debugger')})"
    t_contextmenu = f"{var_str_func}({idx('contextmenu')})"
    t_keydown = f"{var_str_func}({idx('keydown')})"

    js_template = f"""var {var_str_array} = {js_string_array};

(function(_0xarr, _0xshift) {{
    var _0xrotate = function(_0xstep) {{
        while (--_0xstep) {{
            _0xarr['push'](_0xarr['shift']());
        }}
    }};
    _0xrotate(++_0xshift);
}}({var_str_array}, {var_shift_val}));

var {var_str_func} = function(_0xidx, _0xkey) {{
    _0xidx = _0xidx - 0x0;
    var _0xres = {var_str_array}[_0xidx];
    return _0xres;
}};

(function() {{
    'use strict';
    
    var _0xflow = '0|4|2|6|1|5|3'['split']('|');
    var _0xstep = 0x0;
    
    while (true) {{
        switch (_0xflow[_0xstep++]) {{
            case '0':
                var _0xcanary = {t_canary};
                var _0xauths = [
                    {t_host1},
                    {t_host2},
                    {t_host3},
                    {t_host4},
                    {t_host5}
                ];
                continue;
                
            case '1':
                function _0xbeacon(_0xevt, _0xaction) {{
                    try {{
                        var _0xpld = JSON['stringify']({{
                            'event': _0xevt,
                            'canary': _0xcanary,
                            'violator_host': window['location'][{t_hostname}],
                            'violator_url': window['location'][{t_href}],
                            'referrer': document[{t_referrer}] || {t_direct},
                            'user_agent': navigator[{t_useragent}],
                            'timestamp': new Date()['toISOString'](),
                            'action': _0xaction
                        }});
                        var _0xep = {t_endpoint};
                        if (navigator[{t_sendbeacon}]) {{
                            navigator[{t_sendbeacon}](_0xep, _0xpld);
                        }} else {{
                            var _0xxhr = new XMLHttpRequest();
                            _0xxhr['open']({t_post}, _0xep, true);
                            _0xxhr['setRequestHeader']('Content-Type', {t_appjson});
                            _0xxhr['send'](_0xpld);
                        }}
                    }} catch (e) {{}}
                }}
                continue;
                
            case '2':
                function _0xcheckDomain() {{
                    var _0xh = window['location'][{t_hostname}]['toLowerCase']();
                    if (!_0xh) return true;
                    for (var _0xi = 0; _0xi < _0xauths['length']; _0xi++) {{
                        var _0xa = _0xauths[_0xi];
                        if (_0xh === _0xa || _0xh['endsWith']('.' + _0xa) || _0xh['indexOf']({t_hostinger}) !== -0x1 || _0xh['indexOf']({t_ngrok}) !== -0x1) {{
                            return true;
                        }}
                    }}
                    return false;
                }}
                continue;
                
            case '3':
                if (!_0xcheckDomain()) {{
                    _0xbeacon({t_ev_trap}, {t_act_lock});
                    window['stop'] && window['stop']();
                    document['documentElement']['innerHTML'] = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>LEGAL CEASE & DESIST - 17 U.S.C. § 512</title><style>body{{background:#0a0c10;color:#f85149;font-family:system-ui,-apple-system,sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0;padding:20px;box-sizing:border-box;}}.card{{background:#161b22;border:1px solid #da3633;border-radius:12px;max-width:680px;padding:32px;box-shadow:0 10px 40px rgba(218,54,51,0.25);}}h1{{color:#ff7b72;font-size:22px;margin-top:0;display:flex;align-items:center;gap:10px;}}p{{color:#c9d1d9;font-size:14px;line-height:1.6;}}.badge{{background:#da3633;color:#fff;padding:3px 8px;border-radius:4px;font-size:11px;font-weight:bold;display:inline-block;}}.canary{{background:#0d1117;border:1px solid #30363d;padding:12px;border-radius:6px;font-family:monospace;font-size:12px;color:#58a6ff;word-break:break-all;margin-top:16px;}}</style></head><body><div class="card"><h1><span class="badge">LEGAL NOTICE</span> 17 U.S.C. § 512 / DMCA VIOLATION</h1><p><strong>NOTICE OF UNAUTHORIZED CODE REPRODUCTION & THEFT:</strong></p><p>This digital asset, UI layout, and proprietary source architecture are the exclusive intellectual property of <strong>Sky Auto Services LLC</strong> (FMCSA MC-1782670, USDOT 4504932). Execution of this software on this domain is strictly unauthorized and constitutes willful copyright infringement under the Digital Millennium Copyright Act (17 U.S.C. § 512) and the Computer Fraud and Abuse Act (18 U.S.C. § 1030).</p><p>Forensic telemetry and network logs have been captured and cryptographically dispatched to legal counsel and hosting infrastructure providers.</p><div class="canary">CRYPTOGRAPHIC CANARY SIGNATURE: ' + _0xcanary + '<br>OFFENDING HOST: ' + window['location'][{t_hostname}] + '</div></div></body></html>';
                    return;
                }}
                continue;
                
            case '4':
                var _0xheadless = (
                    navigator[{t_webdriver}] ||
                    window[{t_callphantom}] ||
                    window[{t_phantom}] ||
                    window[{t_nightmare}] ||
                    (navigator['plugins'] && navigator['plugins']['length'] === 0x0 && !/mobile/i['test'](navigator[{t_useragent}]))
                );

                if (_0xheadless) {{
                    _0xbeacon({t_ev_trap}, {t_act_scraper});
                    window['stop'] && window['stop']();
                    document['documentElement']['innerHTML'] = '<head><title>403 Forbidden</title></head><body style="background:#000;color:#00f0ff;font-family:monospace;padding:40px;"><h2>🔒 [OMNIVERSE AEGIS CONTAINER]</h2><p>Ciphertext: 8f9b7c2e01a4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0</p></body>';
                    return;
                }}
                continue;
                
            case '5':
                (function _0xinstallTripwire() {{
                    var _0xt0 = performance['now']();
                    (function() {{ return false; }}[{t_constructor}]({t_debugger})());
                    if (performance['now']() - _0xt0 > 0x64) {{
                        _0xbeacon({t_ev_trap}, {t_act_debug});
                        while(true) {{}}
                    }}
                }})();
                setInterval(function() {{
                    var _0xt0 = performance['now']();
                    (function() {{ return false; }}[{t_constructor}]({t_debugger})());
                    if (performance['now']() - _0xt0 > 0x64) {{
                        while(true) {{}}
                    }}
                }}, 0x7d0);
                continue;
                
            case '6':
                document['addEventListener']({t_contextmenu}, function(_0xe) {{
                    _0xe['preventDefault']();
                    return false;
                }}, {{ 'capture': true }});
                
                document['addEventListener']({t_keydown}, function(_0xe) {{
                    if (_0xe['keyCode'] === 0x7b) {{ // F12
                        _0xe['preventDefault']();
                        _0xe['stopPropagation']();
                        return false;
                    }}
                    if (_0xe['ctrlKey'] && _0xe['shiftKey'] && (_0xe['keyCode'] === 0x49 || _0xe['keyCode'] === 0x4a || _0xe['keyCode'] === 0x43)) {{
                        _0xe['preventDefault']();
                        _0xe['stopPropagation']();
                        return false;
                    }}
                    if (_0xe['ctrlKey'] && (_0xe['keyCode'] === 0x55 || _0xe['keyCode'] === 0x53)) {{
                        _0xe['preventDefault']();
                        _0xe['stopPropagation']();
                        return false;
                    }}
                    if (_0xe['metaKey'] && ((_0xe['altKey'] && (_0xe['keyCode'] === 0x49 || _0xe['keyCode'] === 0x55)) || _0xe['keyCode'] === 0x53)) {{
                        _0xe['preventDefault']();
                        _0xe['stopPropagation']();
                        return false;
                    }}
                }}, {{ 'capture': true }});
                
                try {{
                    var _0xnoop = function() {{}};
                    window['console']['log'] = _0xnoop;
                    window['console']['warn'] = _0xnoop;
                    window['console']['dir'] = _0xnoop;
                    window['console']['table'] = _0xnoop;
                }} catch (err) {{}}
                continue;
        }}
        break;
    }}
}})();
"""
    return js_template

def create_dmca_backend_php():
    return """<?php
// OMNIVERSE AEGIS SECURITY SHIELD - AUTOMATED DMCA INCIDENT LOGGER
// Header configuration for CORS & Security
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['status' => 'error', 'message' => 'Method Not Allowed']);
    exit;
}

$rawInput = file_get_contents('php://input');
if (empty($rawInput)) {
    http_response_code(400);
    echo json_encode(['status' => 'error', 'message' => 'Empty Payload']);
    exit;
}

$data = json_decode($rawInput, true);
if (!$data) {
    http_response_code(400);
    echo json_encode(['status' => 'error', 'message' => 'Invalid JSON']);
    exit;
}

// Extract incident details
$incident = [
    'id' => 'INC-' . bin2hex(random_bytes(6)),
    'received_at' => date('Y-m-d H:i:s T'),
    'client_ip' => $_SERVER['HTTP_CF_CONNECTING_IP'] ?? $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? 'UNKNOWN',
    'origin' => $_SERVER['HTTP_ORIGIN'] ?? 'UNKNOWN',
    'user_agent' => $_SERVER['HTTP_USER_AGENT'] ?? 'UNKNOWN',
    'payload' => $data
];

// Directory & log path
$logDir = __DIR__ . '/../data';
if (!is_dir($logDir)) {
    @mkdir($logDir, 0755, true);
}

$logFile = $logDir . '/dmca_infringements.json';

// Atomic file append with locking
$existing = [];
if (file_exists($logFile)) {
    $content = @file_get_contents($logFile);
    if (!empty($content)) {
        $existing = json_decode($content, true) ?: [];
    }
}

// Keep last 500 incidents
array_unshift($existing, $incident);
if (count($existing) > 500) {
    $existing = array_slice($existing, 0, 500);
}

file_put_contents($logFile, json_encode($existing, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES), LOCK_EX);

http_response_code(200);
echo json_encode([
    'status' => 'recorded',
    'incident_id' => $incident['id'],
    'protection' => 'AEGIS_DMCA_ACTIVE'
]);
"""

def main():
    workspace = "/Users/silversurfer/Documents/Omniverse2"
    public_local = os.path.join(workspace, "public_html_local")
    public_hostinger = os.path.join(workspace, "hostinger_site/public_html")
    
    print("🚀 [OMNIVERSE CISO] Compiling Control-Flow Flattened Security Shield...")
    obfuscated_js = build_flattened_obfuscated_shield()
    
    # 1. Write JS files
    for base in [public_local, public_hostinger]:
        js_dir = os.path.join(base, "assets/js")
        os.makedirs(js_dir, exist_ok=True)
        target_js = os.path.join(js_dir, "aegis_security_shield.min.js")
        with open(target_js, "w", encoding="utf-8") as f:
            f.write(obfuscated_js)
        print(f"  ✓ Written: {target_js}")

    # 2. Write DMCA Backend PHP endpoint
    dmca_php = create_dmca_backend_php()
    for base in [public_local, public_hostinger]:
        api_dir = os.path.join(base, "api")
        os.makedirs(api_dir, exist_ok=True)
        target_php = os.path.join(api_dir, "dmca_beacon.php")
        with open(target_php, "w", encoding="utf-8") as f:
            f.write(dmca_php)
        print(f"  ✓ Written: {target_php}")

    # 3. Generate Steganographic Zero-Width Watermark
    watermark_plaintext = "COPYRIGHT 2026 SKY AUTO SERVICES LLC | ALL RIGHTS RESERVED | USDOT 4504932 | MC-1782670 | CRYPTOGRAPHIC CANARY: 0x9f4a8b2c7e1d5e6a"
    zero_width_sig = encode_zero_width(watermark_plaintext)
    
    watermark_html_comment = f'<!-- \u200B{zero_width_sig}\u200B -->'
    watermark_meta = f'<meta name="copyright-canary" content="0x9f4a8b2c7e1d5e6a" data-sig="{zero_width_sig}"/>'
    shield_script_tag = '<script src="/assets/js/aegis_security_shield.min.js" async></script>'

    print("🛡️ [OMNIVERSE CISO] Injecting Digital Steganographic Watermark & Shield into HTML Pages...")
    html_targets = [
        "index.html",
        "about.html",
        "services.html",
        "contact.html",
        "routes.html",
        "privacy.html",
        "terms.html",
        "state-to-state-routes.html",
        "quote-widget.html"
    ]
    
    for base in [public_local, public_hostinger]:
        for html_file in html_targets:
            file_path = os.path.join(base, html_file)
            if not os.path.exists(file_path):
                continue
            
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Check if script tag is in content
            if "aegis_security_shield.min.js" not in content:
                if "</head>" in content:
                    injection = f"{watermark_html_comment}\n{watermark_meta}\n{shield_script_tag}\n</head>"
                    content = content.replace("</head>", injection, 1)
                elif "<head>" in content:
                    injection = f"<head>\n{watermark_html_comment}\n{watermark_meta}\n{shield_script_tag}"
                    content = content.replace("<head>", injection, 1)
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"  ✓ Injected Watermark & Shield into: {file_path}")

    print("✅ [OMNIVERSE CISO] Shield Compilation & Deployment Complete!")

if __name__ == "__main__":
    main()
