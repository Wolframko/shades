import requests
import json
import os

# API base URL
BASE_URL = "http://localhost:8000"

# Load test input data
with open("testinput.json", "r") as f:
    test_data = json.load(f)

# Ensure output directory exists
os.makedirs("test_output", exist_ok=True)

# Test JSON endpoint
print("Testing JSON endpoint...")
response = requests.post(f"{BASE_URL}/pack/json", json=test_data)
if response.status_code == 200:
    json_data = response.json()
    with open("test_output/output.json", "w") as f:
        json.dump(json_data, f, indent=2)
    print("JSON output saved to test_output/output.json")
    
    # Check for warnings
    if json_data["warnings"]:
        print("Warnings:")
        for warning in json_data["warnings"]:
            print(f"- {warning}")
else:
    print(f"Error: {response.status_code} - {response.text}")

# Test HTML endpoint
print("Testing HTML endpoint...")
response = requests.post(f"{BASE_URL}/pack/html", json=test_data)
if response.status_code == 200:
    with open("test_output/output.html", "w") as f:
        f.write(response.text)
    print("HTML output saved to test_output/output.html")
else:
    print(f"Error: {response.status_code} - {response.text}")


print("API testing completed.")
