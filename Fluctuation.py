import requests
import time

def call_api():
    url = 'https://pricingservice-z16l.onrender.com/update_fluctuation/'  # Replace with your API endpoint
    try:
        response = requests.post(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        print(f"API response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")

def main():
    while True:
        call_api()
        time.sleep(2)  # Wait for 15 seconds before the next call

if __name__ == "__main__":
    main()