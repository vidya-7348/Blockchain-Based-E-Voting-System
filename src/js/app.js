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
            alert(data.detail || data.message || 'You have already voted.');
        } else if (response.status === 404) {
            alert('Voting endpoint not found. Please check server configuration.');
        } else {
            // Try to parse error response as JSON first
            const text = await response.text();
            try {
                const errorData = JSON.parse(text);
                alert(errorData.detail || errorData.message || `Voting failed with status ${response.status}`);
            } catch (parseError) {
                // If JSON parsing fails, use the raw text
                alert(text || `Voting failed with status ${response.status}: ${response.statusText}`);
            }
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
        // Display all candidates with vote counts
        if (data.candidates && data.candidates.length > 0) {
            // Filter out any candidates with invalid data
            const validCandidates = data.candidates.filter(candidate => 
                candidate && 
                typeof candidate.name === 'string' && 
                candidate.name.trim() !== ''
            );
            
            if (validCandidates.length === 0) {
                container.innerHTML = '<p>No valid candidates found.</p>';
                return;
            }
            
            // Sort candidates by vote count (descending)
            const sortedCandidates = [...validCandidates].sort((a, b) => {
                const aVotes = typeof a.vote_count === 'number' ? a.vote_count : 0;
                const bVotes = typeof b.vote_count === 'number' ? b.vote_count : 0;
                return bVotes - aVotes;
            });
            
            // Find winner (candidate with most votes)
            const winner = sortedCandidates[0];
            
            // Calculate total votes for percentage calculation
            const totalVotes = sortedCandidates.reduce((sum, candidate) => {
                const votes = typeof candidate.vote_count === 'number' ? candidate.vote_count : 0;
                return sum + votes;
            }, 0);
            
            // Calculate party vote totals
            const partyVotes = {};
            sortedCandidates.forEach(candidate => {
                // Safely get party name
                const party = (candidate.party && typeof candidate.party === 'string' && candidate.party.trim() !== '') 
                    ? candidate.party.trim() 
                    : 'Independent';
                // Safely get vote count
                const votes = typeof candidate.vote_count === 'number' ? candidate.vote_count : 0;
                if (!partyVotes[party]) {
                    partyVotes[party] = 0;
                }
                partyVotes[party] += votes;
            });
            
            // Find party with most votes
            let winningParty = '';
            let maxPartyVotes = 0;
            for (const [party, votes] of Object.entries(partyVotes)) {
                if (votes > maxPartyVotes) {
                    maxPartyVotes = votes;
                    winningParty = party;
                }
            }
            
            let resultsHtml = `
                <div class="results-container">
                    <h2>Election Results</h2>
                    <div class="candidates-results">
                        <div class="results-header">
                            <div class="candidate-info-header">Candidate</div>
                            <div class="party-header">Party</div>
                            <div class="votes-header">Votes</div>
                            <div class="percentage-header">Percentage</div>
                        </div>
                    `;
                    
                    sortedCandidates.forEach((candidate, index) => {
                        const isWinner = index === 0 && (typeof candidate.vote_count === 'number' ? candidate.vote_count : 0) > 0;
                        const votes = typeof candidate.vote_count === 'number' ? candidate.vote_count : 0;
                        const percentage = totalVotes > 0 ? ((votes / totalVotes) * 100).toFixed(1) : '0.0';
                        const rowClass = isWinner ? 'candidate-row winner' : 'candidate-row';
                        
                        // Safely get candidate name
                        const candidateName = (candidate.name && typeof candidate.name === 'string') 
                            ? candidate.name 
                            : 'Unknown Candidate';
                        
                        // Safely get party name
                        const partyName = (candidate.party && typeof candidate.party === 'string' && candidate.party.trim() !== '') 
                            ? candidate.party.trim() 
                            : 'Independent';
                        
                        resultsHtml += `
                            <div class="${rowClass}">
                                <div class="candidate-info">
                                    <span class="candidate-name">${candidateName}${isWinner ? ' 🏆' : ''}</span>
                                </div>
                                <div class="party">${partyName}</div>
                                <div class="votes">${votes}</div>
                                <div class="percentage">${percentage}%</div>
                            </div>
                        `;
                    });
                    
                    resultsHtml += `
                            </div>
                            <div class="results-summary">
                                <div class="summary-item">
                                    <div class="summary-value">${totalVotes}</div>
                                <div class="summary-label">Total Votes</div>
                                </div>
                                <div class="summary-item">
                                    <div class="summary-value">${sortedCandidates.length}</div>
                                    <div class="summary-label">Candidates</div>
                                </div>
                                <div class="summary-item">
                                    <div class="summary-value">${winner.name}</div>
                                    <div class="summary-label">Winner</div>
                                </div>
                                <div class="summary-item">
                                    <div class="summary-value">${winningParty}</div>
                                    <div class="summary-label">Winning Party</div>
                                </div>
                            </div>
                        </div>
                    `;
                    
                    container.innerHTML = resultsHtml;
                    
                    // Add CSS styles
                    const style = document.createElement('style');
                    style.innerHTML = `
                        .results-container {
                            background: #f8f9fa;
                            border-radius: 10px;
                            padding: 20px;
                            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                        }
                        
                        .results-header {
                            display: flex;
                            justify-content: space-between;
                            padding: 15px;
                            border-bottom: 2px solid #ddd;
                            background: #e9ecef;
                            font-weight: bold;
                        }
                        
                        .candidate-info-header, .candidate-info {
                            flex: 2;
                            text-align: left;
                        }
                        
                        .party-header, .party {
                            flex: 1;
                        }
                        
                        .votes-header, .votes {
                            flex: 1;
                            text-align: center;
                        }
                        
                        .percentage-header, .percentage {
                            flex: 1;
                            text-align: center;
                        }
                        
                        .candidate-row {
                            display: flex;
                            justify-content: space-between;
                            padding: 15px;
                            border-bottom: 1px solid #eee;
                            background: white;
                        }
                        
                        .candidate-row.winner {
                            font-weight: 700;
                            background: #d4edda;
                            border-left: 4px solid #28a745;
                        }
                        
                        .candidate-name {
                            font-weight: 500;
                        }
                        
                        .results-summary {
                            display: flex;
                            justify-content: space-around;
                            margin-top: 20px;
                            padding: 15px;
                            background: #e9ecef;
                            border-radius: 5px;
                        }
                        
                        .summary-item {
                            text-align: center;
                        }
                        
                        .summary-value {
                            font-size: 24px;
                            font-weight: bold;
                        }
                        
                        .summary-label {
                            font-size: 14px;
                            color: #6c757d;
                        }
                    `;
                    document.head.appendChild(style);
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