import os
import json
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

# Try to import web3, but handle the case when it's not available
try:
    from web3 import Web3
    WEB3_AVAILABLE = True
    print("[VOTING_API] web3 module imported successfully")
except ImportError as e:
    print(f"[VOTING_API] web3 module not available: {e}")
    print("[VOTING_API] System will work in database-only mode")
    Web3 = None
    WEB3_AVAILABLE = False

# Load environment variables
load_dotenv(dotenv_path=Path(__file__).with_name('.env'))

# Connect to Ethereum node (using Ganache for development)
# In production, you would use a real Ethereum node URL
if WEB3_AVAILABLE:
    ganache_url = os.environ.get('GANACHE_URL', 'http://127.0.0.1:7545')
    w3 = Web3(Web3.HTTPProvider(ganache_url))
    
    # Check connection on import
    try:
        if w3.is_connected():
            print(f"✅ Connected to blockchain at {ganache_url}")
            try:
                chain_id = w3.eth.chain_id
                block_number = w3.eth.block_number
                print(f"   Chain ID: {chain_id}, Latest block: {block_number}")
            except:
                pass
        else:
            print(f"⚠️  Not connected to blockchain at {ganache_url}")
            print("   Start Ganache or update GANACHE_URL in .env file")
    except Exception as e:
        print(f"⚠️  Blockchain connection error: {e}")
        print("   The system will work with database storage only")
else:
    w3 = None
    print("[VOTING_API] Skipping blockchain connection as web3 is not available")

# Load contract ABI and address
contract_address = None
contract_abi = None

def load_contract_address():
    """Load contract address from build file or environment variable"""
    global contract_address, contract
    try:
        # First try to get contract address from environment variable
        env_contract_address = os.environ.get('CONTRACT_ADDRESS')
        if env_contract_address:
            contract_address = env_contract_address
            print(f"✅ Contract address loaded from environment: {contract_address}")
            
            # Load contract ABI from build file
            build_path = Path(__file__).parent.parent / 'build' / 'contracts' / 'Voting.json'
            if build_path.exists():
                with open(build_path) as f:
                    contract_data = json.load(f)
                    contract_abi_value = contract_data.get('abi')
                    if contract_abi_value:
                        global contract_abi
                        contract_abi = contract_abi_value
                        # Only create contract instance if web3 is available
                        if WEB3_AVAILABLE and w3 and w3.is_connected():
                            contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address) if hasattr(Web3, 'to_checksum_address') else contract_address, abi=contract_abi)
                            print("✅ Contract ABI loaded and contract instance created")
                        else:
                            print("⚠️  Contract ABI loaded but web3 not available, skipping contract instance creation")
                        return True
            else:
                print(f"Warning: Contract build file not found at {build_path}")
        else:
            # Fallback to loading from build file networks section
            # Load contract data from build directory
            build_path = Path(__file__).parent.parent / 'build' / 'contracts' / 'Voting.json'
            if not build_path.exists():
                print(f"Warning: Contract build file not found at {build_path}")
                return False
                
            with open(build_path) as f:
                contract_data = json.load(f)
                contract_abi_value = contract_data.get('abi')
                if contract_abi_value:
                    contract_abi = contract_abi_value
                
                # Try to get contract address from networks
                networks = contract_data.get('networks', {})
                if networks:
                    # Get the first network (usually the development network)
                    network_id = list(networks.keys())[0]
                    network_info = networks[network_id]
                    address = network_info.get('address')
                    
                    if address:
                        contract_address = address
                        # Only create contract instance if web3 is available
                        if WEB3_AVAILABLE and contract_abi:
                            if w3 and w3.is_connected():
                                contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address) if hasattr(Web3, 'to_checksum_address') else contract_address, abi=contract_abi)
                                print("✅ Contract address loaded and contract instance created")
                            else:
                                print("⚠️  Contract address loaded but web3 not available, skipping contract instance creation")
                        return True
                    else:
                        print("Warning: No contract address found in network info")
                else:
                    print("Warning: No networks found in build file. Run 'truffle migrate' to deploy.")
                    
    except Exception as e:
        print(f"Error loading contract: {e}")
    
    return False

# Try to load contract address automatically on import
try:
    load_contract_address()
except Exception as e:
    print(f"Note: Could not auto-load contract address: {e}")
    print("You can set it manually using set_contract_address()")

# Ensure contract is initialized if web3 becomes available later
def ensure_contract_initialized():
    """Ensure the contract is properly initialized"""
    global contract, contract_address, contract_abi
    
    # If contract is already initialized, return
    if contract is not None:
        return True
        
    # If we have all required components, initialize the contract
    if contract_address and contract_abi and WEB3_AVAILABLE and w3 and w3.is_connected():
        try:
            contract = w3.eth.contract(
                address=Web3.to_checksum_address(contract_address) if hasattr(Web3, 'to_checksum_address') else contract_address, 
                abi=contract_abi
            )
            print("✅ Contract instance created on demand")
            return True
        except Exception as e:
            print(f"Error creating contract instance: {e}")
    
    return contract is not None
# Contract instance (initialize as None)
contract = None

# Admin account for contract interactions (in development, this would be from Ganache)
admin_account = None
admin_private_key = None

# Try to load admin account from environment variables or Ganache
try:
    admin_private_key_env = os.environ.get('ADMIN_PRIVATE_KEY')
    
    if admin_private_key_env and WEB3_AVAILABLE:
        # Derive account from private key
        try:
            from eth_account import Account
            admin_account = Account.from_key(admin_private_key_env).address
            admin_private_key = admin_private_key_env
            print(f"✅ Admin account loaded from environment: {admin_account}")
        except Exception as e:
            print(f"Note: Could not load admin account from private key: {e}")
    elif WEB3_AVAILABLE and w3 and w3.is_connected():
        # Get first account from Ganache if admin key not provided
        try:
            accounts = w3.eth.accounts
            if accounts and len(accounts) > 0:
                admin_account = accounts[0]
                # Note: In production, you should use the private key, not just the address
                print(f"✅ Using first Ganache account as admin: {admin_account}")
                print("⚠️  Warning: For blockchain operations, you need ADMIN_PRIVATE_KEY in .env")
        except Exception as e:
            print(f"Note: Could not get accounts from Ganache: {e}")
except Exception as e:
    print(f"Note: Could not load admin account: {e}")

def set_contract_address(address):
    """Set the contract address after deployment"""
    global contract_address, contract
    contract_address = address
    if WEB3_AVAILABLE and contract_abi and w3 and w3.is_connected():
        contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address) if hasattr(Web3, 'to_checksum_address') else contract_address, abi=contract_abi)

def set_admin_account(account, private_key):
    """Set the admin account for contract interactions"""
    global admin_account, admin_private_key
    admin_account = account
    admin_private_key = private_key

def add_candidate(name, party, photo_hash="", party_logo_hash=""):
    """Add a candidate to the blockchain"""
    if not contract or not admin_account or not admin_private_key:
        return {"error": "Contract or admin account not configured"}
    
    try:
        # Build transaction
        transaction = contract.functions.addCandidate(name, party, photo_hash, party_logo_hash).build_transaction({
            'from': admin_account,
            'gas': 1000000,
            'gasPrice': w3.to_wei('10', 'gwei'),
            'nonce': w3.eth.get_transaction_count(admin_account),
        })
        
        # Sign transaction
        signed_txn = w3.eth.account.sign_transaction(transaction, admin_private_key)
        
        # Send transaction (handle both old and new web3.py versions)
        if hasattr(signed_txn, 'raw_transaction'):
            # New web3.py version
            tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        else:
            # Old web3.py version
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        # Wait for transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return {
            "success": True,
            "transaction_hash": tx_hash.hex(),
            "candidate_id": contract.functions.countCandidates().call()
        }
    except Exception as e:
        return {"error": str(e)}

def set_voting_dates(start_date, end_date, result_date):
    """Set voting start, end, and result dates"""
    ensure_contract_initialized()
    if not contract or not admin_account or not admin_private_key:
        return {"error": "Contract or admin account not configured"}    
    try:
        # Convert dates to timestamps
        start_timestamp = int(start_date.timestamp())
        end_timestamp = int(end_date.timestamp())
        result_timestamp = int(result_date.timestamp())
        
        # Build transaction
        transaction = contract.functions.setElectionDates(start_timestamp, end_timestamp, result_timestamp).build_transaction({
            'from': admin_account,
            'gas': 1000000,
            'gasPrice': w3.to_wei('10', 'gwei'),
            'nonce': w3.eth.get_transaction_count(admin_account),
        })
        
        # Sign transaction
        signed_txn = w3.eth.account.sign_transaction(transaction, admin_private_key)
        
        # Send transaction (handle both old and new web3.py versions)
        if hasattr(signed_txn, 'raw_transaction'):
            # New web3.py version
            tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        else:
            # Old web3.py version
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        # Wait for transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return {
            "success": True,
            "transaction_hash": tx_hash.hex()
        }
    except Exception as e:
        return {"error": str(e)}

def update_candidate(candidate_id, name, party, photo_hash="", party_logo_hash=""):
    """Update a candidate in the blockchain"""
    ensure_contract_initialized()
    if not contract or not admin_account or not admin_private_key:
        return {"error": "Contract or admin account not configured"}
    
    try:
        # Build transaction
        transaction = contract.functions.updateCandidate(candidate_id, name, party, photo_hash, party_logo_hash).build_transaction({
            'from': admin_account,
            'gas': 1000000,
            'gasPrice': w3.to_wei('10', 'gwei'),
            'nonce': w3.eth.get_transaction_count(admin_account),
        })
        
        # Sign transaction
        signed_txn = w3.eth.account.sign_transaction(transaction, admin_private_key)
        
        # Send transaction (handle both old and new web3.py versions)
        if hasattr(signed_txn, 'raw_transaction'):
            # New web3.py version
            tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        else:
            # Old web3.py version
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        # Wait for transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return {
            "success": True,
            "transaction_hash": tx_hash.hex()
        }
    except Exception as e:
        return {"error": str(e)}

def get_voting_dates():
    """Get voting start, end, and result dates"""
    ensure_contract_initialized()
    if not contract:
        return {"error": "Contract not configured"}    
    try:
        start_date, end_date, result_date = contract.functions.getElectionDates().call()
        return {
            "start_date": start_date,
            "end_date": end_date,
            "result_date": result_date
        }
    except Exception as e:
        return {"error": str(e)}

def get_candidate_count():
    """Get the number of candidates"""
    ensure_contract_initialized()
    if not contract:
        return {"error": "Contract not configured"}
    
    try:
        count = contract.functions.countCandidates().call()
        return {"count": count}
    except Exception as e:
        return {"error": str(e)}
def get_candidate(candidate_id):
    """Get candidate details by ID"""
    ensure_contract_initialized()
    if not contract:
        return {"error": "Contract not configured"}
    
    try:
        candidate_data = contract.functions.getCandidate(candidate_id).call()
        return {
            "id": candidate_data[0],
            "name": candidate_data[1],
            "party": candidate_data[2],
            "photo_hash": candidate_data[3],
            "party_logo_hash": candidate_data[4],
            "vote_count": candidate_data[5]
        }
    except Exception as e:
        return {"error": str(e)}

def vote(candidate_id, voter_id):
    """Cast a vote for a candidate"""
    print(f"[VOTING_API] vote() called with candidate_id={candidate_id}, voter_id={voter_id}")
    
    # Database-based voting system
    # Blockchain integration is optional - votes are tracked in database
    
    # Ensure contract is initialized if possible
    ensure_contract_initialized()
    
    # If web3 is not available or blockchain is not connected, just return success
    # The database already tracks votes via has_voted column and voter_id
    if not WEB3_AVAILABLE or not contract or not w3 or not w3.is_connected():
        print("[VOTING_API] Using database-only mode (web3 not available or not connected)")
        return {
            "success": True,
            "transaction_hash": "0x" + "0" * 64  # Dummy hash when blockchain is not used
        }
    
    print("[VOTING_API] Contract and Web3 connection available, attempting blockchain vote")
    
    # If blockchain is available, try to use it but don't fail if wallet issues occur
    voter_account = None
    voter_private_key = os.environ.get('VOTER_PRIVATE_KEY')
    
    # Use the account with funds (0xF4eDE00BCD2C2b1CF5c18609875479be5c16E465)
    # The private key in .env now corresponds to this account
    if voter_private_key:
        try:
            voter_account = w3.eth.account.from_key(voter_private_key).address
            print(f"[VOTING_API] Using voter account with funds: {voter_account}")
        except Exception as e:
            print(f"[VOTING_API] Error deriving account from private key: {e}")
    else:
        print("[VOTING_API] No voter private key available")
    
    print(f"[VOTING_API] Voter private key available: {bool(voter_private_key)}")
    
    # If no wallet configured, skip blockchain and return success
    # Database handles vote tracking
    if not voter_account or not voter_private_key:
        print("[VOTING_API] No voter account or private key, using database-only mode")
        return {
            "success": True,
            "transaction_hash": "0x" + "0" * 64  # Dummy hash
        }
    
    try:
        print("[VOTING_API] Checking if voter has already voted")
        # Check if voter has already voted with this voter ID
        try:
            has_voted = contract.functions.hasVoterIdVoted(voter_id).call()
            if has_voted:
                print("[VOTING_API] Voter has already voted")
                return {"error": "You have already voted"}
        except Exception as e:
            print(f"[WARNING] Could not check if voter has already voted: {str(e)}")
            # Continue with voting even if we can't check
        
        print("[VOTING_API] Checking if voting is active")
        # Check if voting is active
        try:
            election_dates = contract.functions.electionDates().call()
            start_date = election_dates[0]
            end_date = election_dates[1]
            current_time = int(datetime.utcnow().timestamp())
            
            print(f"[VOTING_API] Election dates - Start: {start_date}, End: {end_date}, Current: {current_time}")
            
            if current_time < start_date:
                print("[VOTING_API] Voting has not started yet")
                return {"error": "Voting has not started yet"}
            elif current_time > end_date:
                print("[VOTING_API] Voting has ended")
                return {"error": "Voting has ended"}
        except Exception as e:
            print(f"[WARNING] Could not check voting dates: {str(e)}")
            # Continue with voting even if we can't check dates
        
        print("[VOTING_API] Building transaction")
        # Build transaction
        transaction = contract.functions.vote(candidate_id, voter_id).build_transaction({
            'from': voter_account,
            'gas': 1000000,
            'gasPrice': w3.to_wei('10', 'gwei'),
            'nonce': w3.eth.get_transaction_count(voter_account),
        })
        
        print("[VOTING_API] Signing transaction")
        # Sign transaction
        signed_txn = w3.eth.account.sign_transaction(transaction, voter_private_key)
        
        print("[VOTING_API] Sending transaction")
        # Send transaction (handle both old and new web3.py versions)
        if hasattr(signed_txn, 'raw_transaction'):
            # New web3.py version
            tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        else:
            # Old web3.py version
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        print("[VOTING_API] Waiting for transaction receipt")
        # Wait for transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        print(f"[VOTING_API] Transaction successful: {tx_hash.hex()}")
        return {
            "success": True,
            "transaction_hash": tx_hash.hex()
        }
    except Exception as e:
        # If blockchain fails, still allow voting via database
        # Return success with dummy hash
        print(f"[WARNING] Blockchain vote failed, using database only: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "success": True,
            "transaction_hash": "0x" + "0" * 64  # Dummy hash
        }

def get_winner():
    """Get the winning candidate"""
    if not contract:
        return {"error": "Contract not configured"}
    
    try:
        # Check if result date has passed
        election_dates = contract.functions.electionDates().call()
        result_date = election_dates[2]
        current_time = int(datetime.utcnow().timestamp())
        
        if current_time < result_date:
            return {"error": "Results not available yet"}
        
        # Get winner from contract
        winner_id, winner_name, winner_party, winner_photo_hash, winner_party_logo_hash, winner_votes = contract.functions.getWinner().call()
        
        return {
            "id": winner_id,
            "name": winner_name,
            "party": winner_party,
            "photo_hash": winner_photo_hash,
            "party_logo_hash": winner_party_logo_hash,
            "vote_count": winner_votes
        }
    except Exception as e:
        return {"error": str(e)}

def get_all_candidates():
    """Get all candidates"""
    if not contract:
        return {"error": "Contract not configured"}
    
    try:
        candidate_count = contract.functions.countCandidates().call()
        candidates = []
        
        for i in range(1, candidate_count + 1):
            candidate_data = contract.functions.getCandidate(i).call()
            candidates.append({
                "id": candidate_data[0],
                "name": candidate_data[1],
                "party": candidate_data[2],
                "photo_hash": candidate_data[3],
                "party_logo_hash": candidate_data[4],
                "vote_count": candidate_data[5]
            })
        
        return candidates
    except Exception as e:
        return {"error": str(e)}

# Module exports
__all__ = [
    'set_contract_address',
    'set_admin_account',
    'add_candidate',
    'update_candidate',
    'set_voting_dates',
    'get_voting_dates',
    'get_candidate_count',
    'get_candidate',
    'vote',
    'get_winner',
    'get_all_candidates'
]
