# Blockchain-Based E-Voting System

This is a complete blockchain-based voting system with a clear role-based flow. The system integrates FastAPI backend, MySQL database, React/HTML frontend, and Hardhat Solidity smart contract for secure vote storage.

## Features

- **Role-Based Flow**: Role selection page with User and Admin options
- **User Registration**: Collects name, email, mobile number, Aadhaar/ID, and password
- **Secure Authentication**: JWT tokens with OTP verification
- **Blockchain Integration**: Hardhat + Solidity smart contract for vote storage
- **Voting**: One vote per user, recorded on blockchain
- **Admin Dashboard**: Add candidates, manage election, view users, live vote counts
- **Responsive Design**: Works on all device sizes

## Prerequisites

- Node.js (v14 or higher)
- Python (v3.8 or higher)
- MySQL database
- Ganache (for local blockchain development)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Decentralized-Voting-System
```

2. Install frontend dependencies:
```bash
npm install
```

3. Install backend dependencies:
```bash
cd Database_API
pip install -r requirements.txt
```

4. Set up environment variables:
- Copy `.env.example` to `.env` and fill in the required values

5. Set up the database:
- Create a MySQL database
- Update the database configuration in `.env`
- Run the database initialization script

## Running the Complete System

The easiest way to run the complete system is to use the provided start script:

```bash
python start_system.py
```

This script will:
1. Initialize the database
2. Build the frontend
3. Start the backend API server on port 8000
4. Start the frontend server on port 8080

## Manual Setup (Alternative)

If you prefer to run the components manually:

### Step 1: Start Local Blockchain Network

In a new terminal, start a local Hardhat network:
```bash
npx hardhat node
```

This will start a local Ethereum network on http://127.0.0.1:8545 and display a list of accounts with their private keys.

### Step 2: Deploy Smart Contract

In another terminal, deploy the contract to the local network:
```bash
npx hardhat run scripts/deploy.js --network localhost
```

Note the contract address that gets displayed after successful deployment.

### Step 3: Update Environment Variables

Add the following lines to your `.env` file:
```env
GANACHE_URL=http://127.0.0.1:8545
CONTRACT_ADDRESS=YOUR_DEPLOYED_CONTRACT_ADDRESS_HERE
ADMIN_PRIVATE_KEY=YOUR_ADMIN_PRIVATE_KEY_HERE
VOTER_PRIVATE_KEY=YOUR_VOTER_PRIVATE_KEY_HERE
```

Replace:
- `YOUR_DEPLOYED_CONTRACT_ADDRESS_HERE` with the contract address from deployment
- `YOUR_ADMIN_PRIVATE_KEY_HERE` with the private key of the first account shown by Hardhat node
- `YOUR_VOTER_PRIVATE_KEY_HERE` with the private key of the second account shown by Hardhat node

### Step 4: Start the Application

```bash
npm start
```

The application will be available at http://localhost:8080

## Troubleshooting Blockchain Connection Issues

If you see the message "Blockchain: Contract or admin account not configured", it means the system couldn't connect to the blockchain or find the deployed contract. 

To fix this:

1. Make sure you've started the Hardhat node with `npx hardhat node`
2. Deploy the contract with `npx hardhat run scripts/deploy.js --network localhost`
3. Update your `.env` file with the contract address and private keys
4. Restart the application

Alternatively, you can run the setup helper script:
```bash
python setup_blockchain.py
```

The system will work in database-only mode if blockchain is not configured, but for full functionality, the blockchain connection is recommended.

## System Architecture

### Frontend (React/HTML)
- Role selection page with proper redirection logic
- Simplified registration form with required fields only
- Voting page with candidate list from blockchain
- Admin dashboard with all required functionality
- Proper JWT token handling across all pages

### Backend (FastAPI)
- RESTful API endpoints for all system functionality
- MySQL database integration for user management
- Blockchain integration using Web3.py
- JWT authentication and authorization
- OTP generation and verification

### Database (MySQL)
- User table with all required fields
- Voting dates table for election scheduling
- Candidates table for caching blockchain data
- Proper indexing for performance

### Blockchain (Solidity + Hardhat)
- Voting smart contract with candidate management
- Secure vote recording with duplicate prevention
- Election date management
- Real-time vote counting
- Winner determination

## Smart Contract Functions

The smart contract includes functions for:

- Adding candidates
- Updating candidates
- Voting for candidates
- Getting vote counts
- Setting election dates
- Declaring winners
- Checking voting status

## Security Features

- JWT token-based authentication
- OTP verification for login and registration
- Role-based access control
- Blockchain-based vote storage for immutability
- Prevention of multiple voting attempts
- Secure password handling

## API Endpoints

- `/login` - User/Admin login with OTP verification
- `/register` - User registration with OTP verification
- `/api/candidates` - Get/add/update/delete candidates
- `/api/vote` - Cast vote on blockchain
- `/api/results` - Get live election results
- `/api/voting-dates` - Manage election dates
- `/otp/send` - Send OTP via email/SMS
- `/otp/verify` - Verify OTP

## Usage

1. Register as a new user or login as admin (default admin credentials in database)
2. Admin can:
   - Add/remove candidates
   - Set voting dates
   - View results
3. Users can:
   - View candidates
   - Cast votes
   - View results after voting period ends

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- OTP verification for login
- Role-based access control
- SQL injection prevention
- Blockchain immutability for voting records

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Node.js, Express.js
- **Database**: MySQL
- **Blockchain**: Ethereum, Solidity, Web3.js
- **Authentication**: JWT, bcrypt
- **Development Tools**: Hardhat, Truffle

## Smart Contracts

The system uses a Voting.sol smart contract that handles:
- Candidate management
- Voting period management
- Vote casting and counting
- Winner determination

## API Endpoints

- `POST /api/register` - User registration
- `POST /api/login` - User login with OTP
- `GET /api/candidates` - Get all candidates
- `POST /api/candidates` - Add candidate (admin only)
- `DELETE /api/candidates/:id` - Delete candidate (admin only)
- `GET /api/voting-dates` - Get voting dates
- `POST /api/voting-dates` - Set voting dates (admin only)
- `POST /api/vote` - Cast vote (user only)
- `GET /api/results` - Get voting results

## License

This project is licensed under the MIT License.