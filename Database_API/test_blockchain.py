import os
import sys
from pathlib import Path

# Add the current directory to the path
sys.path.insert(0, str(Path(__file__).parent))

# Try to import the voting_api module
try:
    from voting_api import add_candidate
    print("✅ Successfully imported voting_api module")
    
    # Try to call the add_candidate function
    result = add_candidate("Test Candidate", "Test Party")
    print(f"✅ add_candidate result: {result}")
except Exception as e:
    print(f"❌ Error: {e}")