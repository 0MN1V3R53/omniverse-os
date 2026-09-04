<?php
/**
 * save_call.php — Sky Auto Services Phone Call Intake & Telemetry Logger (Security Hardened)
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
header('Access-Control-Allow-Headers: Content-Type, Accept');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'Method not allowed. POST required.']);
    exit;
}

$raw_input = file_get_contents('php://input');
$body = json_decode($raw_input, true);
if (!$body && !empty($_POST)) {
    $body = $_POST;
}

$call_id = 'CALL-' . strtoupper(bin2hex(random_bytes(4)));
$timestamp = date('Y-m-d H:i:s');

$session_id = preg_replace('/[^A-Za-z0-9_-]/', '', substr($body['session_id'] ?? ('SESS-' . bin2hex(random_bytes(3))), 0, 64));
$page = preg_replace('/[\r\n\t]/', '', strip_tags(substr($body['page'] ?? ($_SERVER['HTTP_REFERER'] ?? '/'), 0, 255)));
$phone = preg_replace('/[^\d+]/', '', $body['phone'] ?? '+12244490397');
$button_type = preg_replace('/[^a-zA-Z0-9_ -]/', '', strip_tags(substr($body['button_type'] ?? 'direct_phone_click', 0, 64)));
$is_test = !empty($body['is_test']);

$call_record = [
    'id' => $call_id,
    'session_id' => $session_id,
    'timestamp' => $timestamp,
    'page' => $page,
    'phone' => $phone,
    'button_type' => $button_type,
    'user_agent' => substr($_SERVER['HTTP_USER_AGENT'] ?? '', 0, 255),
    'is_test' => $is_test
];

// Append to call_requests.json safely
$json_file = __DIR__ . '/../../call_requests.json';
if (!file_exists($json_file)) {
    $json_file = __DIR__ . '/../call_requests.json';
}
if (!file_exists($json_file)) {
    $json_file = dirname(__DIR__, 2) . '/call_requests.json';
}

$calls = [];
if (file_exists($json_file)) {
    $existing = @file_get_contents($json_file);
    if ($existing) {
        $calls = json_decode($existing, true) ?: [];
    }
}
array_unshift($calls, $call_record);
@file_put_contents($json_file, json_encode(array_slice($calls, 0, 500), JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES), LOCK_EX);

echo json_encode([
    'success' => true,
    'call_id' => $call_id,
    'timestamp' => $timestamp
]);
exit;
