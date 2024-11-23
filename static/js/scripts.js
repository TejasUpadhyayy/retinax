// scripts.js

// Function to load results from localStorage and display them in the table
function loadResults() {
    let results = JSON.parse(localStorage.getItem('resultsLog')) || [];
    const tableBody = document.querySelector('#results-table tbody');
    tableBody.innerHTML = '';

    results.forEach((result, index) => {
        const row = document.createElement('tr');

        const cellIndex = document.createElement('th');
        cellIndex.scope = 'row';
        cellIndex.textContent = index + 1;
        row.appendChild(cellIndex);

        const cellDrGrade = document.createElement('td');
        cellDrGrade.textContent = result.dr_grade;
        row.appendChild(cellDrGrade);

        const cellDmePresence = document.createElement('td');
        cellDmePresence.textContent = result.dme_presence;
        row.appendChild(cellDmePresence);

        const cellTimestamp = document.createElement('td');
        cellTimestamp.textContent = result.timestamp;
        row.appendChild(cellTimestamp);

        tableBody.appendChild(row);
    });
}

// Function to save the current result to localStorage
function saveResult(result) {
    let results = JSON.parse(localStorage.getItem('resultsLog')) || [];
    results.unshift(result); // Add the new result to the beginning
    localStorage.setItem('resultsLog', JSON.stringify(results));
}

// On page load
document.addEventListener('DOMContentLoaded', () => {
    // Check if currentResult is defined (only on result.html after a prediction)
    if (typeof currentResult !== 'undefined') {
        // Save the current result
        saveResult(currentResult);
    }
    // Load and display results
    loadResults();
});
