tell application "Safari"
    activate
    open location "http://localhost:8081/"
    delay 5
    do JavaScript "
        document.getElementById('quote_origin').value = '90210';
        document.getElementById('quote_destination').value = '10001';
        document.getElementById('quote_year_make').value = '2026 Porsche';
        document.getElementById('quote_model').value = '911 GT3';
        document.getElementById('quote_name').value = 'Test User';
        document.getElementById('quote_phone').value = '5555555555';
        document.getElementById('quote_email').value = 'test@example.com';
        document.getElementById('btn_submit_quote').click();
    " in current tab of window 1
    delay 5
end tell
