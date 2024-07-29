import requests
import json

# Path to your JSON file
def load_json_file(file_path):
    # Open the file with 'utf-8' encoding
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

file_path = 'scraped_data.json'

# Read the JSON file into a variable
data = load_json_file(file_path)


# URL of the API
url = 'https://kuekmhuxf8.execute-api.us-east-1.amazonaws.com/project/upload-data'

# Headers: usually include the 'Content-Type' as 'application/json'
headers = {
    'Content-Type': 'application/json'
}

# Make the POST request
response = requests.post(url, json=data, headers=headers)

# Print the response from the server
print(response.text)

# Check the response status code
if response.status_code == 200:
    print("Success!")
else:
    print(f"Error: {response.status_code}")
