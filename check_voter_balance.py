import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'Database_API'))

# Import the voting API to get access to web3
try:
    import voting_api
    from web3 import Web3
    
    # Check balance of the account we're using
    voter_account = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"
    print(f"Checking balance of voter account: {voter_account}")
    
    balance = voting_api.w3.eth.get_balance(voter_account)
    balance_eth = voting_api.w3.from_wei(balance, 'ether')
    print(f"Balance: {balance_eth} ETH")
    
    # Also check all accounts to see which ones have funds
    print("\nAll accounts and their balances:")
    accounts = voting_api.w3.eth.accounts
    for i, account in enumerate(accounts):
        balance = voting_api.w3.eth.get_balance(account)
        balance_eth = voting_api.w3.from_wei(balance, 'ether')
        print(f"Account {i}: {account} - Balance: {balance_eth} ETH")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()