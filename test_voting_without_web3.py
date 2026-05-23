import sys
import os

# Add the Database_API directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Database_API'))

def test_voting_without_web3():
    print("=== Testing Voting Without Web3 ===")
    
    try:
        # Try to import voting_api
        from Database_API.voting_api import vote, WEB3_AVAILABLE
        print(f"✅ voting_api imported successfully")
        print(f"WEB3_AVAILABLE: {WEB3_AVAILABLE}")
        
        # Test the vote function
        result = vote(1, "VOTER001")
        print(f"Vote function result: {result}")
        
        if result.get("success"):
            print("✅ Voting works in database-only mode")
        else:
            print("❌ Voting failed")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_voting_without_web3()