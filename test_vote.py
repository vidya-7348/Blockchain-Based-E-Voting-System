import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'Database_API'))

# Import the voting API
try:
    import voting_api
    
    print("=== Testing Vote Function ===")
    
    # Test voting for candidate 1 with voter ID "test_voter_001"
    result = voting_api.vote(1, "test_voter_001")
    print(f"Vote result: {result}")
    
    if "success" in result and result["success"]:
        print("✅ Vote cast successfully!")
        print(f"Transaction hash: {result.get('transaction_hash', 'N/A')}")
    else:
        print(f"❌ Vote failed: {result}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()