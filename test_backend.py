import os
import sys
import time

# Set the correct contract address before importing
os.environ['CONTRACT_ADDRESS'] = '0x48aa51D32E6B7Fbbde01bABB3274C21d9471AB0E'

# Add the Database_API directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Database_API'))

try:
    # Change to Database_API directory
    os.chdir(os.path.join(os.path.dirname(__file__), 'Database_API'))
    
    # Import the app
    from main import app
    
    # Test import voting_api to check contract loading
    import voting_api
    print("Voting API imported successfully")
    print(f"Contract loaded: {voting_api.contract is not None}")
    if voting_api.contract_address:
        print(f"Contract address: {voting_api.contract_address}")
    
    print("Backend components loaded successfully!")
    
except Exception as e:
    print(f"Error loading backend components: {e}")
    import traceback
    traceback.print_exc()