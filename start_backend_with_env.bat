@echo off
cd /d "C:\Users\Genius\Desktop\voting mainfullmainnn0002 (4)\voting mainfullmainnn0002\voting mainfullmainnn (2)\voting mainfullmainnn\voting mainfull\voting main01\Decentralized-Voting-System-main\Database_API"
set CONTRACT_ADDRESS=0x48aa51D32E6B7Fbbde01bABB3274C21d9471AB0E
echo Starting backend server with correct contract address...
python -m uvicorn main:app --host 127.0.0.1 --port 8000
pause