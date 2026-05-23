# Complete Blockchain-Based E-Voting System

A secure voting system with role-based authentication, OTP verification, and blockchain integration for transparent and tamper-proof voting.

## Features

- **Role-based Authentication**: Separate flows for Users and Admins
- **Dual OTP Verification**: Email and Phone OTP verification for enhanced security
- **User Registration**: Complete registration with email and phone verification
- **Admin Login**: Direct admin access with email OTP verification
- **Blockchain Integration**: Secure vote storage using Ethereum smart contracts
- **Double Voting Prevention**: System prevents users from voting more than once
- **Candidate Management**: Admin can add candidates with photos, names, and party affiliations
- **Voting Period Control**: Admin can set voting start/end dates
- **Result Management**: Admin can set result declaration date and custom messages

## System Architecture

### Frontend (Express.js)
- HTML/CSS/JavaScript for user interface
- Responsive design for all devices
- Role-based navigation

### Backend (FastAPI)
- RESTful API for authentication and voting operations
- MySQL database integration
- OTP management (email and SMS)
- JWT token-based authentication

### Blockchain (Ethereum)
- Smart contract for voting operations
- Transparent and tamper-proof vote storage
- Candidate management on blockchain
- Voting period control

## Setup Instructions

### 1. Database Setup

1. Ensure MySQL is installed and running
2. Create the database:
   ```sql
   CREATE DATABASE voter_db_copy;
   ```
3. Run the database update scripts:
   ```bash
   mysql -u your_username -p voter_db_copy < database_update.sql
   mysql -u your_username -p voter_db_copy < database_update_voting.sql
   ```

### 2. Environment Configuration

Create a `.env` file in the `Database_API` directory with the following variables:

```env
# Database Configuration
MYSQL_USER=root
MYSQL_PASSWORD=your_password_here
MYSQL_HOST=localhost
MYSQL_DB=voter_db_copy

# JWT Secret Key
SECRET_KEY=your_secret_key_here

# OTP Configuration
OTP_TTL_MINUTES=5
OTP_VERIFIED_TTL_MINUTES=10
OTP_MAX_ATTEMPTS=5
OTP_DEBUG=true

# Twilio SMS Configuration (optional)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number

# Email Configuration (for email OTP)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_email_app_password
```

### 3. Install Dependencies

```bash
# Install Node.js dependencies
npm install

# Install Python dependencies
cd Database_API
pip install -r requirements.txt
```

### 4. Blockchain Setup

1. Install Truffle globally:
   ```bash
   npm install -g truffle
   ```

2. Install Ganache for local blockchain development:
   ```bash
   npm install -g ganache
   ```

3. Start Ganache:
   ```bash
   ganache
   ```

4. Compile and deploy smart contracts:
   ```bash
   truffle compile
   truffle migrate
   ```

### 5. Initialize Database

```bash
python init_voting_db.py
```

### 6. Build Frontend

```bash
npm run build
```

## Running the Application

### Method 1: Using npm scripts

1. Start the frontend server:
   ```bash
   npm start
   ```

2. In a new terminal, start the backend API:
   ```bash
   cd Database_API
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

### Method 2: Manual start

1. Start the frontend server:
   ```bash
   node index.js
   ```

2. In a new terminal, start the backend API:
   ```bash
   cd Database_API
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

### Access the Application

Open your browser and navigate to `http://127.0.0.1:8080`

## User Flow

### Role Selection
- Users select between "User" or "Admin" roles
- **User**: Redirects to login/register choice page
- **Admin**: Redirects to admin login page

### User Flow
1. **New Users**: Can register with email and phone OTP verification
2. **Existing Users**: Can login with email + password + email OTP verification

### Admin Flow
1. **Admin Login**: Direct login with email + password + email OTP verification
2. **No Registration**: Admin credentials are manually stored in database

## API Endpoints

### Authentication
- `GET /login` - Login with email, password, and OTP verification
- `POST /register` - Register new user with dual OTP verification

### OTP Management
- `POST /otp/send` - Send OTP to email or phone
- `POST /otp/verify` - Verify OTP code
- `GET /otp/status` - Check OTP service status

### Voting API
- `GET /api/voting-dates` - Get current voting dates
- `POST /api/voting-dates` - Set voting dates (admin only)
- `GET /api/candidates` - Get all candidates
- `POST /api/candidates` - Add candidate (admin only)
- `DELETE /api/candidates/{id}` - Delete candidate (admin only)
- `POST /api/vote` - Cast vote for a candidate
- `GET /api/results` - Get election results

## Security Features

1. **Dual OTP Verification**: Both email and phone OTP required for registration
2. **Email OTP for Login**: Email OTP verification for all login attempts
3. **Phone OTP for Users**: Additional phone OTP for user logins
4. **JWT Tokens**: Secure token-based authentication
5. **Input Validation**: Comprehensive client and server-side validation
6. **OTP Expiration**: Time-limited OTP codes with attempt limits
7. **Blockchain Security**: Immutable vote storage on Ethereum
8. **Double Voting Prevention**: System prevents multiple votes per user

## Troubleshooting

### Common Issues

1. **Database Connection Error**: Check MySQL credentials in `.env`
2. **OTP Not Sending**: Verify Twilio/Email credentials
3. **Email OTP Issues**: Check SMTP settings and app passwords
4. **CORS Errors**: Ensure frontend and backend ports match
5. **Blockchain Connection**: Ensure Ganache is running on port 8545

### Development Mode

Set `OTP_DEBUG=true` in `.env` to see OTP codes in console logs for testing.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.