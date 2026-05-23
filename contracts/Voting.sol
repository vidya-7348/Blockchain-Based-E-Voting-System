pragma solidity >=0.5.0 <0.9.0;

contract Voting {
    // Structs
    struct Candidate {
        uint id;
        string name;
        string party;
        string photoHash; // IPFS hash for candidate photo
        string partyLogoHash; // IPFS hash for party logo
        uint voteCount;
    }
    
    struct Voter {
        bool hasVoted;
        uint candidateId;
        string voterId; // Link to database voter ID
    }
    
    struct ElectionDates {
        uint256 startDate;
        uint256 endDate;
        uint256 resultDate;
    }
    
    // State variables
    address public owner;
    uint public countCandidates;
    ElectionDates public electionDates;
    
    // Mappings
    mapping(uint => Candidate) public candidates;
    mapping(address => Voter) public voters;
    mapping(string => bool) public voterIds; // Track if voter ID has voted
    
    // Events
    event CandidateAdded(uint indexed candidateId, string name, string party);
    event CandidateUpdated(uint indexed candidateId, string name, string party);
    event Voted(address indexed voter, uint indexed candidateId);
    event DatesUpdated(uint256 startDate, uint256 endDate, uint256 resultDate);
    
    // Modifiers
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }
    
    modifier onlyDuringVotingPeriod() {
        require(block.timestamp >= electionDates.startDate, "Voting has not started yet");
        require(block.timestamp <= electionDates.endDate, "Voting period has ended");
        _;
    }
    
    modifier onlyAfterResultDate() {
        require(block.timestamp >= electionDates.resultDate, "Results not available yet");
        _;
    }
    
    // Constructor
    constructor() {
        owner = msg.sender;
        electionDates.startDate = block.timestamp;
        electionDates.endDate = block.timestamp + 30 days;
        electionDates.resultDate = block.timestamp + 35 days;
    }
    
    // Functions
    
    // Add a candidate
    function addCandidate(string memory _name, string memory _party, string memory _photoHash, string memory _partyLogoHash) public onlyOwner returns(uint) {
        countCandidates++;
        candidates[countCandidates] = Candidate(countCandidates, _name, _party, _photoHash, _partyLogoHash, 0);
        emit CandidateAdded(countCandidates, _name, _party);
        return countCandidates;
    }
    
    // Update a candidate
    function updateCandidate(uint _candidateId, string memory _name, string memory _party, string memory _photoHash, string memory _partyLogoHash) public onlyOwner {
        require(_candidateId > 0 && _candidateId <= countCandidates, "Invalid candidate ID");
        candidates[_candidateId].name = _name;
        candidates[_candidateId].party = _party;
        candidates[_candidateId].photoHash = _photoHash;
        candidates[_candidateId].partyLogoHash = _partyLogoHash;
        emit CandidateUpdated(_candidateId, _name, _party);
    }
    
    // Vote for a candidate
    function vote(uint _candidateId, string memory _voterId) public onlyDuringVotingPeriod {
        // Check if candidate exists
        require(_candidateId > 0 && _candidateId <= countCandidates, "Invalid candidate ID");
        
        // Check if voter has already voted with this voter ID
        require(!voterIds[_voterId], "This voter ID has already voted");
        
        // Check if voter address has already voted
        require(!voters[msg.sender].hasVoted, "This address has already voted");
        
        // Record the vote
        voters[msg.sender] = Voter(true, _candidateId, _voterId);
        voterIds[_voterId] = true;
        candidates[_candidateId].voteCount++;
        
        emit Voted(msg.sender, _candidateId);
    }
    
    // Check if voter has voted
    function hasVoted(address _voter) public view returns(bool) {
        return voters[_voter].hasVoted;
    }
    
    // Check if voter ID has voted
    function hasVoterIdVoted(string memory _voterId) public view returns(bool) {
        return voterIds[_voterId];
    }
    
    // Get candidate details
    function getCandidate(uint _candidateId) public view returns (uint, string memory, string memory, string memory, string memory, uint) {
        require(_candidateId > 0 && _candidateId <= countCandidates, "Invalid candidate ID");
        Candidate memory candidate = candidates[_candidateId];
        return (candidate.id, candidate.name, candidate.party, candidate.photoHash, candidate.partyLogoHash, candidate.voteCount);
    }
    
    // Get all candidates
    function getAllCandidates() public view returns (Candidate[] memory) {
        Candidate[] memory allCandidates = new Candidate[](countCandidates);
        for (uint i = 1; i <= countCandidates; i++) {
            allCandidates[i-1] = candidates[i];
        }
        return allCandidates;
    }
    
    // Get candidate vote count
    function getCandidateVoteCount(uint _candidateId) public view returns (uint) {
        require(_candidateId > 0 && _candidateId <= countCandidates, "Invalid candidate ID");
        return candidates[_candidateId].voteCount;
    }
    
    // Get total votes cast
    function getTotalVotes() public view returns (uint) {
        uint totalVotes = 0;
        for (uint i = 1; i <= countCandidates; i++) {
            totalVotes += candidates[i].voteCount;
        }
        return totalVotes;
    }
    
    // Set election dates
    function setElectionDates(uint256 _startDate, uint256 _endDate, uint256 _resultDate) public onlyOwner {
        require(_endDate > _startDate, "End date must be after start date");
        require(_resultDate >= _endDate, "Result date must be after end date");
        
        electionDates.startDate = _startDate;
        electionDates.endDate = _endDate;
        electionDates.resultDate = _resultDate;
        
        emit DatesUpdated(_startDate, _endDate, _resultDate);
    }
    
    // Get election dates
    function getElectionDates() public view returns (uint256, uint256, uint256) {
        return (electionDates.startDate, electionDates.endDate, electionDates.resultDate);
    }
    
    // Get winning candidate
    function getWinner() public view onlyAfterResultDate returns (uint, string memory, string memory, string memory, string memory, uint) {
        require(countCandidates > 0, "No candidates available");
        
        uint winningCandidateId = 1;
        uint maxVotes = candidates[1].voteCount;
        
        for (uint i = 2; i <= countCandidates; i++) {
            if (candidates[i].voteCount > maxVotes) {
                maxVotes = candidates[i].voteCount;
                winningCandidateId = i;
            }
        }
        
        Candidate memory winner = candidates[winningCandidateId];
        return (winner.id, winner.name, winner.party, winner.photoHash, winner.partyLogoHash, winner.voteCount);
    }
    
    // Get all candidates with vote counts (for results)
    function getResults() public view onlyAfterResultDate returns (Candidate[] memory) {
        return getAllCandidates();
    }
}