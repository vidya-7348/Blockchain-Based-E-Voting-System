# Complete Setup Instructions for Blockchain-Based E-Voting System

## Prerequisites
1. Node.js and npm installed
2. Python 3.7+ installed
3. MySQL database installed and running
4. Ganache (for local blockchain) or Infura account (for testnet)
5. Truffle installed globally: `npm install -g truffle`

## Step 1: Database Setup

1. Create MySQL database:
```sql
CREATE DATABASE voter_db_copy;
```

2. Initialize database tables:
```bash
cd Database_API
python init_voting_db.py
python init_candidates_table.py
```

## Step 2: Environment Configuration

Create `.env` file in `Database_API` folder:

```env
# Database Configuration
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_DB=voter_db_copy

# JWT Secret Key (generate a random string)
SECRET_KEY=your_random_secret_key_minimum_32_characters_long

# OTP Configuration
OTP_TTL_MINUTES=5
OTP_VERIFIED_TTL_MINUTES=10
OTP_MAX_ATTEMPTS=5
OTP_DEBUG=true

# Email Configuration (optional - for OTP)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# Twilio SMS Configuration (optional - for OTP)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_phone_number

# Blockchain Configuration (optional - if using Ganache)
GANACHE_URL=http://127.0.0.1:8545
ADMIN_PRIVATE_KEY=your_ganache_admin_private_key
VOTER_PRIVATE_KEY=your_ganache_voter_private_key
```

## Step 3: Blockchain Setup

### Option A: Using Ganache (Recommended for Development)

1. Install Ganache:
```bash
npm install -g ganache
```

2. Start Ganache:
```bash
ganache
```
This starts a local blockchain on port 8545.

3. Deploy smart contracts:
```bash
truffle migrate
```

4. Copy the contract address:
   - After migration, check the output or run:
   ```bash
   python get_contract_address.py
   ```
   - The contract address is automatically loaded from `build/contracts/Voting.json`

### Option B: Using Testnet (Production-like)

1. Update `truffle-config.js` with your testnet configuration
2. Run: `truffle migrate --network testnet`
3. Update contract address in `.env` file

## Step 4: Install Dependencies

```bash
# Install Node.js dependencies
npm install

# Install Python dependencies
cd Database_API
pip install -r requirements.txt
```

## Step 5: Initialize System

1. Run database initialization:
```bash
cd Database_API
python init_voting_db.py
python init_candidates_table.py
```

2. Verify contract address is loaded:
```bash
cd ..
python get_contract_address.py
```

## Step 6: Start the System

### Method 1: Using Start Script (Recommended)

```bash
python start_system.py
```

### Method 2: Manual Start (3 Terminals)

**Terminal 1 - Frontend Server:**
```bash
node index.js
```

**Terminal 2 - Backend API:**
```bash
cd Database_API
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 3 - Blockchain (if using Ganache):**
```bash
ganache
```

**Terminal 4 - Deploy Contracts (one time):**
```bash
truffle migrate
```

## Step 7: Access the Application

- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Images**: http://localhost:8080/images/...

## Important Notes

1. **Contract Address**: The contract address is automatically loaded from the build file. No manual configuration needed.

2. **JavaScript in Terminal**: Never run JavaScript code directly in PowerShell/terminal. JavaScript code runs in Node.js (`node index.js`) or in the browser.

3. **Blockchain Connection**: 
   - If blockchain is not available, the system will work with database storage
   - Candidates can still be added via admin panel
   - Files are always saved to disk

4. **Image Serving**: Images are served through the Node.js proxy to the backend.

5. **Token Authentication**: Tokens are stored in localStorage and automatically extracted from URL parameters.

## Troubleshooting

### Contract Address Not Found
- Run `truffle migrate` to deploy contracts
- Check `build/contracts/Voting.json` exists
- Verify Ganache is running on port 8545

### Images Not Loading
- Check that `/images` proxy is configured in `index.js`
- Verify uploads directory exists: `uploads/candidates/` and `uploads/parties/`
- Check browser console for 404 errors

### Candidates Not Showing
- Check backend logs for errors
- Verify database has candidates table: `python init_candidates_table.py`
- Check blockchain connection if using blockchain storage

### Authentication Errors
- Verify SECRET_KEY is set in `.env`
- Check token is being sent in request headers
- Clear browser localStorage and re-login

## File Structure

```
project/
├── contracts/          # Solidity smart contracts
├── build/             # Compiled contracts (generated)
├── src/
│   ├── html/         # HTML pages
│   ├── js/           # JavaScript files
│   └── css/          # Stylesheets
├── Database_API/     # Python FastAPI backend
│   ├── main.py       # Main API server
│   ├── voting_api.py # Blockchain interaction
│   └── .env          # Environment variables
├── uploads/          # Uploaded images (generated)
│   ├── candidates/   # Candidate photos
│   └── parties/      # Party logos
├── index.js          # Node.js frontend server
└── get_contract_address.py  # Utility script
```

## Admin Account Setup

Admin accounts must be manually added to the database:

```sql
INSERT INTO users (firstName, lastName, emailid, password, role)
VALUES ('Admin', 'User', 'admin@example.com', 'admin_password', 'admin');
```

Then login with email and password + OTP verification.

## How to Fix Blockchain Connection Issues

If you're seeing the message "Blockchain: Contract or admin account not configured", follow these steps:

### Step 1: Start Local Blockchain Network

In a new terminal, start a local Hardhat network:
```bash
cd "voting mainfullmainnn (2)/voting mainfullmainnn/voting mainfull/voting main01/Decentralized-Voting-System-main"
npx hardhat node
```

This will start a local Ethereum network on http://127.0.0.1:8545 and display a list of accounts with their private keys.

### Step 2: Deploy Smart Contract

In another terminal, deploy the contract to the local network:
```bash
cd "voting mainfullmainnn (2)/voting mainfullmainnn/voting mainfull/voting main01/Decentralized-Voting-System-main"
npx hardhat run scripts/deploy.js --network localhost
```

Note the contract address that gets displayed after successful deployment.

### Step 3: Update Environment Variables

Add the following lines to your `.env` file:
```env
GANACHE_URL=http://127.0.0.1:8545
ADMIN_PRIVATE_KEY=YOUR_ADMIN_PRIVATE_KEY_HERE
VOTER_PRIVATE_KEY=YOUR_VOTER_PRIVATE_KEY_HERE
```

Replace `YOUR_ADMIN_PRIVATE_KEY_HERE` with the private key of the first account shown by Hardhat node.
Replace `YOUR_VOTER_PRIVATE_KEY_HERE` with the private key of the second account shown by Hardhat node.

Also add this line with the contract address you got from deployment:
```env
CONTRACT_ADDRESS=YOUR_DEPLOYED_CONTRACT_ADDRESS_HERE
```

### Step 4: Restart the Application

Stop and restart your application:
```bash
# Stop the current server (Ctrl+C)
# Then start it again
npm start
```

