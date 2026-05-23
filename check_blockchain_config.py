#!/usr/bin/env python3
"""
Script to check blockchain configuration for the voting system.
This script will:
1. Check if Hardhat node is running
2. Verify contract address is configured
3. Check if admin account is configured
4. Test basic blockchain connectivity
"""

import os
import sys
from pathlib import Path

# Add the Database_API directory to the path
sys.path.insert(0, str(Path(__file__).joinpath('Database_API')))

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_path = Path(__file__).parent / '.env'
    if not env_path.exists():
        print("❌ .env file not found")
        return False
    
    required_vars = ['GANACHE_URL', 'CONTRACT_ADDRESS', 'ADMIN_PRIVATE_KEY']
    found_vars = []
    
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key = line.split('=')[0]
                if key in required_vars:
                    found_vars.append(key)
    
    missing_vars = [var for var in required_vars if var not in found_vars]
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ All required environment variables found")
        return True

def check_blockchain_connection():
    """Check if we can connect to the blockchain"""
    try:
        from web3 import Web3
        from dotenv import load_dotenv
        
        # Load environment variables
        load_dotenv()
        
        ganache_url = os.environ.get('GANACHE_URL', 'http://127.0.0.1:8545')
        w3 = Web3(Web3.HTTPProvider(ganache_url))
        
        if w3.is_connected():
            print(f"✅ Connected to blockchain at {ganache_url}")
            try:
                chain_id = w3.eth.chain_id
                block_number = w3.eth.block_number
                print(f"   Chain ID: {chain_id}, Latest block: {block_number}")
                
                # Check if we have accounts
                accounts = w3.eth.accounts
                if accounts:
                    print(f"   Available accounts: {len(accounts)}")
                else:
                    print("   No accounts available")
                    
                return True
            except Exception as e:
                print(f"⚠️  Connected but error getting chain info: {e}")
                return True
        else:
            print(f"❌ Not connected to blockchain at {ganache_url}")
            return False
    except Exception as e:
        print(f"❌ Error connecting to blockchain: {e}")
        return False

def check_contract_address():
    """Check if contract address is configured"""
    try:
        from dotenv import load_dotenv
        
        # Load environment variables
        load_dotenv()
        
        contract_address = os.environ.get('CONTRACT_ADDRESS')
        if contract_address:
            print(f"✅ Contract address configured: {contract_address}")
            return True
        else:
            print("❌ Contract address not configured")
            return False
    except Exception as e:
        print(f"❌ Error checking contract address: {e}")
        return False

def check_admin_account():
    """Check if admin account is configured"""
    try:
        from dotenv import load_dotenv
        
        # Load environment variables
        load_dotenv()
        
        admin_private_key = os.environ.get('ADMIN_PRIVATE_KEY')
        if admin_private_key:
            print("✅ Admin private key configured")
            return True
        else:
            print("❌ Admin private key not configured")
            return False
    except Exception as e:
        print(f"❌ Error checking admin account: {e}")
        return False

def main():
    print("=== Blockchain Configuration Check ===\n")
    
    # Check .env file
    print("1. Checking .env file...")
    env_ok = check_env_file()
    
    # Check blockchain connection
    print("\n2. Checking blockchain connection...")
    blockchain_ok = check_blockchain_connection()
    
    # Check contract address
    print("\n3. Checking contract address...")
    contract_ok = check_contract_address()
    
    # Check admin account
    print("\n4. Checking admin account...")
    admin_ok = check_admin_account()
    
    print("\n=== Summary ===")
    if env_ok and blockchain_ok and contract_ok and admin_ok:
        print("✅ All blockchain configurations are correct!")
        print("The system should work with full blockchain functionality.")
    else:
        print("⚠️  Some blockchain configurations are missing or incorrect.")
        print("The system will work in database-only mode.")
        print("To enable blockchain functionality, run 'python setup_blockchain.py'")

if __name__ == "__main__":
    main()