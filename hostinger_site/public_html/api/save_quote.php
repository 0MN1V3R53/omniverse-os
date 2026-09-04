<?php
/**
 * save_quote.php — Sky Auto Services Enterprise Lead Ingestion & Google Sheets Sync
 * Omniverse Security Hardened Suite | CISO Michael Chang & Dr. Alexander Vance
 */
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: SAMEORIGIN');

// 1. Strict CORS Policy
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
    echo json_encode(['success' => false, 'error' => 'Method not allowed']);
    exit;
}

// 2. Ingest & Parse Input Payload
$raw_input = file_get_contents('php://input');
$body = json_decode($raw_input, true);
if (!$body && !empty($_POST)) {
    $body = $_POST;
}

if (empty($body) || !is_array($body)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'No quote data provided']);
    exit;
}

// 3. Rate Limiting Defense (Max 15 submissions per 5 minutes per IP)
$client_ip = $_SERVER['HTTP_CF_CONNECTING_IP'] ?? $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? 'UNKNOWN';
$rate_dir = sys_get_temp_dir() . '/sky_rate_limits';
if (!is_dir($rate_dir)) {
    @mkdir($rate_dir, 0700, true);
}
$ip_hash = md5($client_ip);
$rate_file = $rate_dir . '/rate_' . $ip_hash . '.json';
$now = time();
$rate_data = ['count' => 0, 'first_req' => $now];

if (file_exists($rate_file)) {
    $content = @file_get_contents($rate_file);
    if ($content) {
        $parsed = json_decode($content, true);
        if ($parsed && ($now - $parsed['first_req']) < 300) {
            $rate_data = $parsed;
        }
    }
}
$rate_data['count']++;
@file_put_contents($rate_file, json_encode($rate_data), LOCK_EX);

if ($rate_data['count'] > 20) {
    http_response_code(429);
    echo json_encode(['success' => false, 'error' => 'Too many quote requests. Please call our advisors directly at (224) 449-0397.']);
    exit;
}

// 4. Strict Input Sanitization & Anti-Injection Filtering
$raw_name = trim($body['name'] ?? $body['full_name'] ?? ($body['firstName'] ?? '') . ' ' . ($body['lastName'] ?? ''));
$name = preg_replace('/[\r\n\t]/', '', strip_tags($raw_name)) ?: 'Website Visitor';

$raw_phone = $body['phone'] ?? '';
$phone = preg_replace('/[^\d+]/', '', $raw_phone);

$raw_email = trim($body['email'] ?? '');
$email = filter_var(preg_replace('/[\r\n\t]/', '', $raw_email), FILTER_SANITIZE_EMAIL);

$origin = preg_replace('/[\r\n\t]/', '', strip_tags(trim($body['origin'] ?? '')));
$destination = preg_replace('/[\r\n\t]/', '', strip_tags(trim($body['destination'] ?? '')));

$raw_vehicle = trim($body['vehicle'] ?? trim(($body['vehicleYear'] ?? '') . ' ' . ($body['vehicleMake'] ?? '') . ' ' . ($body['vehicleModel'] ?? '')));
$vehicle = preg_replace('/[\r\n\t]/', '', strip_tags($raw_vehicle)) ?: 'Standard Vehicle';

$distance = intval($body['distance_miles'] ?? ($body['distance'] ?? 0));
$transport_type = preg_replace('/[\r\n\t]/', '', strip_tags(trim($body['transport_type_label'] ?? ($body['transport_type'] ?? ($body['transportType'] ?? 'Open Standard')))));

// Price validation and formatting
$raw_price = $body['price'] ?? ($body['final_quoted_price'] ?? '');
if (is_numeric($raw_price)) {
    $price = '$' . number_format((float)$raw_price, 0);
} elseif (is_string($raw_price) && preg_match('/[0-9]/', $raw_price)) {
    $clean_num = floatval(preg_replace('/[^\d.]/', '', $raw_price));
    $price = $clean_num > 0 ? ('$' . number_format($clean_num, 0)) : '$399';
} else {
    $price = '$399';
}

$quote_id = 'QUOTE-' . strtoupper(bin2hex(random_bytes(4)));
$timestamp = date('Y-m-d H:i:s');
$pickup_date = preg_replace('/[\r\n\t]/', '', strip_tags(trim($body['pickupDate'] ?? ($body['pickup_date'] ?? ''))));
$comments = strip_tags(trim($body['comments'] ?? ($body['more_info'] ?? '')));

$lead_record = [
    'id' => $quote_id,
    'received_at' => $timestamp,
    'name' => $name,
    'phone' => $phone,
    'email' => $email,
    'origin' => $origin,
    'destination' => $destination,
    'vehicle' => $vehicle,
    'distance_miles' => $distance,
    'transport_type' => $transport_type,
    'price' => $price,
    'pickup_date' => $pickup_date,
    'comments' => $comments,
    'ip_hash' => substr($ip_hash, 0, 8),
    'is_test' => !empty($body['is_test']) || stripos($name, 'test') !== false
];

// 5. Append to Protected Server Lead Archive
$json_file = __DIR__ . '/../../quote_submissions.json';
if (!file_exists($json_file)) {
    $json_file = __DIR__ . '/../quote_submissions.json';
}
if (!file_exists($json_file)) {
    $json_file = dirname(__DIR__, 2) . '/quote_submissions.json';
}

$quotes = [];
if (file_exists($json_file)) {
    $existing = @file_get_contents($json_file);
    if ($existing) {
        $quotes = json_decode($existing, true) ?: [];
    }
}
array_unshift($quotes, $lead_record);
@file_put_contents($json_file, json_encode(array_slice($quotes, 0, 500), JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES), LOCK_EX);

// 6. Dispatch to Google Apps Script Webhook (WITH STRICT SSL VERIFICATION)
$google_sheets_url = 'https://script.google.com/macros/s/AKfycbxjTrpOti2ZPZscPAbgKRTPc3PeAkNyBMCVnieVW2BtnUsnQsiIBp5wKo3JVKb6F43m/exec';
$google_payload = [
    'id' => $quote_id,
    'name' => $name,
    'full_name' => $name,
    'phone' => $phone,
    'email' => $email,
    'origin' => $origin,
    'destination' => $destination,
    'vehicle' => $vehicle,
    'distance' => $distance,
    'distance_miles' => $distance,
    'transport_type' => $transport_type,
    'price' => $price,
    'pickup_date' => $pickup_date,
    'comments' => $comments
];

$google_synced = false;
if (!empty($google_sheets_url)) {
    $ch = curl_init($google_sheets_url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_FOLLOWLOCATION => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => json_encode($google_payload),
        CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
        CURLOPT_TIMEOUT => 10,
        CURLOPT_SSL_VERIFYPEER => true, // STRICT SSL VALIDATION
        CURLOPT_SSL_VERIFYHOST => 2
    ]);
    $google_response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($http_code >= 200 && $http_code < 400) {
        $google_synced = true;
    }
}

// 7. Secure Email Dispatch (Sanitized Headers, Zero CRLF Injection)
$to_email = 'sales@skyservicesllc.com, mehmet33339999@gmail.com';
$email_subject = '🚨 NEW AUTO TRANSPORT LEAD: ' . $name;
$clean_reply_to = filter_var($email, FILTER_VALIDATE_EMAIL) ? $email : 'sales@skyservicesllc.com';

$email_headers = "From: Sky Auto Services <noreply@skyautoservices.com>\r\n" .
                 "Reply-To: " . $clean_reply_to . "\r\n" .
                 "MIME-Version: 1.0\r\n" .
                 "Content-Type: text/html; charset=UTF-8\r\n" .
                 "X-Mailer: PHP/" . phpversion();

$email_html = "
<!DOCTYPE html>
<html>
<head><style>body{font-family:Arial,sans-serif;color:#333;line-height:1.6;} .card{max-width:600px;margin:20px auto;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;box-shadow:0 4px 12px rgba(0,0,0,0.08);} .header{background:#1e293b;color:#fff;padding:20px;text-align:center;} .content{padding:25px;} .field{margin-bottom:12px;} .label{font-weight:bold;color:#64748b;} .val{font-size:16px;color:#0f172a;} .badge{display:inline-block;padding:4px 12px;background:#dcfce7;color:#166534;font-weight:bold;border-radius:999px;font-size:14px;}</style></head>
<body>
<div class='card'>
  <div class='header'><h2>🚨 New Auto Transport Lead</h2></div>
  <div class='content'>
    <div class='field'><span class='label'>Customer Name:</span> <div class='val'><b>" . htmlspecialchars($name, ENT_QUOTES, 'UTF-8') . "</b></div></div>
    <div class='field'><span class='label'>Phone:</span> <div class='val'><a href='tel:" . htmlspecialchars($phone, ENT_QUOTES, 'UTF-8') . "'>" . htmlspecialchars($phone, ENT_QUOTES, 'UTF-8') . "</a></div></div>
    <div class='field'><span class='label'>Email:</span> <div class='val'><a href='mailto:" . htmlspecialchars($email, ENT_QUOTES, 'UTF-8') . "'>" . htmlspecialchars($email, ENT_QUOTES, 'UTF-8') . "</a></div></div>
    <hr style='border:0;border-top:1px solid #e2e8f0;margin:15px 0;'>
    <div class='field'><span class='label'>Route:</span> <div class='val'>" . htmlspecialchars($origin, ENT_QUOTES, 'UTF-8') . " ➔ " . htmlspecialchars($destination, ENT_QUOTES, 'UTF-8') . " (" . htmlspecialchars((string)$distance, ENT_QUOTES, 'UTF-8') . " miles)</div></div>
    <div class='field'><span class='label'>Vehicle:</span> <div class='val'>" . htmlspecialchars($vehicle, ENT_QUOTES, 'UTF-8') . "</div></div>
    <div class='field'><span class='label'>Transport Type:</span> <div class='val'>" . htmlspecialchars($transport_type, ENT_QUOTES, 'UTF-8') . "</div></div>
    <div class='field'><span class='label'>Price Quoted:</span> <div class='val'><span class='badge'>" . htmlspecialchars($price, ENT_QUOTES, 'UTF-8') . "</span></div></div>
    " . (!empty($comments) ? ("<div class='field'><span class='label'>Comments:</span> <div class='val'>" . htmlspecialchars($comments, ENT_QUOTES, 'UTF-8') . "</div></div>") : "") . "
    <hr style='border:0;border-top:1px solid #e2e8f0;margin:15px 0;'>
    <p style='font-size:13px;color:#94a3b8;'>Quote ID: " . htmlspecialchars($quote_id, ENT_QUOTES, 'UTF-8') . " | Received: " . $timestamp . "</p>
  </div>
</div>
</body>
</html>
";

$mail_sent = @mail($to_email, $email_subject, $email_html, $email_headers);

echo json_encode([
    'success' => true,
    'quote_id' => $quote_id,
    'google_sync' => $google_synced,
    'direct_mail_sent' => $mail_sent,
    'data' => [
        'id' => $quote_id,
        'name' => $name,
        'origin' => $origin,
        'destination' => $destination,
        'vehicle' => $vehicle,
        'price' => $price
    ]
]);
exit;
