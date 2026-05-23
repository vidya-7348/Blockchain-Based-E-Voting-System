import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'Database_API'))

# Import web3
from web3 import Web3

# The private key you provided
private_key = "0x6741fd810d6de6df3a159308eb69e7a3a679241ce0fb4fda30e460a96c55d436"
print(f"Private key: {private_key}")

# Derive the account address from the private key
account = Web3().eth.account.from_key(private_key)
print(f"Derived account address: {account.address}")

# Target account
target_account = "0xF4eDE00BCD2C2b1CF5c18609875479be5c16E465"
print(f"Target account: {target_account}")

# Check if they match
if account.address.lower() == target_account.lower():
    print("✅ Private key matches the target account!")
else:
    print("❌ Private key does not match the target account")