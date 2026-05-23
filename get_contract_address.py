#!/usr/bin/env python3
"""Extract contract address from build file and update configuration"""
import json
from pathlib import Path

def get_contract_address():
    """Extract contract address from build file"""
    build_path = Path(__file__).parent / 'build' / 'contracts' / 'Voting.json'
    
    if not build_path.exists():
        print("Error: Voting.json build file not found")
        return None
    
    try:
        with open(build_path, 'r') as f:
            contract_data = json.load(f)
        
        networks = contract_data.get('networks', {})
        
        if not networks:
            print("Warning: No networks found in build file. Contract may not be deployed.")
            return None
        
        # Get the first network (usually development network)
        network_id = list(networks.keys())[0]
        network_info = networks[network_id]
        address = network_info.get('address')
        
        if address:
            print(f"Contract deployed on network {network_id}")
            print(f"Contract address: {address}")
            return address
        else:
            print("Warning: Contract address not found in network info")
            return None
            
    except Exception as e:
        print(f"Error reading contract file: {e}")
        return None

if __name__ == "__main__":
    address = get_contract_address()
    if address:
        print(f"\nContract Address: {address}")
    else:
        print("\nNo contract address found. Please deploy the contract first using: truffle migrate")


