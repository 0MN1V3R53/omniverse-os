/**
 * ==============================================================================
 * 🚗 SKY AUTO SERVICES - CRM & SMS TEXT DISPATCH ENGINE v3.0 (POD 20 & WEB)
 * ==============================================================================
 * Features:
 * 1. 🚗 Sky Auto CRM Menu (Email alerts, lead intake, CRM formatting, permissions)
 * 2. 💬 Sky SMS & Text Dispatch Menu (Custom SMS, instant quote templates, follow-ups)
 * 3. 📋 Client Profiles Engine (Auto-compiles customer directory with history & routes)
 * 4. 📜 SMS History & Audit Ledger (Records every sent/received text message)
 * 5. ⚡ Multi-Gateway SMS Sender (1-Click Device SMS, Android Gateway, Cloud API)
 * ==============================================================================
 */

/**
 * 1. DUAL MENU INITIALIZATION ON SPREADSHEET OPEN
 */
function onOpen(e) {
  try {
    var ui = SpreadsheetApp.getUi();
    
    // Menu 1: Core CRM & Email Engine
    ui.createMenu('🚗 Sky Auto CRM')
      .addItem('🔍 View Sent Emails in Gmail', 'checkSentEmailAudit')
      .addItem('🧪 Send Test Email Alert', 'sendTestEmailAlert')
      .addItem('📥 Insert Test Lead & Send Email', 'insertTestLeadAndEmail')
      .addSeparator()
      .addItem('📊 Setup / Format All CRM Sheets', 'setupAllCRMSheets')
      .addItem('⚙️ Authorize Email Permissions', 'testAuth')
      .addToUi();

    // Menu 2: Dedicated SMS & Text Messaging Engine
    ui.createMenu('💬 Sky SMS & Text Dispatch')
      .addItem('📱 Send Custom SMS (Selected Lead Row)', 'sendCustomSMSToSelectedRow')
      .addItem('⚡ Send Instant Quote SMS (Selected Lead Row)', 'sendInstantQuoteSMSToSelectedRow')
      .addItem('🔄 Send Follow-Up SMS: "Still Shipping?" (Selected Row)', 'sendFollowUpSMSToSelectedRow')
      .addSeparator()
      .addItem('📋 Build / Refresh Client Profiles Sheet', 'buildOrRefreshClientProfiles')
      .addItem('📜 View SMS History & Audit Log', 'openSMSHistorySheet')
      .addSeparator()
      .addItem('🧪 Send Test SMS to Any Phone Number', 'sendTestSMSPrompt')
      .addItem('⚙️ SMS Gateway / API Settings', 'configureSMSGatewaySettings')
      .addToUi();
      
  } catch (err) {
    Logger.log("UI menu skipped in non-browser context: " + err.message);
  }
}

/**
 * 2. INCOMING WEBHOOK HANDLER (GET / POST)
 */
function doGet(e) {  
  return ContentService.createTextOutput(JSON.stringify({ 
    status: "ok", 
    message: "Sky Auto Services CRM & SMS Engine v3.0 Active",
    timestamp: new Date().toISOString()
  })).setMimeType(ContentService.MimeType.JSON);
}  

function doPost(e) {  
  var emailStatus = "⏳ Pending";
  var isSuccess = false;
  
  try {  
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var liveSheet = ss.getSheetByName("Live Leads") || ss.getActiveSheet();  
    var data = {};
    
    if (e && e.postData && e.postData.contents) {
      try { data = JSON.parse(e.postData.contents); } catch (err) { data = e.parameter || {}; }
    } else if (e && e.parameter) {
      data = e.parameter;
    }
    
    var leadName = data.name || data.full_name || ((data.firstName || '') + ' ' + (data.lastName || '')).trim() || 'Website Visitor';
    var leadOrigin = data.origin || data.pickupCity || data.pickup_city || '';
    var leadDest = data.destination || data.deliveryCity || data.delivery_city || '';
    var leadVehicle = data.vehicle || ((data.vehicleYear || '') + ' ' + (data.vehicleMake || '') + ' ' + (data.vehicleModel || '')).trim() || '';
    var leadDistance = data.distance || data.distance_miles || '';
    var leadTransport = data.transport_type || data.transportType || 'Standard Open';
    var leadPrice = data.price ? ('$' + String(data.price).replace('$', '')) : '';
    var leadEmail = data.email || '';
    var leadPhone = normalizePhoneNumber(data.phone || '');
    var notes = data.comments || data.more_info || data.notes || '';
    
    var recipientEmail = "sales@skyservicesllc.com";  
    var subject = "🚨 NEW AUTO TRANSPORT LEAD: " + leadName;  
    var timeString = Utilities.formatDate(new Date(), "GMT-5", "hh:mm:ss a 'EST'");
    
    var body = "Sky Auto Services - New Lead Alert!\n\n" +  
               "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n" +
               "CUSTOMER DETAILS:\n" +
               "• Name: " + leadName + "\n" +  
               "• Phone: " + (leadPhone || "N/A") + "\n" +  
               "• Email: " + (leadEmail || "N/A") + "\n\n" +  
               "TRANSPORT DETAILS:\n" +
               "• Route: " + (leadOrigin || "N/A") + " ➔ " + (leadDest || "N/A") + "\n" +  
               "• Vehicle: " + (leadVehicle || "N/A") + "\n" +  
               "• Transport: " + (leadTransport || "N/A") + "\n" +  
               "• Distance: " + (leadDistance ? (leadDistance + " miles") : "N/A") + "\n" +
               "• Quoted Price: " + (leadPrice || "N/A") + "\n" +
               "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n" +
               "Dispatched At: " + timeString;

    // 1. Dispatch Email Notification
    try {
      GmailApp.sendEmail(recipientEmail, subject, body, { name: "Sky Auto CRM" });
      emailStatus = "✅ SENT to " + recipientEmail + " (" + timeString + ")";
      isSuccess = true;
    } catch (gErr) {
      try {
        MailApp.sendEmail(recipientEmail, subject, body);
        emailStatus = "✅ SENT (MailApp) to " + recipientEmail + " (" + timeString + ")";
        isSuccess = true;
      } catch (mErr) {
        emailStatus = "❌ FAILED: " + mErr.message;
      }
    }

    // 2. Append Row to Live Leads
    liveSheet.appendRow([  
      new Date(),  
      leadOrigin,  
      leadDest,  
      leadVehicle,  
      leadDistance,  
      leadTransport,  
      leadPrice,  
      leadName,  
      leadEmail,  
      leadPhone,  
      'New',  
      emailStatus,
      notes  
    ]);   
    
    var lastRow = liveSheet.getLastRow();
    var statusCell = liveSheet.getRange(lastRow, 12);
    if (isSuccess) {
      statusCell.setBackground("#dcfce7").setFontColor("#166534").setFontWeight("bold");
    } else {
      statusCell.setBackground("#fee2e2").setFontColor("#991b1b").setFontWeight("bold");
    }
    
    // 3. Automatically Update / Create Record in Client Profiles Sheet
    updateClientProfileRecord({
      name: leadName,
      phone: leadPhone,
      email: leadEmail,
      origin: leadOrigin,
      destination: leadDest,
      vehicle: leadVehicle,
      transport: leadTransport,
      price: leadPrice,
      notes: notes,
      receivedAt: new Date()
    });
    
    return ContentService.createTextOutput(JSON.stringify({ 
      "result": "success", 
      "emailStatus": emailStatus,
      "leadPhone": leadPhone,
      "row": lastRow 
    })).setMimeType(ContentService.MimeType.JSON);   
    
  } catch(error) {  
    return ContentService.createTextOutput(JSON.stringify({ "result": "error", "message": error.toString() }))  
      .setMimeType(ContentService.MimeType.JSON);  
  } 
}

/**
 * 3. CLIENT PROFILE BUILDER ENGINE
 */
function buildOrRefreshClientProfiles() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var liveSheet = ss.getSheetByName("Live Leads");
  if (!liveSheet) {
    SpreadsheetApp.getUi().alert("⚠️ 'Live Leads' sheet not found. Please run 'Setup / Format All CRM Sheets' first.");
    return;
  }
  
  var profileSheet = ss.getSheetByName("Client Profiles");
  if (!profileSheet) {
    profileSheet = ss.insertSheet("Client Profiles");
  }
  
  // Format Profile Headers
  var headers = [
    "Client ID", "Full Name", "Phone Number", "Email Address", "Primary Route", 
    "Vehicle Details", "Transport Type", "Quoted Price", "Lead Stage", 
    "Total Texts Sent", "Last Text Sent", "Quick 1-Click SMS Link", "Profile Created", "Notes"
  ];
  profileSheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  profileSheet.getRange(1, 1, 1, headers.length)
    .setFontWeight("bold")
    .setBackground("#0f172a")
    .setFontColor("#38bdf8");
  profileSheet.setFrozenRows(1);
  
  var leadsData = liveSheet.getDataRange().getValues();
  if (leadsData.length <= 1) {
    SpreadsheetApp.getUi().alert("ℹ️ No leads found in 'Live Leads' to compile.");
    return;
  }
  
  // Read existing SMS counts
  var smsHistorySheet = ss.getSheetByName("SMS History");
  var smsStats = getSMSStatsByPhone(smsHistorySheet);
  
  var clientsMap = {};
  
  // Process rows from Live Leads (Skipping header row)
  for (var i = 1; i < leadsData.length; i++) {
    var row = leadsData[i];
    var receivedDate = row[0];
    var origin = row[1] || "";
    var dest = row[2] || "";
    var vehicle = row[3] || "";
    var transport = row[5] || "Standard";
    var price = row[6] || "";
    var name = (row[7] || "").toString().trim() || "Valued Customer";
    var email = (row[8] || "").toString().trim();
    var rawPhone = (row[9] || "").toString().trim();
    var phone = normalizePhoneNumber(rawPhone);
    var stage = row[10] || "New";
    var notes = row[12] || "";
    
    if (!phone && !email) continue;
    var clientKey = phone || email;
    
    var routeStr = (origin && dest) ? (origin + " ➔ " + dest) : (origin || dest || "US Domestic");
    var smsInfo = smsStats[phone] || { count: 0, lastDate: "None" };
    
    // Construct prefilled 1-Click SMS link
    var quoteMsg = encodeURIComponent("Hi " + name + ", this is Sky Auto Services regarding your " + vehicle + " transport (" + routeStr + "). Your locked rate is " + price + " with $0 upfront deposit! When are you looking to ship?");
    var smsUrl = phone ? ('=HYPERLINK("sms:' + phone + '?body=' + quoteMsg + '", "📱 Send Text")') : "No Phone";
    
    clientsMap[clientKey] = [
      "SKY-" + (1000 + Object.keys(clientsMap).length + 1),
      name,
      phone,
      email,
      routeStr,
      vehicle,
      transport,
      price,
      stage,
      smsInfo.count,
      smsInfo.lastDate,
      smsUrl,
      receivedDate ? Utilities.formatDate(new Date(receivedDate), "GMT-5", "yyyy-MM-dd HH:mm") : "",
      notes
    ];
  }
  
  // Clear old data and write refreshed client profiles
  var totalRows = profileSheet.getLastRow();
  if (totalRows > 1) {
    profileSheet.getRange(2, 1, totalRows - 1, headers.length).clearContent();
  }
  
  var clientRows = Object.values(clientsMap);
  if (clientRows.length > 0) {
    profileSheet.getRange(2, 1, clientRows.length, headers.length).setValues(clientRows);
    
    // Auto-fit column widths
    for (var c = 1; c <= headers.length; c++) {
      profileSheet.autoResizeColumn(c);
    }
  }
  
  try {
    SpreadsheetApp.getUi().alert("✅ Client Profiles Compiled!", "Built/Updated " + clientRows.length + " unique client profiles with SMS links.", SpreadsheetApp.getUi().ButtonSet.OK);
  } catch(e){}
}

function updateClientProfileRecord(lead) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var profileSheet = ss.getSheetByName("Client Profiles");
  if (!profileSheet) return;
  
  var phone = normalizePhoneNumber(lead.phone);
  if (!phone) return;
  
  var data = profileSheet.getDataRange().getValues();
  var foundRow = -1;
  
  for (var i = 1; i < data.length; i++) {
    if (data[i][2] === phone) {
      foundRow = i + 1;
      break;
    }
  }
  
  var routeStr = (lead.origin && lead.destination) ? (lead.origin + " ➔ " + lead.destination) : "US Domestic";
  var quoteMsg = encodeURIComponent("Hi " + lead.name + ", this is Sky Auto Services regarding your " + lead.vehicle + " shipping (" + routeStr + "). Locked price: " + lead.price + " with $0 deposit!");
  var smsUrl = '=HYPERLINK("sms:' + phone + '?body=' + quoteMsg + '", "📱 Send Text")';
  
  if (foundRow > 0) {
    // Update existing profile
    profileSheet.getRange(foundRow, 5).setValue(routeStr);
    profileSheet.getRange(foundRow, 6).setValue(lead.vehicle);
    profileSheet.getRange(foundRow, 8).setValue(lead.price);
    profileSheet.getRange(foundRow, 12).setValue(smsUrl);
  } else {
    // Append new profile
    var newId = "SKY-" + (1000 + data.length);
    profileSheet.appendRow([
      newId, lead.name, phone, lead.email, routeStr, lead.vehicle, 
      lead.transport, lead.price, "New", 0, "None", smsUrl, new Date(), lead.notes
    ]);
  }
}

/**
 * 4. SMS DISPATCH & TEXT RECORDING ENGINE
 */
function sendCustomSMSToSelectedRow() {
  var lead = getSelectedRowLeadData();
  if (!lead) return;
  
  var ui = SpreadsheetApp.getUi();
  var defaultMsg = "Hi " + lead.name + ", this is Sky Auto Services regarding your car shipping request. How can we assist you with your transport today?";
  
  var response = ui.prompt(
    "📱 Send Custom SMS to " + lead.name,
    "Recipient: " + lead.phone + "\n\nEnter your message text below:",
    ui.ButtonSet.OK_CANCEL
  );
  
  if (response.getSelectedButton() !== ui.Button.OK) return;
  var customText = response.getResponseText().trim();
  if (!customText) {
    ui.alert("⚠️ Message was empty. Text not sent.");
    return;
  }
  
  dispatchAndRecordSMS(lead.name, lead.phone, customText, "Custom Direct Text");
}

function sendInstantQuoteSMSToSelectedRow() {
  var lead = getSelectedRowLeadData();
  if (!lead) return;
  
  var route = (lead.origin && lead.destination) ? (lead.origin + " to " + lead.destination) : "your route";
  var vehicle = lead.vehicle || "your vehicle";
  var price = lead.price || "the locked online rate";
  
  var quoteText = "Hi " + lead.name + "! This is Sky Auto Services. Your instant quote for shipping your " + vehicle + " (" + route + ") is " + price + " with $0 upfront deposit & $1M insurance included. Reply YES or call (224) 449-0397 to lock in your pickup dates!";
  
  var ui = SpreadsheetApp.getUi();
  var confirm = ui.alert(
    "⚡ Send Instant Quote SMS",
    "Sending to: " + lead.name + " (" + lead.phone + ")\n\nMessage:\n\"" + quoteText + "\"",
    ui.ButtonSet.YES_NO
  );
  
  if (confirm !== ui.Button.YES) return;
  dispatchAndRecordSMS(lead.name, lead.phone, quoteText, "Instant Quote SMS Template");
}

function sendFollowUpSMSToSelectedRow() {
  var lead = getSelectedRowLeadData();
  if (!lead) return;
  
  var vehicle = lead.vehicle || "your vehicle";
  var followUpText = "Hi " + lead.name + ", quick update from Sky Auto Services dispatch: We have carriers verified along your route for your " + vehicle + ". Are you still looking to transport? Let us know so we can reserve your carrier spot!";
  
  var ui = SpreadsheetApp.getUi();
  var confirm = ui.alert(
    "🔄 Send Follow-Up SMS",
    "Sending to: " + lead.name + " (" + lead.phone + ")\n\nMessage:\n\"" + followUpText + "\"",
    ui.ButtonSet.YES_NO
  );
  
  if (confirm !== ui.Button.YES) return;
  dispatchAndRecordSMS(lead.name, lead.phone, followUpText, "Follow-Up Template");
}

function sendTestSMSPrompt() {
  var ui = SpreadsheetApp.getUi();
  var phonePrompt = ui.prompt("🧪 Send Test SMS", "Enter destination US mobile number (e.g. +1 224 449 0397):", ui.ButtonSet.OK_CANCEL);
  if (phonePrompt.getSelectedButton() !== ui.Button.OK) return;
  
  var phone = normalizePhoneNumber(phonePrompt.getResponseText());
  if (!phone) {
    ui.alert("❌ Invalid US phone number.");
    return;
  }
  
  var testMsg = "Sky Auto Services CRM Test: SMS Gateway & Dispatch Ledger is 100% operational! (Dispatched at " + Utilities.formatDate(new Date(), "GMT-5", "hh:mm a 'EST'") + ")";
  dispatchAndRecordSMS("Test Customer", phone, testMsg, "Test Verification SMS");
}

/**
 * 5. CORE DISPATCHER & AUDIT LOGGER
 */
function dispatchAndRecordSMS(recipientName, rawPhone, messageBody, templateType) {
  var phone = normalizePhoneNumber(rawPhone);
  var ui = SpreadsheetApp.getUi();
  
  if (!phone) {
    ui.alert("❌ Error: Recipient phone number is missing or invalid.");
    return;
  }
  
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var logSheet = ss.getSheetByName("SMS History") || ss.insertSheet("SMS History");
  
  // Format log headers if new
  if (logSheet.getLastRow() === 0) {
    var headers = ["Timestamp", "Client Name", "Phone Number", "Direction", "Template / Category", "Message Content", "Status", "Delivery Gateway", "Agent / Dispatcher"];
    logSheet.appendRow(headers);
    logSheet.getRange(1, 1, 1, headers.length).setFontWeight("bold").setBackground("#1e293b").setFontColor("#ffffff");
    logSheet.setFrozenRows(1);
  }
  
  var gatewayUrl = PropertiesService.getScriptProperties().getProperty("SMS_GATEWAY_URL");
  var gatewayToken = PropertiesService.getScriptProperties().getProperty("SMS_GATEWAY_TOKEN");
  var sendStatus = "✅ Dispatched";
  var deliveryMethod = "1-Click Native Device / Web";
  
  // Method 1: If Open-Source Android SMS Gateway / Cloud Webhook configured
  if (gatewayUrl) {
    try {
      var payload = {
        phone: phone,
        message: messageBody,
        token: gatewayToken || ""
      };
      var options = {
        method: "post",
        contentType: "application/json",
        payload: JSON.stringify(payload),
        muteHttpExceptions: true
      };
      var response = UrlFetchApp.fetch(gatewayUrl, options);
      var respCode = response.getResponseCode();
      if (respCode >= 200 && respCode < 300) {
        sendStatus = "✅ Delivered via Gateway (" + respCode + ")";
        deliveryMethod = "Android Gateway API";
      } else {
        sendStatus = "⚠️ Gateway Error (" + respCode + ") - Fallback to 1-Click";
      }
    } catch(err) {
      sendStatus = "⚠️ Gateway Timeout - Fallback to 1-Click";
    }
  }
  
  // Record in SMS History Sheet
  var now = new Date();
  var currentUser = Session.getActiveUser().getEmail() || "Dispatcher (Sky CRM)";
  logSheet.appendRow([
    now,
    recipientName,
    phone,
    "Outgoing",
    templateType || "Direct SMS",
    messageBody,
    sendStatus,
    deliveryMethod,
    currentUser
  ]);
  
  // Highlight last row in green
  var lastRow = logSheet.getLastRow();
  logSheet.getRange(lastRow, 7).setBackground("#dcfce7").setFontColor("#166534").setFontWeight("bold");
  
  // Show 1-Click Launch Modal for Immediate Mobile/Web Dispatch
  var smsUri = "sms:" + phone + "?body=" + encodeURIComponent(messageBody);
  var gVoiceUri = "https://voice.google.com/u/0/messages";
  
  var htmlOutput = HtmlService.createHtmlOutput(
    '<div style="font-family: Arial, sans-serif; padding: 15px; color: #1e293b;">' +
    '<h3 style="color: #0284c7; margin-top: 0;">📱 SMS Dispatched & Recorded!</h3>' +
    '<p><strong>Recipient:</strong> ' + recipientName + ' (' + phone + ')</p>' +
    '<div style="background: #f1f5f9; padding: 10px; border-radius: 6px; font-size: 13px; margin: 10px 0; max-height: 100px; overflow-y: auto;">' +
    messageBody +
    '</div>' +
    '<p style="font-size: 12px; color: #64748b;">Logged in <strong>SMS History</strong> (Row ' + lastRow + '). Click below to send directly from your phone/desktop:</p>' +
    '<div style="margin-top: 15px; display: flex; gap: 10px;">' +
    '<a href="' + smsUri + '" target="_blank" style="background: #0284c7; color: white; padding: 10px 18px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">📲 Open in Messages App</a>' +
    '<a href="' + gVoiceUri + '" target="_blank" style="background: #475569; color: white; padding: 10px 18px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">🌐 Open Google Voice</a>' +
    '</div>' +
    '</div>'
  ).setWidth(480).setHeight(280);
  
  ui.showModalDialog(htmlOutput, "Sky Auto SMS Dispatcher");
}

/**
 * 6. HELPER FUNCTIONS & SHEET SETUP
 */
function getSelectedRowLeadData() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getActiveSheet();
  var rowIdx = sheet.getActiveCell().getRow();
  var ui = SpreadsheetApp.getUi();
  
  if (rowIdx <= 1) {
    ui.alert("⚠️ Please select a row containing client data (Row 2 or below).");
    return null;
  }
  
  var rowData = sheet.getRange(rowIdx, 1, 1, sheet.getLastColumn()).getValues()[0];
  var sheetName = sheet.getName();
  
  var lead = {};
  if (sheetName === "Live Leads") {
    lead.origin = rowData[1] || "";
    lead.destination = rowData[2] || "";
    lead.vehicle = rowData[3] || "";
    lead.price = rowData[6] || "";
    lead.name = rowData[7] || "Valued Client";
    lead.email = rowData[8] || "";
    lead.phone = rowData[9] || "";
  } else if (sheetName === "Client Profiles") {
    lead.name = rowData[1] || "Valued Client";
    lead.phone = rowData[2] || "";
    lead.email = rowData[3] || "";
    var routeParts = (rowData[4] || "").split("➔");
    lead.origin = routeParts[0] ? routeParts[0].trim() : "";
    lead.destination = routeParts[1] ? routeParts[1].trim() : "";
    lead.vehicle = rowData[5] || "";
    lead.price = rowData[7] || "";
  } else {
    // Fallback for custom formatted sheet
    lead.name = rowData[7] || rowData[1] || rowData[2] || "Valued Client";
    lead.phone = rowData[9] || rowData[4] || rowData[2] || "";
    lead.origin = rowData[1] || "";
    lead.destination = rowData[2] || "";
    lead.vehicle = rowData[3] || "";
    lead.price = rowData[6] || "";
  }
  
  lead.phone = normalizePhoneNumber(lead.phone);
  if (!lead.phone) {
    var promptPhone = ui.prompt("📞 Missing Phone Number", "Enter phone number for " + lead.name + ":", ui.ButtonSet.OK_CANCEL);
    if (promptPhone.getSelectedButton() === ui.Button.OK) {
      lead.phone = normalizePhoneNumber(promptPhone.getResponseText());
    }
  }
  
  return lead;
}

function normalizePhoneNumber(phoneStr) {
  if (!phoneStr) return "";
  var cleaned = phoneStr.toString().replace(/[^0-9+]/g, '');
  if (cleaned.length === 10) {
    return "+1" + cleaned;
  } else if (cleaned.length === 11 && cleaned.startsWith("1")) {
    return "+" + cleaned;
  }
  return cleaned.startsWith("+") ? cleaned : ("+" + cleaned);
}

function getSMSStatsByPhone(historySheet) {
  var stats = {};
  if (!historySheet || historySheet.getLastRow() <= 1) return stats;
  
  var data = historySheet.getDataRange().getValues();
  for (var i = 1; i < data.length; i++) {
    var date = data[i][0];
    var phone = data[i][2];
    if (!phone) continue;
    
    if (!stats[phone]) {
      stats[phone] = { count: 0, lastDate: "" };
    }
    stats[phone].count += 1;
    if (date) {
      stats[phone].lastDate = Utilities.formatDate(new Date(date), "GMT-5", "MMM dd, hh:mm a");
    }
  }
  return stats;
}

function setupAllCRMSheets() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  
  // 1. Format Live Leads
  formatSkyCRM();
  
  // 2. Setup Client Profiles
  buildOrRefreshClientProfiles();
  
  // 3. Setup SMS History
  openSMSHistorySheet();
  
  SpreadsheetApp.getUi().alert("✅ All CRM Sheets Formatted & Synchronized:\n\n1. Live Leads (Incoming Stream)\n2. Client Profiles (Directory & SMS Links)\n3. SMS History (Full Text Audit Ledger)");
}

function openSMSHistorySheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var logSheet = ss.getSheetByName("SMS History");
  if (!logSheet) {
    logSheet = ss.insertSheet("SMS History");
    var headers = ["Timestamp", "Client Name", "Phone Number", "Direction", "Template / Category", "Message Content", "Status", "Delivery Gateway", "Agent / Dispatcher"];
    logSheet.appendRow(headers);
    logSheet.getRange(1, 1, 1, headers.length).setFontWeight("bold").setBackground("#0f172a").setFontColor("#38bdf8");
    logSheet.setFrozenRows(1);
  }
  ss.setActiveSheet(logSheet);
}

function configureSMSGatewaySettings() {
  var ui = SpreadsheetApp.getUi();
  var props = PropertiesService.getScriptProperties();
  var currentUrl = props.getProperty("SMS_GATEWAY_URL") || "None (1-Click Device Mode Active)";
  
  var prompt = ui.prompt(
    "⚙️ SMS Gateway / Webhook Configuration",
    "Current Webhook URL: " + currentUrl + "\n\nEnter your Android SMS Gateway or Twilio API Webhook URL (Leave blank to use free 1-Click mode):",
    ui.ButtonSet.OK_CANCEL
  );
  
  if (prompt.getSelectedButton() === ui.Button.OK) {
    var newUrl = prompt.getResponseText().trim();
    if (newUrl) {
      props.setProperty("SMS_GATEWAY_URL", newUrl);
      ui.alert("✅ Gateway Webhook URL Saved!");
    } else {
      props.deleteProperty("SMS_GATEWAY_URL");
      ui.alert("✅ Switched to Free 1-Click Native Device / Web Messaging mode.");
    }
  }
}

// Retain legacy formatSkyCRM and testAuth for 100% backward compatibility
function formatSkyCRM() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName("Live Leads") || ss.getActiveSheet();
  sheet.setName("Live Leads");

  const headers = [
    "Received At", "Origin", "Destination", "Vehicle", "Distance", 
    "Transport Type", "Price", "Customer Name", "Email", "Phone", "Lead Stage", 
    "Email Notification Status", "Notes"
  ];
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  sheet.getRange(1, 1, 1, headers.length).setFontWeight("bold").setBackground("#1e293b").setFontColor("#ffffff");
  sheet.setFrozenRows(1);
}

function checkSentEmailAudit() {
  try {
    const ui = SpreadsheetApp.getUi();
    const threads = GmailApp.search('to:sales@skyservicesllc.com', 0, 5);
    if (threads.length === 0) {
      ui.alert("📬 Sent Mail Report", "No sent emails to sales@skyservicesllc.com found in this Gmail account yet.", ui.ButtonSet.OK);
      return;
    }
    
    var msg = "Found " + threads.length + " recent sent emails to sales@skyservicesllc.com:\n\n";
    for (var i = 0; i < threads.length; i++) {
      var lastMsgDate = threads[i].getLastMessageDate();
      var subject = threads[i].getFirstMessageSubject();
      msg += (i + 1) + ". " + Utilities.formatDate(lastMsgDate, "GMT-5", "MMM dd, hh:mm a") + " — " + subject + "\n";
    }
    
    ui.alert("✅ Verified Sent Emails (From Your Gmail)", msg, ui.ButtonSet.OK);
  } catch (err) {
    Logger.log("Audit error: " + err.message);
  }
}

function sendTestEmailAlert() {
  const recipientEmail = "sales@skyservicesllc.com";
  try {
    const ui = SpreadsheetApp.getUi();
    GmailApp.sendEmail(
      recipientEmail, 
      "🧪 TEST EMAIL ALERT: Sky Auto Services CRM", 
      "This is a verified test email sent from your Google Sheet.\n\nStatus: ✅ Active and Delivered!"
    );
    ui.alert("✅ Email Sent Successfully!", "Delivered to " + recipientEmail + ".\nYou can also click 'View Sent Emails in Gmail' to verify.", ui.ButtonSet.OK);
  } catch (err) {
    try {
      SpreadsheetApp.getUi().alert("❌ Email Failed", err.message, SpreadsheetApp.getUi().ButtonSet.OK);
    } catch(e){}
  }
}

function insertTestLeadAndEmail() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName("Live Leads") || ss.getActiveSheet();
  var timeStr = Utilities.formatDate(new Date(), "GMT-5", "hh:mm:ss a 'EST'");
  var emailStatus = "⏳ Pending";
  var isSuccess = false;
  
  try {
    GmailApp.sendEmail(
      "sales@skyservicesllc.com", 
      "🚨 NEW AUTO TRANSPORT LEAD: Bruce Wayne (Test)", 
      "Sky Auto Services - Test Lead inserted from Google Sheet.\n\nRoute: Chicago, IL -> Miami, FL\nPrice: $1,450"
    );
    emailStatus = "✅ SENT to sales@skyservicesllc.com (" + timeStr + ")";
    isSuccess = true;
  } catch (e) {
    emailStatus = "❌ FAILED: " + e.message;
  }
  
  sheet.appendRow([
    new Date(), "Chicago, IL", "Miami, FL", "2024 Tesla Model S", "1,330", 
    "Enclosed", "$1,450", "Bruce Wayne (Test)", "sales@skyservicesllc.com", "(224) 449-0397", "New", emailStatus, "Toolbar Test"
  ]);
  
  var lastRow = sheet.getLastRow();
  var statusCell = sheet.getRange(lastRow, 12);
  if (isSuccess) {
    statusCell.setBackground("#dcfce7").setFontColor("#166534").setFontWeight("bold");
  } else {
    statusCell.setBackground("#fee2e2").setFontColor("#991b1b").setFontWeight("bold");
  }
  
  // Also create client profile for test lead
  updateClientProfileRecord({
    name: "Bruce Wayne (Test)",
    phone: "+12244490397",
    email: "sales@skyservicesllc.com",
    origin: "Chicago, IL",
    destination: "Miami, FL",
    vehicle: "2024 Tesla Model S",
    transport: "Enclosed",
    price: "$1,450",
    notes: "Toolbar Test",
    receivedAt: new Date()
  });
  
  try {
    SpreadsheetApp.getUi().alert("✅ Test Completed", "Lead row added to row " + lastRow + " with status:\n" + emailStatus + "\n\nClient profile updated in 'Client Profiles' sheet.", SpreadsheetApp.getUi().ButtonSet.OK);
  } catch(e){}
}

function testAuth() { 
  try {
    const ui = SpreadsheetApp.getUi();
    var quota = MailApp.getRemainingDailyQuota();
    ui.alert("✅ Permissions Active", "Authorized to send emails & manage sheets. Daily email quota remaining: " + quota, ui.ButtonSet.OK);
  } catch (e) {
    Logger.log("Auth check: " + e.message);
  }
}
