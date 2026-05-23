import json
import os
from web3 import Web3
from eth_account import Account

# Connect to the local blockchain
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

if not w3.is_connected():
    print("❌ Could not connect to blockchain")
    exit(1)

print(f"✅ Connected to blockchain at http://127.0.0.1:8545")
print(f"   Chain ID: {w3.eth.chain_id}, Latest block: {w3.eth.block_number}")

# Load contract ABI and bytecode
contract_path = os.path.join(os.path.dirname(__file__), '..', 'build', 'contracts', 'Voting.json')
with open(contract_path) as f:
    contract_data = json.load(f)

abi = contract_data['abi']
bytecode = contract_data['bytecode']

# Get the first account as deployer
deployer_account = w3.eth.accounts[0]
deployer_private_key = '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80'  # First account private key

print(f"✅ Using account {deployer_account} as deployer")

# Create contract instance
Voting = w3.eth.contract(abi=abi, bytecode=bytecode)

# Build transaction
transaction = Voting.constructor().build_transaction({
    'from': deployer_account,
    'gas': 4000000,  # Increased gas limit
    'gasPrice': w3.to_wei('40', 'gwei'),
    'nonce': w3.eth.get_transaction_count(deployer_account),
})

# Sign transaction
signed_txn = w3.eth.account.sign_transaction(transaction, deployer_private_key)

# Send transaction
try:
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print(f"✅ Transaction sent: {tx_hash.hex()}")
    
    # Wait for transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = tx_receipt['contractAddress']
    
    print(f"✅ Contract deployed at address: {contract_address}")
    
    # Update the .env file with the new contract address
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    with open(env_path, 'r') as f:
        env_content = f.read()
    
    # Replace the contract address in the .env file
    lines = env_content.split('\n')
    with open(env_path, 'w') as f:
        for line in lines:
            if line.startswith('CONTRACT_ADDRESS='):
                f.write(f'CONTRACT_ADDRESS={contract_address}\n')
            else:
                f.write(line + '\n')
    
    print(f"✅ Updated .env file with new contract address")
    
except Exception as e:
    print(f"❌ Error deploying contract: {e}")