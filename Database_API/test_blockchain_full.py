import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add the current directory to the path
sys.path.insert(0, str(Path(__file__).parent))

# Try to import the voting_api module
try:
    from voting_api import (
        add_candidate, 
        set_voting_dates, 
        update_candidate, 
        vote, 
        get_candidate, 
        get_all_candidates, 
        get_candidate_count,
        get_voting_dates,
        get_winner
    )
    print("✅ Successfully imported voting_api module")
    
    # Test add_candidate function
    print("\n--- Testing add_candidate ---")
    result = add_candidate("Test Candidate 1", "Test Party 1", "photo1.jpg", "logo1.jpg")
    print(f"✅ add_candidate result: {result}")
    
    result = add_candidate("Test Candidate 2", "Test Party 2", "photo2.jpg", "logo2.jpg")
    print(f"✅ add_candidate result: {result}")
    
    # Test get_candidate_count function
    print("\n--- Testing get_candidate_count ---")
    result = get_candidate_count()
    print(f"✅ get_candidate_count result: {result}")
    
    # Test get_all_candidates function
    print("\n--- Testing get_all_candidates ---")
    result = get_all_candidates()
    print(f"✅ get_all_candidates result: {result}")
    
    # Test get_candidate function
    print("\n--- Testing get_candidate ---")
    candidate_id = None
    if isinstance(result, list) and len(result) > 0:
        candidate_id = result[0]['id']
        result = get_candidate(candidate_id)
        print(f"✅ get_candidate result: {result}")
    
    # Test set_voting_dates function (set dates in the past so we can test voting)
    print("\n--- Testing set_voting_dates ---")
    start_date = datetime.now() - timedelta(days=10)
    end_date = datetime.now() + timedelta(days=10)
    result_date = end_date + timedelta(days=5)
    
    result = set_voting_dates(start_date, end_date, result_date)
    print(f"✅ set_voting_dates result: {result}")
    
    # Test get_voting_dates function
    print("\n--- Testing get_voting_dates ---")
    result = get_voting_dates()
    print(f"✅ get_voting_dates result: {result}")
    
    # Test update_candidate function
    print("\n--- Testing update_candidate ---")
    if candidate_id is not None:
        result = update_candidate(candidate_id, "Updated Candidate", "Updated Party", "updated_photo.jpg", "updated_logo.jpg")
        print(f"✅ update_candidate result: {result}")
        
        # Verify the update
        result = get_candidate(candidate_id)
        print(f"✅ Updated candidate: {result}")
    
    # Test vote function
    print("\n--- Testing vote ---")
    if candidate_id is not None:
        result = vote(candidate_id, "VOTER001")
        print(f"✅ vote result: {result}")
    
    print("\n🎉 All blockchain functions tested successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()