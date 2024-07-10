# Restaurant Emails Web Scraping
A Python script to get emails from restaurants websites.

## Why
Sometimes it could be needed to contact many restaurants to ask for information, and one of the most common ways to do it is by email.
This script is a way to automate the process of getting the emails from the restaurant websites.

## How
The script uses Selenium to:
- Search on Google for the restaurants in a city (e.g. "restaurants Milano")
- Click on the Website of each restaurant in the page
- Get the email from the website and save it
- Navigate back to the Google page and repeat the process for the next restaurants in the page
- Save the emails in a CSV file
- Repeat the process for the next pages of Google search

The script actually can process an array of cities, saving all the emails into a `data/restaurants.csv` file, avoiding duplicates.

## Requirements
- Python 3

## Installation
1. Clone the repository
2. Setup a virtual environment with `python -m venv venv`
3. Activate the virtual environment with 
   - `source venv/bin/activate` on macOS / Linux
   - `venv\Scripts\activate` on Windows
4. Install selenium with `pip install --upgrade selenium`
5. Run the script with `python get_emails.py`
6. Deactivate the virtual environment with `deactivate`

## Configuration
The script is ready to be used, but you can change the cities to search for in the `cities` array in the `get_emails.py` file.

## Disclaimer
This script is for educational purposes only. The author is not responsible for any misuse of the information provided.
