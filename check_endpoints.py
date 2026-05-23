import re

# Read the main.py file
with open('Database_API/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all endpoint definitions
endpoints = re.findall(r'@(?:app\.)?(get|post|put|delete)\("([^"]+)"', content)

print("API Endpoints found in main.py:")
for method, path in endpoints:
    print(f"  {method.upper()} {path}")