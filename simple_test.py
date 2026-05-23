import requests

# Test the results API with a valid token
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InZhaXNobmF2aXB1amFyaTQ0NDRAZ21haWwuY29tIiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNzY0NDkzNTQ4LjU5NzMzNzV9.sS9MTWX8PSG3PzkYgzWi4tlhSSF8mdahztBKZSLxXsA"
}

try:
    response = requests.get("http://127.0.0.1:8000/api/user/results", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print("Data:")
        print(data)
except Exception as e:
    print(f"Error: {e}")