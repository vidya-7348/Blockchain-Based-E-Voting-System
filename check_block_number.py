import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'Database_API'))

# Import the voting API to get access to web3
try:
    import voting_api
    
    print("=== Checking Current Block Number ===")
    
    # Get the current block number
    block_number = voting_api.w3.eth.block_number
    print(f"Current block number: {block_number}")
    
    # Get the latest block
    latest_block = voting_api.w3.eth.get_block('latest')
    print(f"Latest block hash: {latest_block.hash.hex()}")
    print(f"Latest block timestamp: {latest_block.timestamp}")
    print(f"Number of transactions in latest block: {len(latest_block.transactions)}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()