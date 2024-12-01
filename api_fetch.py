import toml
import os
import aiohttp
import asyncio
import json

# Asynchronously fetch Hearthstone card data from Blizzard's API
async def fetch_hearthstone_data():
    # Load API credentials from the config file
    config = toml.load('config.toml')
    client_id = config['blizzard_api']['client_id']
    client_secret = config['blizzard_api']['client_secret']

    # API URL for fetching Hearthstone cards
    url = 'https://us.api.blizzard.com/hearthstone/cards?locale=en_US&pageSize=500'

    # OAuth token request URL and data
    auth_url = 'https://us.battle.net/oauth/token'
    auth_data = {'grant_type': 'client_credentials'}

    # Create an HTTP session to interact with the API
    async with aiohttp.ClientSession() as session:
        # Send POST request to get the access token
        async with session.post(auth_url, data=auth_data, auth=aiohttp.BasicAuth(client_id, client_secret)) as response:
            # If authentication fails, print an error and return an empty list
            if response.status != 200:
                print("Error fetching OAuth token:", response.status, await response.text())
                return []
            # Parse the response to extract the access token
            token_data = await response.json()
            access_token = token_data['access_token']
    
        # Set the authorization header for subsequent API requests
        headers = {'Authorization': f'Bearer {access_token}'}

        # List to store all the Hearthstone cards
        all_cards = []
        
        # Function to fetch a single page of cards
        async def fetch_page(page_number):
            page_url = f'{url}&page={page_number}'
            async with session.get(page_url, headers=headers) as response:
                # If the page request is successful, parse and return the cards
                if response.status == 200:
                    data = await response.json()
                    return data.get('cards', [])
                else:
                    print(f"Error fetching data for page {page_number}: {response.status}")
                    return []

        # Function to fetch all pages concurrently
        async def fetch_all_pages():
            tasks = []
            page_number = 1  # Start from page 1
            while True:
                tasks.append(fetch_page(page_number))  # Add the task for this page
                page_number += 1
                if len(tasks) >= 10:  # Batch the requests for efficiency
                    # Wait for all the tasks to finish
                    pages = await asyncio.gather(*tasks)
                    # Process each page of data
                    for page in pages:
                        if not page:  # Stop if there's no data on the current page
                            return all_cards
                        all_cards.extend(page)  # Add the fetched cards to the list
                    tasks = []  # Reset tasks after processing a batch
            return all_cards
        
        # Fetch all pages concurrently and collect the data
        all_cards = await fetch_all_pages()

    # Save the fetched data to a JSON file
    with open('hearthstone_all_cards.json', 'w') as json_file:
        json.dump(all_cards, json_file, indent=4)

    # Print the total number of cards fetched from the API
    print(f"Fetched {len(all_cards)} cards in total from the API.")
    
    return all_cards

# Run the fetch function if the script is executed directly
if __name__ == "__main__":
    asyncio.run(fetch_hearthstone_data())
