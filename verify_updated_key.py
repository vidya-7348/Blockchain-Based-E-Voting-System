import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'Database_API'))

# Import web3
from web3 import Web3

# The voter private key from .env
voter_private_key = "0x6741fd810d6de6df3a159308eb69e7a3a679241ce0fb4fda30e460a96c55d436"
print(f"Voter private key: {voter_private_key}")

# Derive the account address from the private key
account = Web3().eth.account.from_key(voter_private_key)
print(f"Derived voter account address: {account.address}")

# The account we want to use (the one with funds)
target_account = "0xF4eDE00BCD2C2b1CF5c18609875479be5c16E465"
print(f"Target account (with funds): {target_account}")

# Check if they match
if account.address.lower() == target_account.lower():
    print("✅ Private key matches the target account!")
else:
    print("❌ Private key does not match the target account")
    print(f"Private key corresponds to: {account.address}")