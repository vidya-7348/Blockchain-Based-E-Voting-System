import subprocess
import sys
import os
import time
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return the process"""
    print(f"Running: {command}")
    if cwd:
        process = subprocess.Popen(command, shell=True, cwd=cwd)
    else:
        process = subprocess.Popen(command, shell=True)
    return process

def main():
    print("🚀 Starting Complete Blockchain-Based E-Voting System")
    print("=" * 50)
    
    # Get the project root directory
    project_root = Path(__file__).parent.absolute()
    database_api_dir = project_root / "Database_API"
    
    try:
        # Step 1: Initialize database
        print("\n📋 Step 1: Initializing Database")
        init_process = subprocess.run([sys.executable, "init_voting_db.py"], 
                                    cwd=str(project_root), capture_output=True, text=True)
        if init_process.returncode == 0:
            print("✅ Database initialized successfully")
        else:
            print(f"❌ Database initialization failed: {init_process.stderr}")
            return
        
        # Step 2: Build frontend
        print("\n🔨 Step 2: Building Frontend")
        build_process = subprocess.run("npm run build", shell=True, 
                                     cwd=str(project_root), capture_output=True, text=True)
        if build_process.returncode == 0:
            print("✅ Frontend built successfully")
        else:
            print(f"❌ Frontend build failed: {build_process.stderr}")
            return
        
        # Step 3: Start backend API
        print("\n🚀 Step 3: Starting Backend API")
        backend_process = run_command(
            f"{sys.executable} -m uvicorn main:app --reload --host 127.0.0.1 --port 8000",
            cwd=str(database_api_dir)
        )
        time.sleep(3)  # Give backend time to start
        
        # Step 4: Start frontend server
        print("\n🌐 Step 4: Starting Frontend Server")
        frontend_process = run_command("node index.js", cwd=str(project_root))
        
        print("\n" + "=" * 50)
        print("🎉 System Started Successfully!")
        print("📱 Access the application at: http://127.0.0.1:8080")
        print("⚙️  Backend API available at: http://127.0.0.1:8000")
        print("🛑 Press Ctrl+C to stop all services")
        print("=" * 50)
        
        # Wait for processes to complete or for user interruption
        try:
            backend_process.wait()
            frontend_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down services...")
            backend_process.terminate()
            frontend_process.terminate()
            backend_process.wait()
            frontend_process.wait()
            print("✅ All services stopped")
            
    except Exception as e:
        print(f"❌ Error starting system: {e}")

if __name__ == "__main__":
    main()