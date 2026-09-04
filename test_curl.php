<?php
$google_sheets_url = 'https://script.google.com/macros/s/AKfycbxjTrpOti2ZPZscPAbgKRTPc3PeAkNyBMCVnieVW2BtnUsnQsiIBp5wKo3JVKb6F43m/exec';
$google_payload = ['test' => 'data'];
$ch = curl_init($google_sheets_url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($google_payload));
curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
$google_response = curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$eff_url = curl_getinfo($ch, CURLINFO_EFFECTIVE_URL);
echo "HTTP: $http_code\n";
echo "Effective URL: $eff_url\n";
echo "Response: $google_response\n";
?>
