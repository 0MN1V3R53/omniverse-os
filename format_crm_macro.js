function formatSkyCRM() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getActiveSheet();
  
  // 1. Rename Document
  ss.rename("Sky Auto Services CRM");
  sheet.setName("Live Leads");

  // 2. Set Headers
  const headers = [
    "Quote ID", "Received At", "Full Name", "Email", "Phone", 
    "Origin", "Destination", "Miles", "Vehicle", "Type", 
    "Condition", "Transport", "Date", "Price", "Range", "ETA",
    "Lead Stage", "Call Status", "Answer Status", "Availability", "Next Follow-Up", "Notes"
  ];
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  sheet.getRange(1, 1, 1, headers.length).setFontWeight("bold").setBackground("#202124").setFontColor("#ffffff");
  
  // 3. Freeze Panes
  sheet.setFrozenRows(1);
  sheet.setFrozenColumns(3);
  
  // 4. Dropdowns and Data Validation (Start from Row 2 to 1000)
  const maxRows = Math.max(sheet.getMaxRows(), 1000);
  if (sheet.getMaxRows() < 1000) {
      sheet.insertRowsAfter(sheet.getMaxRows(), 1000 - sheet.getMaxRows());
  }
  
  // Lead Stage (Col 17 - Q)
  const stageRule = SpreadsheetApp.newDataValidation().requireValueInList(["New", "Contacted", "Negotiating", "Closed Won", "Closed Lost"], true).build();
  sheet.getRange(2, 17, maxRows - 1).setDataValidation(stageRule);
  
  // Call Status (Col 18 - R)
  const callRule = SpreadsheetApp.newDataValidation().requireValueInList(["Called", "Not Called"], true).build();
  sheet.getRange(2, 18, maxRows - 1).setDataValidation(callRule);
  
  // Answer Status (Col 19 - S)
  const answerRule = SpreadsheetApp.newDataValidation().requireValueInList(["Answered", "Not Answered"], true).build();
  sheet.getRange(2, 19, maxRows - 1).setDataValidation(answerRule);
  
  // Availability (Col 20 - T)
  const availRule = SpreadsheetApp.newDataValidation().requireValueInList(["Available", "Unavailable"], true).build();
  sheet.getRange(2, 20, maxRows - 1).setDataValidation(availRule);

  // 5. Conditional Formatting for colors
  let rules = sheet.getConditionalFormatRules();
  
  // Helper to add color rules
  function addRule(text, bgColor, fontColor, colIndex) {
    const range = sheet.getRange(2, colIndex, maxRows - 1, 1);
    const rule = SpreadsheetApp.newConditionalFormatRule()
      .whenTextEqualTo(text)
      .setBackground(bgColor)
      .setFontColor(fontColor)
      .setRanges([range])
      .build();
    rules.push(rule);
  }
  
  addRule("Closed Won", "#b7e1cd", "#0f5232", 17); // Green
  addRule("Closed Lost", "#f4c7c3", "#741b47", 17); // Red
  addRule("New", "#c9daf8", "#1155cc", 17); // Blue
  addRule("Called", "#d9ead3", "#274e13", 18);
  addRule("Not Called", "#fce5cd", "#b45f06", 18);
  addRule("Answered", "#d9ead3", "#274e13", 19);
  addRule("Not Answered", "#f4c7c3", "#741b47", 19);
  
  sheet.setConditionalFormatRules(rules);

  // 6. Column Widths
  const widths = {
    1: 180, // ID
    2: 150, // Received
    3: 150, // Name
    4: 180, // Email
    5: 120, // Phone
    6: 120, // Origin
    7: 120, // Dest
    8: 70,  // Miles
    9: 180, // Vehicle
    10: 100, // Type
    11: 100, // Condition
    12: 130, // Transport
    13: 100, // Date
    14: 90,  // Price
    15: 110, // Range
    16: 80,  // ETA
    17: 130, // Stage
    18: 110, // Call
    19: 130, // Answer
    20: 110, // Avail
    21: 120, // Follow Up
    22: 300  // Notes
  };
  
  for (let col in widths) {
    sheet.setColumnWidth(parseInt(col), widths[col]);
  }
  
  // 7. Alternating Colors
  const bandings = sheet.getBandings();
  bandings.forEach(b => b.remove());
  sheet.getRange(1, 1, maxRows, headers.length).applyRowBanding(SpreadsheetApp.BandingTheme.LIGHT_GREY);
  
  try {
      SpreadsheetApp.getUi().alert("CRM Formatting Complete!");
  } catch(e) {}
}
