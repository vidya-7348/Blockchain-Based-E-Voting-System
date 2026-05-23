import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'Database_API'))

# Import web3
from web3 import Web3

# The voter private key from .env
voter_private_key = "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d"
print(f"Voter private key: {voter_private_key}")

# Derive the account address from the private key
account = Web3().eth.account.from_key(voter_private_key)
print(f"Derived voter account address: {account.address}")

# The account we want to use (the one with funds)
target_account = "0xF5611adFf7Db687EBC765043193B7d47BFa93ac4"
print(f"Target account (with funds): {target_account}")

# Check if they match
if account.address.lower() == target_account.lower():
    print("✅ Private key matches the target account!")
else:
    print("❌ Private key does not match the target account")
    print(f"Private key corresponds to: {account.address}")