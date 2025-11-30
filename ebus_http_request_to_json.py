import requests
import json
import os

# --- Configuration ---
CONFIG_FILE = "data/config.json"
output_file = "data/output.json"

# --- Load Configuration ---
config = {}
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)

# Get URL and Timeout from config
url = config["ebusd"]["ebusd_url"]
ebusd_http_timeout = config["ebusd"]["ebusd_http_timeout"]

try:
    # 1. Send the HTTP GET request
    print(f"Fetching data from {url} with a timeout of {ebusd_http_timeout} seconds...")
    response = requests.get(url, timeout=ebusd_http_timeout)
    
    # 2. Check if the request was successful (Status Code 200)
    response.raise_for_status()

    # 3. Parse the response content as JSON
    data = response.json()

    # 4. Write the data to a file
    with open(output_file, 'w', encoding='utf-8') as f:
        # indent=4 makes the file readable (pretty printed)
        json.dump(data, f, indent=4) 

    print(f"Success! Data saved to {output_file}")

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except requests.exceptions.ConnectionError as conn_err:
    print(f"Connection error occurred: {conn_err}")
except json.JSONDecodeError:
    print("Error: The response from the server was not valid JSON.")
except Exception as err:
    print(f"An unexpected error occurred: {err}")
