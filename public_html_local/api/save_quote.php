<?php
/**
 * save_quote.php — Sky Auto Services Live Quote Ingestion & Google Sheets Sync
 * Omniverse Group | Marcus Vance Jr. (Backend Quote Logger) & Dr. Alexander Vance
 */
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
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

$raw_input = file_get_contents('php://input');
$body = json_decode($raw_input, true);

if (!$body) {
    // Fallback to $_POST if sent as form-encoded
    $body = $_POST;
}

if (empty($body)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'No quote data provided']);
    exit;
}

// 1. Generate Quote ID & Format Payload
$quote_id = !empty($body['id']) ? $body['id'] : ('QUOTE-' . strtoupper(substr(md5(uniqid(rand(), true)), 0, 8)));
$timestamp = date('Y-m-d H:i:s');

$name = !empty($body['name']) ? $body['name'] : (!empty($body['full_name']) ? $body['full_name'] : trim(($body['firstName'] ?? '') . ' ' . ($body['lastName'] ?? '')));
$phone = preg_replace('/[^\d+]/', '', $body['phone'] ?? '');
$email = trim($body['email'] ?? '');
$origin = trim($body['origin'] ?? '');
$destination = trim($body['destination'] ?? '');
$vehicle = trim($body['vehicle'] ?? trim(($body['vehicleYear'] ?? '') . ' ' . ($body['vehicleMake'] ?? '') . ' ' . ($body['vehicleModel'] ?? '')));
$distance = $body['distance_miles'] ?? ($body['distance'] ?? '');
$transport_type = $body['transport_type_label'] ?? ($body['transport_type'] ?? ($body['transportType'] ?? 'Open Standard'));
$raw_price = $body['price'] ?? ($body['final_quoted_price'] ?? '');
if (is_numeric($raw_price)) {
    $price = '$' . number_format((float)$raw_price, 0);
} elseif (is_string($raw_price) && preg_match('/[0-9]/', $raw_price)) {
    $clean_num = floatval(preg_replace('/[^\d.]/', '', $raw_price));
    $price = $clean_num > 0 ? ('$' . number_format($clean_num, 0)) : trim($raw_price);
} else {
    $price = trim((string)$raw_price);
}

$lead_record = [
    'id' => $quote_id,
    'received_at' => $timestamp,
    'name' => $name ?: 'Website Visitor',
    'full_name' => $name ?: 'Website Visitor',
    'phone' => $phone,
    'email' => $email,
    'origin' => $origin,
    'destination' => $destination,
    'vehicle' => $vehicle ?: 'Standard Vehicle',
    'distance' => $distance,
    'distance_miles' => $distance,
    'transport_type' => $transport_type,
    'price' => $price,
    'price_estimate_low' => $body['price_estimate_low'] ?? '',
    'price_estimate_high' => $body['price_estimate_high'] ?? '',
    'eta' => $body['eta'] ?? '',
    'pickup_date' => $body['pickupDate'] ?? ($body['pickup_date'] ?? ''),
    'comments' => $body['comments'] ?? ($body['more_info'] ?? ''),
    'is_test' => !empty($body['is_test']) || stripos($name, 'test') !== false
];

// 2. Append to local quote_submissions.json on Hostinger server
$json_file = __DIR__ . '/../../quote_submissions.json';
if (!file_exists($json_file)) {
    $json_file = __DIR__ . '/../quote_submissions.json';
}
if (!file_exists($json_file)) {
    $json_file = dirname(__DIR__, 2) . '/quote_submissions.json';
}

$quotes = [];
if (file_exists($json_file)) {
    $existing = file_get_contents($json_file);
    $quotes = json_decode($existing, true) ?: [];
}
array_unshift($quotes, $lead_record);
@file_put_contents($json_file, json_encode(array_slice($quotes, 0, 500), JSON_PRETTY_PRINT), LOCK_EX);

// 3. Dispatch to Google Apps Script Webhook (Live Leads Sheet & Email Alert)
$google_sheets_url = 'https://script.google.com/macros/s/AKfycbxjTrpOti2ZPZscPAbgKRTPc3PeAkNyBMCVnieVW2BtnUsnQsiIBp5wKo3JVKb6F43m/exec';
$google_payload = [
    'id' => $quote_id,
    'name' => $lead_record['name'],
    'full_name' => $lead_record['name'],
    'phone' => $lead_record['phone'],
    'email' => $lead_record['email'],
    'origin' => $lead_record['origin'],
    'destination' => $lead_record['destination'],
    'vehicle' => $lead_record['vehicle'],
    'distance' => $lead_record['distance'],
    'distance_miles' => $lead_record['distance_miles'],
    'transport_type' => $lead_record['transport_type'],
    'price' => $lead_record['price'],
    'price_estimate_low' => $lead_record['price_estimate_low'],
    'price_estimate_high' => $lead_record['price_estimate_high'],
    'eta' => $lead_record['eta'],
    'pickup_date' => $lead_record['pickup_date'],
    'comments' => $lead_record['comments']
];

$google_synced = false;
$google_res_text = '';

if (!empty($google_sheets_url)) {
    $ch = curl_init($google_sheets_url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($google_payload));
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    curl_setopt($ch, CURLOPT_TIMEOUT, 15);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    $google_response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($http_code >= 200 && $http_code < 400) {
        $google_synced = true;
        $google_res_text = $google_response;
    }
}

// 4. Direct Server-Side Email Dispatch to sales@skyservicesllc.com & mehmet33339999@gmail.com (Dual-Redundancy)
$to_email = 'sales@skyservicesllc.com, mehmet33339999@gmail.com';
$email_subject = '🚨 NEW AUTO TRANSPORT LEAD: ' . ($lead_record['name'] ?: 'Website Lead');
$email_headers = "From: Sky Auto Services <noreply@skyautoservices.com>\r\n" .
                 "Reply-To: " . ($lead_record['email'] ?: 'sales@skyservicesllc.com') . "\r\n" .
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
    <div class='field'><span class='label'>Customer Name:</span> <div class='val'><b>" . htmlspecialchars($lead_record['name']) . "</b></div></div>
    <div class='field'><span class='label'>Phone:</span> <div class='val'><a href='tel:" . htmlspecialchars($lead_record['phone']) . "'>" . htmlspecialchars($lead_record['phone']) . "</a></div></div>
    <div class='field'><span class='label'>Email:</span> <div class='val'><a href='mailto:" . htmlspecialchars($lead_record['email']) . "'>" . htmlspecialchars($lead_record['email']) . "</a></div></div>
    <hr style='border:0;border-top:1px solid #e2e8f0;margin:15px 0;'>
    <div class='field'><span class='label'>Route:</span> <div class='val'>" . htmlspecialchars($lead_record['origin']) . " ➔ " . htmlspecialchars($lead_record['destination']) . " (" . htmlspecialchars($lead_record['distance']) . " miles)</div></div>
    <div class='field'><span class='label'>Vehicle:</span> <div class='val'>" . htmlspecialchars($lead_record['vehicle']) . "</div></div>
    <div class='field'><span class='label'>Transport Type:</span> <div class='val'>" . htmlspecialchars($lead_record['transport_type']) . "</div></div>
    <div class='field'><span class='label'>Price Quoted:</span> <div class='val'><span class='badge'>" . htmlspecialchars($lead_record['price']) . "</span></div></div>
    " . (!empty($lead_record['comments']) ? ("<div class='field'><span class='label'>Comments:</span> <div class='val'>" . htmlspecialchars($lead_record['comments']) . "</div></div>") : "") . "
    <hr style='border:0;border-top:1px solid #e2e8f0;margin:15px 0;'>
    <p style='font-size:13px;color:#94a3b8;'>Quote ID: " . htmlspecialchars($quote_id) . " | Received: " . $timestamp . "</p>
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
    'google_response' => $google_res_text,
    'direct_mail_sent' => $mail_sent,
    'data' => $lead_record
]);
exit;
