import requests

# Define the API endpoint
url = "http://localhost:8080/generate"

# Define the payload (processed data for text generation)
data = {
    "processed_data": "Once upon a time"
}

# Make the POST request to the FastAPI endpoint
response = requests.post(url, json=data)

# Check if the request was successful
if response.status_code == 200:
    # Parse and print the generated text from the response
    generated_text = response.json()
    print(f"Generated Text: {generated_text['generated_text']}")
else:
    print(f"Error: {response.status_code}, {response.text}")
