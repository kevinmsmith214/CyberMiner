import requests
import json

def login_api(action, username, password, user_type):
    # API endpoint URL
    url = 'https://kuekmhuxf8.execute-api.us-east-1.amazonaws.com/project/login'

    # Create the payload as a dictionary
    payload = {
        "action": action,
        "username": username,
        "password": password,
        "user_type": user_type
    }

    # Send the POST request
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})

    # Check if the request was successful
    if response.status_code == 200 or response.status_code == 201:
        # Print and return the response data
        print("Response from API:", response.text)
        return response.json()  # Return the JSON response if needed
    else:
        # Print the error status code and message
        print("Failed to fetch data from API. Status Code:", response.status_code)
        print("Response Body:", response.text)
        return None

# Example usage
action = "login"
username = "sample_username"
password = "sample_password"
user_type = "Advertiser"

result = login_api(action, username, password, user_type)
print("Query Results:", result)
