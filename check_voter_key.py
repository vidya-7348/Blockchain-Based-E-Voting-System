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

# The account being used in the error
used_account = "0xF5611adFf7Db687EBC765043193B7d47BFa93ac4"
print(f"Account being used: {used_account}")

# The account that matches the private key
expected_account = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"
print(f"Expected account (matches private key): {expected_account}")

print("\nMismatch detected!")
print(f"The system is trying to use account: {used_account}")
print(f"But the private key corresponds to: {expected_account}")