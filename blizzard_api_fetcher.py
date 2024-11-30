import requests
import json
import toml

def fetch_hearthstone_data():
    # Load credentials from config.toml
    config = toml.load('config.toml')

    # Get the credentials from the config
    client_id = config['blizzard_api']['client_id']
    client_secret = config['blizzard_api']['client_secret']

    # Blizzard API URL for Hearthstone cards with a fixed pageSize
    url = 'https://us.api.blizzard.com/hearthstone/cards?locale=en_US&pageSize=500'

    # Step 1: Get the OAuth token (for authentication)
    auth_url = 'https://us.battle.net/oauth/token'
    auth_data = {'grant_type': 'client_credentials'}

    # Make a POST request to get the access token
    response = requests.post(auth_url, data=auth_data, auth=(client_id, client_secret))

    # Check if authentication was successful
    if response.status_code != 200:
        print("Error fetching OAuth token:", response.status_code, response.text)
        return

    access_token = response.json()['access_token']

    # Step 2: Fetch data from Hearthstone cards endpoint using page-based pagination
    headers = {'Authorization': f'Bearer {access_token}'}

    # To store all cards
    all_cards = []
    page_number = 1  # Start from page 1

    # Loop to fetch all pages
    while True:
        # Modify the URL to include the page parameter
        page_url = f'{url}&page={page_number}'
        response = requests.get(page_url, headers=headers)

        if response.status_code == 200:
            data = response.json()

            # Add cards to the list
            all_cards.extend(data.get('cards', []))

            # If there are no cards in this response, stop the loop (end of pagination)
            if len(data.get('cards', [])) == 0:
                break

            page_number += 1
        else:
            print(f"Error fetching data: {response.status_code}, {response.text}")
            break

    # Step 3: Save all cards data to a JSON file
    with open('hearthstone_all_cards.json', 'w') as json_file:
        json.dump(all_cards, json_file, indent=4)

    # Print how many cards were fetched
    print(f"Fetched {len(all_cards)} cards in total.")
