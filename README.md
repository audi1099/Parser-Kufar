# Telegram bot for searching advertisements in Kufar

This Telegram bot allows users to search for advertisements in Kufar. It retrieves search results based on a specified keyword and 
sends them to the user.

## Requirements
- Python 3.6 or higher
- Required Python packages:
  - `requests`
  - `telebot`
  - `bs4` (Beautiful Soup)
  - `openpyxl`
  - `dotenv`

## Installation
1. Clone the repository or download the code files.
2. Install the required Python packages using pip:
pip install requests telebot beautifulsoup4 openpyxl python-dotenv
3. Create a .env file in the root directory and add your Telegram bot token as follows:
TOKEN=<Your_Telegram_Bot_Token>

## Usage
1. Run the bot by executing the Python script:
python bot.py
2. Open the Telegram app and search for the bot by entering its name in the search bar.
3. Start a conversation with the bot.
4. Use the /start command to initiate the bot and choose a phone model from the provided options or enter another model.
5. Receive search results directly in the Telegram chat.

## Functionality
- Command /start: Initiates the bot and provides options to choose a phone model or enter another model.
- Search: Retrieves ads from Kufar based on the provided keyword.
- Results: Sends search results to the user in parts to avoid message length limitations.
- Error Handling: Provides error messages in case of issues during the search or saving results to Excel.
- Export to Excel: Saves search results in an Excel file named <keyword>_results.xlsx for further analysis.

## Author
- Developed by [audi1099]

