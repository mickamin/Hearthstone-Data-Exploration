# Hearthstone Data Exploration

Welcome to the **Hearthstone Data Exploration** project! This project fetches Hearthstone card data from the Blizzard API, stores it locally, and includes analysis of the data.

![Alt Text](https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDZyN2p1cWl4b3Ayc215N3pybDZtOGgwYTI4a2JsenV0emxucWVnaCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3LJ50bojhw9Lc9UJqA/giphy.webp)

## Features

- **Fetches** all Hearthstone card data using the Blizzard API.
- **Analyzes** card mana cost distribution and key card features.
- **Visualizes** the data using `matplotlib` and Jupyter Notebooks.

## Setup Instructions

### Prerequisites
Make sure you have the following installed:

- Python 3.x
- Required Python libraries:
  - `requests` (for API requests)
  - `pandas` (for data handling)
  - `matplotlib` and `seaborn` (for plotting)
  - `toml` (for configuration file parsing)

To install the required libraries, run:

```bash
pip install requests pandas matplotlib seaborn toml
```
## Configuring the API

1. Create a config.toml file in the root directory of the project with the following content:

```toml
[blizzard_api]
client_id = "your_client_id"
client_secret = "your_client_secret"
``` 
2. Replace your_client_id and your_client_secret with your actual Blizzard API credentials.

## Fetch Data

To fetch all Hearthstone card data, run the following script:

```bash
python blizzard_api_fetcher.py
``` 

This will fetch all Hearthstone cards from the Blizzard API and store the data in a hearthstone_all_cards.json file.

