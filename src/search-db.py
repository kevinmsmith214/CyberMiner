import requests
import json

def search_db_api(items):
    # API endpoint URL
    url = 'https://kuekmhuxf8.execute-api.us-east-1.amazonaws.com/project/search'
    # Create the payload as a dictionary
    payload = {'titles': items}

    # Convert the dictionary to a JSON formatted string
    json_payload = json.dumps(payload)

    # Set headers to specify that the request body is JSON
    headers = {'Content-Type': 'application/json'}

    # Send the POST request
    response = requests.post(url, data=json_payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the response data
        print("Response from API:", response.text)
        return response.json()  # Return the JSON response if needed
    else:
        print("Failed to fetch data from API. Status Code:", response.status_code)
        return None

# Example usage
items_to_search = ["List of Farm to Market Roads in Texas (700â€“799) - Wikipedia", "Wyoming Valley - Wikipedia"]

result = search_db_api(items_to_search)
print("Query Results:", result)
