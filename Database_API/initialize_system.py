#!/usr/bin/env python3
"""Complete system initialization script"""
import sys
from pathlib import Path

def main():
    print("🚀 Initializing Blockchain-Based E-Voting System")
    print("=" * 60)
    
    # Get script directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    print("\n📋 Step 1: Initializing Database Tables")
    print("-" * 60)
    try:
        import subprocess
        result = subprocess.run([sys.executable, "init_voting_db.py"], 
                              cwd=str(script_dir), capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"Warning: {result.stderr}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n📋 Step 2: Creating Candidates Table")
    print("-" * 60)
    try:
        result = subprocess.run([sys.executable, "init_candidates_table.py"], 
                              cwd=str(script_dir), capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"Warning: {result.stderr}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n📋 Step 3: Checking Contract Deployment")
    print("-" * 60)
    try:
        result = subprocess.run([sys.executable, "get_contract_address.py"], 
                              cwd=str(project_root), capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"Warning: {result.stderr}")
            print("\n⚠️  Contract not deployed. Run 'truffle migrate' to deploy.")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ System initialization completed!")
    print("\n📝 Next Steps:")
    print("1. Start Ganache: ganache")
    print("2. Deploy contracts: truffle migrate")
    print("3. Start backend: uvicorn main:app --reload --host 127.0.0.1")
    print("4. Start frontend: node index.js")
    print("=" * 60)

if __name__ == "__main__":
    main()


