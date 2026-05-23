import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'Database_API'))

# Import the voting API
try:
    import voting_api
    
    print("=== Adding a Candidate ===")
    
    # Add a candidate
    result = voting_api.add_candidate("John Doe", "Democratic Party")
    print(f"Add candidate result: {result}")
    
    if "success" in result and result["success"]:
        print("✅ Candidate added successfully!")
        print(f"Transaction hash: {result.get('transaction_hash', 'N/A')}")
        print(f"Candidate ID: {result.get('candidate_id', 'N/A')}")
    else:
        print(f"❌ Failed to add candidate: {result}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()