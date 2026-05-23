(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
// Main Application JavaScript for both Admin and User
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is logged in
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');
    
    if (!token) {
        // Redirect to login if not authenticated
        window.location.href = '/login.html';
        return;
    }
    
    // Handle navigation for user pages
    const votingLink = document.getElementById('votingLink');
    const resultLink = document.getElementById('resultLink');
    const logoutLink = document.getElementById('logoutLink');
    
    if (votingLink) {
        votingLink.addEventListener('click', function(e) {
            e.preventDefault();
            showSection('votingSection');
        });
    }
    
    if (resultLink) {
        resultLink.addEventListener('click', function(e) {
            e.preventDefault();
            showSection('resultSection');
            loadResults();
        });
    }
    
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e) {
            e.preventDefault();
            handleLogout();
        });
    }
    
    // Handle navigation for admin pages
    const candidatesLink = document.getElementById('candidatesLink');
    const datesLink = document.getElementById('datesLink');
    const resultsLink = document.getElementById('resultsLink');
    
    if (candidatesLink) {
        candidatesLink.addEventListener('click', function(e) {
            e.preventDefault();
            showSection('candidatesSection');
        });
    }
    
    if (datesLink) {
        datesLink.addEventListener('click', function(e) {
            e.preventDefault();
            showSection('datesSection');
        });
    }
    
    if (resultsLink) {
        resultsLink.addEventListener('click', function(e) {
            e.preventDefault();
            showSection('resultsSection');
        });
    }
    
    // Handle form submissions
    const candidateForm = document.getElementById('candidateForm');
    if (candidateForm) {
        candidateForm.addEventListener('submit', function(e) {
            e.preventDefault();
            addCandidate();
        });
    }
    
    const datesForm = document.getElementById('datesForm');
    if (datesForm) {
        datesForm.addEventListener('submit', function(e) {
            e.preventDefault();
            setVotingDates();
        });
    }
    
    // Load initial data based on role
    if (role === 'admin') {
        loadAdminData();
    } else {
        loadVotingData();
    }
});

// Function to show a specific section and hide others
function showSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.classList.remove('active');
    });
    
    // Show the selected section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active');
    }
}

// Function to handle logout
function handleLogout() {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    window.location.href = '/login.html';
}

// Function to load voting data for users
async function loadVotingData() {
    try {
        // Load voting dates
        const datesResponse = await fetch('http://localhost:8000/api/voting-dates');
        if (datesResponse.ok) {
            const dates = await datesResponse.json();
            document.getElementById('votingPeriod').textContent = 
                `${new Date(dates.startDate).toLocaleString()} - ${new Date(dates.endDate).toLocaleString()}`;
        }
        
        // Load candidates
        const token = localStorage.getItem('token');
        const candidatesResponse = await fetch('/api/candidates', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (candidatesResponse.ok) {
            const candidates = await candidatesResponse.json();
            displayCandidates(candidates);
        }
    } catch (error) {
        console.error('Error loading voting data:', error);
    }
}

// Function to display candidates
function displayCandidates(candidates) {
    const container = document.getElementById('candidatesContainer');
    if (!container) return;
    
    if (candidates.length === 0) {
        container.innerHTML = '<p>No candidates available for voting.</p>';
        return;
    }
    
    let html = '<div class="candidate-grid">';
    candidates.forEach(candidate => {
        html += `
            <div class="candidate-card">
                <div class="candidate-photo">
                    ${candidate.photo ? `<img src="${candidate.photo}" alt="${candidate.name}">` : 'Photo'}
                </div>
                <div class="candidate-info">
                    <div class="candidate-name">${candidate.name}</div>
                    <div class="candidate-party">${candidate.party}</div>
                    <button class="vote-button" onclick="castVote(${candidate.id})">Vote</button>
                </div>
            </div>
        `;
    });
    html += '</div>';
    
    container.innerHTML = html;
}

// Function to cast a vote
async function castVote(candidateId) {
    const token = localStorage.getItem('token');
    
    try {
        const response = await fetch('/api/vote', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ candidateId })
        });
        
        if (response.ok) {
            alert('Your vote has been recorded successfully!');
            // Disable all vote buttons to prevent double voting
            document.querySelectorAll('.vote-button').forEach(button => {
                button.disabled = true;
                button.textContent = 'Voted';
            });
        } else if (response.status === 400) {
            const data = await response.json();
            alert(data.message || 'You have already voted.');
        } else {
            alert('Failed to cast vote. Please try again.');
        }
    } catch (error) {
        console.error('Error casting vote:', error);
        alert('Error casting vote. Please try again.');
    }
}

// Function to load results
async function loadResults() {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/api/user/results', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (response.ok) {
            const data = await response.json();
            displayResults(data);
        }
    } catch (error) {
        console.error('Error loading results:', error);
    }
}

// Function to display results
function displayResults(data) {
    const container = document.getElementById('resultContent');
    if (!container) return;
    
    const now = new Date();
    const resultDate = data.resultDate ? new Date(data.resultDate) : null;
    
    if (!resultDate || now < resultDate) {
        // Before result declaration date
        // Use the admin-defined message or default to "Results will be announced on (date)"
        const formattedDate = resultDate ? resultDate.toLocaleDateString('en-GB') : 'TBA';
        let message = data.resultMessage || `Results will be announced on ${formattedDate}.`;
        message = message.replace('{date}', formattedDate);
        
        container.innerHTML = `
            <div class="result-message">
                <p>${message}</p>
            </div>
        `;
    } else {
        // On or after result declaration date
        // Find winner from candidates
        if (data.candidates && data.candidates.length > 0) {
            const winner = data.candidates.reduce((prev, current) => {
                return (prev.vote_count || 0) > (current.vote_count || 0) ? prev : current;
            });
            
            container.innerHTML = `
                <div class="winner-card">
                    <div class="winner-title">Election Winner</div>
                    <div class="winner-photo">
                        ${winner.photo ? `<img src="${winner.photo}" alt="${winner.name}">` : 'Photo'}
                    </div>
                    <div class="winner-name">${winner.name}</div>
                    <div class="winner-party">${winner.party || 'N/A'}</div>
                    <div class="winner-votes">Votes: ${winner.vote_count || 0}</div>
                </div>
            `;
        } else {
            container.innerHTML = '<p>No results available yet.</p>';
        }
    }
}

// Admin functions
async function loadAdminData() {
    // Load existing candidates
    loadCandidates();
}

async function loadCandidates() {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/api/candidates', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (response.ok) {
            const candidates = await response.json();
            displayAdminCandidates(candidates);
        }
    } catch (error) {
        console.error('Error loading candidates:', error);
    }
}

function displayAdminCandidates(candidates) {
    const container = document.getElementById('candidatesContainer');
    if (!container) return;
    
    if (candidates.length === 0) {
        container.innerHTML = '<p>No candidates added yet.</p>';
        return;
    }
    
    let html = '';
    candidates.forEach(candidate => {
        html += `
            <div class="candidate-card">
                <div class="candidate-photo">
                    ${candidate.photo ? `<img src="${candidate.photo}" alt="${candidate.name}">` : 'Photo'}
                </div>
                <div class="candidate-info">
                    <div class="candidate-name">${candidate.name}</div>
                    <div class="candidate-party">${candidate.party}</div>
                </div>
                <div class="candidate-actions">
                    <button onclick="deleteCandidate(${candidate.id})">Delete</button>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

async function addCandidate() {
    const name = document.getElementById('candidateName').value;
    const party = document.getElementById('candidateParty').value;
    
    if (!name || !party) {
        alert('Please fill in all fields');
        return;
    }
    
    try {
        const response = await fetch('/api/candidates', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({ name, party })
        });
        
        if (response.ok) {
            const result = await response.json();
            if (result.blockchain_error) {
                alert(`Candidate added to database only!\nBlockchain error: ${result.blockchain_error}\n\nThe system is working in database-only mode.`);
            } else {
                alert('Candidate added successfully!');
            }
            document.getElementById('candidateForm').reset();
            loadCandidates();
        } else {
            alert('Failed to add candidate. Please try again.');
        }
    } catch (error) {
        console.error('Error adding candidate:', error);
        alert('Error adding candidate. Please try again.');
    }
}

async function deleteCandidate(candidateId) {
    if (!confirm('Are you sure you want to delete this candidate?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/candidates/${candidateId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        
        if (response.ok) {
            alert('Candidate deleted successfully!');
            loadCandidates();
        } else {
            alert('Failed to delete candidate. Please try again.');
        }
    } catch (error) {
        console.error('Error deleting candidate:', error);
        alert('Error deleting candidate. Please try again.');
    }
}

async function setVotingDates() {
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const resultDate = document.getElementById('resultDate').value;
    
    if (!startDate || !endDate || !resultDate) {
        alert('Please fill in all date fields');
        return;
    }
    
    // Validate dates
    const start = new Date(startDate);
    const end = new Date(endDate);
    const result = new Date(resultDate);
    
    if (end <= start) {
        alert('End date must be after start date');
        return;
    }
    
    if (result <= end) {
        alert('Result date must be after end date');
        return;
    }
    
    try {
        const response = await fetch('/api/voting-dates', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({ startDate, endDate, resultDate })
        });
        
        if (response.ok) {
            const result = await response.json();
            if (result.blockchain_error) {
                alert(`Voting dates set in database only!\nBlockchain error: ${result.blockchain_error}\n\nThe system is working in database-only mode.`);
            } else {
                alert('Voting dates set successfully!');
            }
        } else {
            alert('Failed to set voting dates. Please try again.');
        }
    } catch (error) {
        console.error('Error setting voting dates:', error);
        alert('Error setting voting dates. Please try again.');
    }
}
},{}]},{},[1]);
