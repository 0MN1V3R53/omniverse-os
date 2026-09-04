<?php
/**
 * dmca_beacon.php — Sky Auto Services Incident & Threat Forensics Logger (Security Hardened)
 * Omniverse Security Hardened Suite | CISO Michael Chang & Dr. Alexander Vance
 */
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: SAMEORIGIN');

$allowed_origins = [
    'https://www.skyautoservices.com',
    'https://skyautoservices.com',
    'http://localhost:3000',
    'http://localhost:8000'
];
$http_origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if (in_array($http_origin, $allowed_origins, true)) {
    header("Access-Control-Allow-Origin: {$http_origin}");
} else {
    header("Access-Control-Allow-Origin: https://www.skyautoservices.com");
}
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['status' => 'error', 'message' => 'Method Not Allowed']);
    exit;
}

$rawInput = file_get_contents('php://input');
if (empty($rawInput) || strlen($rawInput) > 65536) {
    http_response_code(400);
    echo json_encode(['status' => 'error', 'message' => 'Invalid or oversized payload']);
    exit;
}

$data = json_decode($rawInput, true);
if (!$data || !is_array($data)) {
    http_response_code(400);
    echo json_encode(['status' => 'error', 'message' => 'Invalid JSON']);
    exit;
}

// Extract and sanitize incident details
$incident = [
    'id' => 'INC-' . bin2hex(random_bytes(6)),
    'received_at' => date('Y-m-d H:i:s T'),
    'client_ip' => substr($_SERVER['HTTP_CF_CONNECTING_IP'] ?? $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? 'UNKNOWN', 0, 45),
    'origin' => substr($_SERVER['HTTP_ORIGIN'] ?? 'UNKNOWN', 0, 255),
    'user_agent' => substr($_SERVER['HTTP_USER_AGENT'] ?? 'UNKNOWN', 0, 255),
    'event' => substr(strval($data['event'] ?? 'UNKNOWN'), 0, 64),
    'action' => substr(strval($data['action'] ?? 'UNKNOWN'), 0, 64)
];

$logDir = __DIR__ . '/../data';
if (!is_dir($logDir)) {
    @mkdir($logDir, 0700, true);
}

$logFile = $logDir . '/dmca_infringements.json';

$existing = [];
if (file_exists($logFile)) {
    $content = @file_get_contents($logFile);
    if (!empty($content)) {
        $existing = json_decode($content, true) ?: [];
    }
}

array_unshift($existing, $incident);
if (count($existing) > 500) {
    $existing = array_slice($existing, 0, 500);
}

@file_put_contents($logFile, json_encode($existing, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES), LOCK_EX);

http_response_code(200);
echo json_encode([
    'status' => 'recorded',
    'incident_id' => $incident['id'],
    'protection' => 'AEGIS_DMCA_ACTIVE'
]);
exit;
