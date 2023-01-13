// This is a script to aid in reformatting of donor donations

// Sheets
const rawDataSheet = "Paste Raw CSV"
const rulesSheet = "Rules"
const outputSheet = "Run/Output"

function formatDonors() {
  try {
    Logger.log("Starting Formatting")
    let spreadsheet = SpreadsheetApp.getActiveSpreadsheet()

    let rawDataInput = spreadsheet.getSheetByName(rawDataSheet)
    let rulesInput = spreadsheet.getSheetByName(rulesSheet)
    let output = spreadsheet.getSheetByName(outputSheet)
    
    let rawData = rawDataInput.getDataRange().getValues().slice(1)
    let rules = rulesInput.getDataRange().getValues()

    // do all the calculations n formatting
    rawData = transposeNestedArray(rawData)
    recepientName = getName(rawData)
    data = cleanUpData(rawData)
    data = applyRules(data, rules)
    dataByCycle = aggregateData(data)
    outputString = createOutput(dataByCycle)

    // write to output sheet
    output.getRange(1, 2).setValue('Formatted Data for '.concat(recepientName).concat(':'))
    output.getRange(2, 2).setValue(outputString)

    console.log("Done Formatting!")
    return

  } catch (err) {
    Logger.log("Failed with error %s", err.message)
  }
}

function getName(rawData) {
  let firstName = ''
  let lastName = ''

  for (let column of rawData) {
    if (column[0] == 'contributor_first_name') {
      firstName = column[1]
    } else if (column[0] == 'contributor_last_name') {
      lastName = column[1]
    }
  }

  return firstName.concat(' ').concat(lastName)
}

function cleanUpData(rawData) {
  // get only necessary columns
  columnNames = ['committee_name', 'report_year', 'contribution_receipt_amount']
  data = []
  for (let column of rawData) {
    if (columnNames.includes(column[0])) {
      tempColumn = [...column]
      // dont add columns with empty data! (specifically duplicate committee name)
      if (tempColumn.slice(1).filter(n => n).length > 0)
        data.push(column)
    }
  }

  // convert to JSON array
  data = transposeNestedArray(data)
  let headers = data.shift()
  let jsonData = []
  for (const item of data) {
    jsonItem = {}
    for (let i = 0; i < headers.length; i++) {
      jsonItem[headers[i]] = item[i]
    }
    jsonData.push(jsonItem)
  }

  return jsonData
}

function getLastRowWithData(ss) {
  let vals = ss.getRange("A1:A").getValues()
  return vals.filter(String).length
}

function transposeNestedArray(array) {
  let output = array[0].map((_, colIndex) => array.map(row => row[colIndex]));
  return output
}

function applyRules(data, rules) {
  // apply remove list rule, special casing rule, and make title case if not
  // get rule lists
  let specialCaseList = transposeNestedArray(rules)[1].slice(2).filter(n => n)
  let removeList = transposeNestedArray(rules)[3].slice(2).filter(n => n)

  // convert all removeList names to uppercase
  removeList = removeList.map(name => name.toUpperCase())

  // Remove rows
  data = data.filter(function(row) {
    return !removeList.includes(row['committee_name'].toUpperCase())
  });

  // Update Casing with special cases
  data = data.map(function(row) {
    for (let specialName of specialCaseList) {
      if (row['committee_name'].toUpperCase() === specialName.toUpperCase()) {
        row['committee_name'] = specialName
        return row;
      }
    }
    row['committee_name'] = toTitleCase(row['committee_name'])
    return row;
  });

  return data
}

function toTitleCase(str) {
  return str.toLowerCase().split(' ').map(function (word) {
    return (word.charAt(0).toUpperCase() + word.slice(1));
  }).join(' ');
}

function aggregateData(data) {
  // create a dict of data by election cycle (every 2 years)
  let dataByCycle = {}
  for (let row of data) {
    if (row['report_year'] % 2 === 1){
      electionYear = parseInt(row['report_year']) + 1
    } else {
      electionYear = row['report_year'] 
    }

    if (electionYear in dataByCycle){
      if (row['committee_name'] in dataByCycle[electionYear]) {
        dataByCycle[electionYear][row['committee_name']] += row['contribution_receipt_amount']
      } else {
        dataByCycle[electionYear][row['committee_name']] = row['contribution_receipt_amount']
      }
    } else {
      dataByCycle[electionYear] = {}
      dataByCycle[electionYear][row['committee_name']] = row['contribution_receipt_amount']
    }
  }
  
  return dataByCycle
}

function createOutput(dataByCycle) {
  let outputString = ''
  let cycleYears = Object.keys(dataByCycle).sort().reverse()

  sortableData = []
  for (let cycle in dataByCycle) {
    for (let donor in dataByCycle[cycle]) {
      sortableData.push([cycle, donor, dataByCycle[cycle][donor]])
    }
  }

  for (let year of cycleYears) {
    yearData = sortableData.filter(dataRow => dataRow[0] == year)
    yearData = yearData.sort(function(a, b) {
      return b[2] - a[2];
    });

    // write to string
    outputString = outputString.concat(year).concat(' cycle: ')
    for (let record of yearData) {
      outputString = outputString.concat(record[1]).concat(' $').concat(record[2].toLocaleString("en-US")).concat('; ')
    }
    outputString = outputString.concat('\n\n')
  }

  return outputString
}







