#!/usr/bin/env python3
"""
Script to help set up the blockchain environment for the voting system.
This script will:
1. Check if Hardhat node is running
2. Deploy the contract if needed
3. Provide instructions for updating the .env file
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from web3 import Web3

def check_hardhat_node():
    """Check if Hardhat node is running"""
    try:
        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
        if w3.is_connected():
            print("✅ Hardhat node is running")
            return True
        else:
            print("❌ Hardhat node is not running")
            return False
    except Exception as e:
        print(f"❌ Error connecting to Hardhat node: {e}")
        return False

def deploy_contract():
    """Deploy the contract using Hardhat"""
    try:
        print("Deploying contract...")
        result = subprocess.run([
            'npx', 'hardhat', 'run', 'scripts/deploy.js', '--network', 'localhost'
        ], capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            print("✅ Contract deployed successfully")
            print(result.stdout)
            return True
        else:
            print("❌ Contract deployment failed")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error deploying contract: {e}")
        return False

def get_contract_address():
    """Try to get contract address from deployment output or build files"""
    try:
        # Try to read from build file
        build_path = Path('build/contracts/Voting.json')
        if build_path.exists():
            with open(build_path) as f:
                contract_data = json.load(f)
                networks = contract_data.get('networks', {})
                if networks:
                    network_id = list(networks.keys())[0]
                    network_info = networks[network_id]
                    address = network_info.get('address')
                    if address:
                        return address
    except Exception as e:
        print(f"Note: Could not read contract address from build file: {e}")
    return None

def get_accounts():
    """Get accounts from Hardhat node"""
    try:
        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
        if w3.is_connected():
            accounts = w3.eth.accounts
            return accounts
    except Exception as e:
        print(f"Note: Could not get accounts: {e}")
    return []

def main():
    print("=== Blockchain Setup Helper ===\n")
    
    # Check if Hardhat node is running
    if not check_hardhat_node():
        print("\nPlease start Hardhat node first:")
        print("  npx hardhat node")
        print("\nThen run this script again.")
        return
    
    # Get accounts
    accounts = get_accounts()
    if accounts:
        print(f"\nAvailable accounts ({len(accounts)}):")
        for i, account in enumerate(accounts):
            print(f"  {i+1}. {account}")
    else:
        print("\nNo accounts found. Make sure Hardhat node is running correctly.")
        return
    
    # Try to get existing contract address
    contract_address = get_contract_address()
    if contract_address:
        print(f"\nExisting contract found: {contract_address}")
        use_existing = input("\nDo you want to use the existing contract? (y/n): ")
        if use_existing.lower() != 'y':
            contract_address = None
    
    # Deploy contract if needed
    if not contract_address:
        print("\nDeploying contract...")
        if deploy_contract():
            contract_address = get_contract_address()
    
    if contract_address:
        print(f"\n✅ Contract is ready at address: {contract_address}")
        
        # Provide .env update instructions
        print("\n=== Update your .env file ===")
        print("Add the following lines to your .env file:")
        print(f"GANACHE_URL=http://127.0.0.1:8545")
        print(f"CONTRACT_ADDRESS={contract_address}")
        
        if accounts and len(accounts) > 0:
            print(f"ADMIN_PRIVATE_KEY= # Private key for {accounts[0]}")
        if accounts and len(accounts) > 1:
            print(f"VOTER_PRIVATE_KEY= # Private key for {accounts[1]}")
        
        print("\nTo get private keys, check the output when you started 'npx hardhat node'")
        print("Look for lines like: 'Private Key: 0x...'")
    else:
        print("\n❌ Could not get contract address. Please check the deployment.")

if __name__ == "__main__":
    main()