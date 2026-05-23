import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'Database_API'))

# Import the voting API
try:
    import voting_api
    
    print("=== Admin Account Status ===")
    print(f"Admin account: {voting_api.admin_account}")
    print(f"Admin private key available: {bool(voting_api.admin_private_key)}")
    
    if voting_api.admin_account:
        # Check balance
        balance = voting_api.w3.eth.get_balance(voting_api.admin_account)
        balance_eth = voting_api.w3.from_wei(balance, 'ether')
        print(f"Admin account balance: {balance_eth} ETH")
    
    print("\n=== Contract Status ===")
    print(f"Contract address: {voting_api.contract_address}")
    print(f"Contract instance available: {voting_api.contract is not None}")
    
    if voting_api.contract is not None:
        print("✅ Contract is properly initialized")
    else:
        print("❌ Contract is not initialized")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()