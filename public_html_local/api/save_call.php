<?php
/**
 * save_call.php — Sky Auto Services Phone Call Intake & Telemetry Logger
 * Omniverse Group | Marcus Vance Jr. (Backend Quote Logger) & Dr. Alexander Vance
 */
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Accept');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

$raw_input = file_get_contents('php://input');
$body = json_decode($raw_input, true);

if (!$body) {
    $body = $_POST;
}

$call_id = 'CALL-' . strtoupper(substr(md5(uniqid(rand(), true)), 0, 8));
$timestamp = date('Y-m-d H:i:s');

$session_id = $body['session_id'] ?? ('SESS-' . substr(md5(uniqid()), 0, 6));
$page = $body['page'] ?? ($_SERVER['HTTP_REFERER'] ?? '/');
$phone = $body['phone'] ?? '+12244490397';
$button_type = $body['button_type'] ?? 'direct_phone_click';
$is_test = !empty($body['is_test']);

$call_record = [
    'id' => $call_id,
    'session_id' => $session_id,
    'timestamp' => $timestamp,
    'page' => $page,
    'phone' => $phone,
    'button_type' => $button_type,
    'user_agent' => $_SERVER['HTTP_USER_AGENT'] ?? '',
    'ip' => $_SERVER['REMOTE_ADDR'] ?? '',
    'is_test' => $is_test
];

// Append to call_requests.json
$json_file = __DIR__ . '/../../call_requests.json';
if (!file_exists($json_file)) {
    $json_file = __DIR__ . '/../call_requests.json';
}
if (!file_exists($json_file)) {
    $json_file = dirname(__DIR__, 2) . '/call_requests.json';
}

$calls = [];
if (file_exists($json_file)) {
    $existing = file_get_contents($json_file);
    $calls = json_decode($existing, true) ?: [];
}
array_unshift($calls, $call_record);
@file_put_contents($json_file, json_encode(array_slice($calls, 0, 500), JSON_PRETTY_PRINT), LOCK_EX);

echo json_encode([
    'success' => true,
    'call_id' => $call_id,
    'timestamp' => $timestamp,
    'data' => $call_record
]);
exit;
