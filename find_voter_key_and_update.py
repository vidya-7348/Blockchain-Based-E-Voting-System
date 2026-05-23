import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'Database_API'))

# Import the voting API to get access to web3
try:
    import voting_api
    from web3 import Web3
    
    # Target account that we want to use (the one with funds)
    target_account = "0xF5611adFf7Db687EBC765043193B7d47BFa93ac4"
    print(f"Looking for private key for account: {target_account}")
    
    # Standard Ganache private keys
    ganache_private_keys = [
        "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80",  # Account 0
        "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d",  # Account 1
        "0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a",  # Account 2
        "0x7c852118294e51e653712a81e05800f419141751be58f605c371e15141b007a6",  # Account 3
        "0x47e179ec197488593b187f80a00eb0da91f1b9d0b13f8733639f19c30a34926a",  # Account 4
        "0x8b3a350cf5c34c9194ca85829a2df0ec3153be0318b5e2d3348e872092edffba",  # Account 5
        "0x92db14e403b83dfe3df233f83dfa3a0d7096f21ca9b0d6d6b8d88b2b4ec1564e",  # Account 6
        "0x4bbbf85ce3377467afe5d46f804f221813b2bb87f24d81f60f1fcdbf7cbf4356",  # Account 7
        "0xdbda1821b80551c9d65939329250298aa3472ba22feea921c0cf5d620ea67b97",  # Account 8
        "0x2a871d0798f97d79848a013d4936a73bf4cc922c825d33c1cf7073dff6d409c6"   # Account 9
    ]
    
    # Try each private key to see which one generates our target account
    for i, private_key in enumerate(ganache_private_keys):
        account = voting_api.w3.eth.account.from_key(private_key)
        if account.address.lower() == target_account.lower():
            print(f"✅ FOUND MATCHING PRIVATE KEY FOR ACCOUNT {i}:")
            print(f"Private key: {private_key}")
            
            # Update the .env file with this private key
            env_file_path = os.path.join(os.path.dirname(__file__), 'Database_API', '.env')
            with open(env_file_path, 'r') as f:
                lines = f.readlines()
            
            # Update the VOTER_PRIVATE_KEY line
            with open(env_file_path, 'w') as f:
                for line in lines:
                    if line.startswith('VOTER_PRIVATE_KEY='):
                        f.write(f'VOTER_PRIVATE_KEY={private_key}\n')
                    else:
                        f.write(line)
            
            print(f"✅ Updated .env file with correct private key for account with funds")
            break
    else:
        print("❌ No matching private key found in standard list")
        print("Let's try to find it by checking all accounts in Ganache...")
        
        # If not found in standard list, let's check if we can get it another way
        # For now, let's just update the voting API to use a fixed account
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()