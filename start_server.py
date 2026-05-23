import os
import sys

# Change to the Database_API directory
os.chdir("Database_API")

# Add the current directory to Python path
sys.path.append(".")

# Import and run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    from main import app
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)