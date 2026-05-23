// Blockchain interface for Node.js
// This file provides a wrapper to access blockchain functions from the Python backend

const { execSync } = require('child_process');
const path = require('path');

// Function to call Python blockchain functions
function callPythonFunction(functionName, args) {
    try {
        // Create a Python script to call the function
        const pythonScript = `
import sys
import json
sys.path.insert(0, '${path.join(__dirname).replace(/\\/g, '/')}')

try:
    from voting_api import ${functionName}
    result = ${functionName}(${args.map(arg => JSON.stringify(arg)).join(', ')})
    print(json.dumps(result))
except Exception as e:
    print(json.dumps({'error': str(e)}))
`;
        
        // Execute the Python script
        const result = execSync(`python -c "${pythonScript.replace(/"/g, '\\"')}"`, {
            cwd: __dirname,
            timeout: 10000 // 10 second timeout
        });
        
        // Parse the result
        const output = result.toString().trim();
        return JSON.parse(output);
    } catch (error) {
        console.log(`⚠️  Error calling Python function ${functionName}:`, error.message);
        return { error: `Failed to call ${functionName}: ${error.message}` };
    }
}

// Wrapper functions
function add_candidate(name, party, photo_hash = "", party_logo_hash = "") {
    console.log(`Adding candidate: ${name}, ${party}`);
    // Try to call the Python function
    const result = callPythonFunction('add_candidate', [name, party, photo_hash, party_logo_hash]);
    
    // If there's an error, return a more descriptive message
    if (result && result.error) {
        console.log(`Blockchain error: ${result.error}`);
        return { 
            error: "Blockchain not available - candidate stored in database only",
            database_only: true
        };
    }
    
    return result;
}

function set_voting_dates(startDate, endDate, resultDate) {
    console.log(`Setting voting dates: ${startDate}, ${endDate}, ${resultDate}`);
    // Convert dates to timestamps for Python
    const startTimestamp = Math.floor(new Date(startDate).getTime() / 1000);
    const endTimestamp = Math.floor(new Date(endDate).getTime() / 1000);
    const resultTimestamp = Math.floor(new Date(resultDate).getTime() / 1000);
    
    // Try to call the Python function
    const result = callPythonFunction('set_voting_dates', [new Date(startTimestamp * 1000), new Date(endTimestamp * 1000), new Date(resultTimestamp * 1000)]);
    
    // If there's an error, return a more descriptive message
    if (result && result.error) {
        console.log(`Blockchain error: ${result.error}`);
        return { 
            error: "Blockchain not available - dates stored in database only",
            database_only: true
        };
    }
    
    return result;
}

module.exports = {
    add_candidate,
    set_voting_dates
};