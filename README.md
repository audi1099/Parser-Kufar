# Telegram Bot for Kufar Ads Search

This Telegram bot allows users to search for advertisements on Kufar. It retrieves search results based on the specified keyword and sends them to the user.

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
3. Create a `.env` file in the root directory and add your Telegram bot token as follows:
TOKEN=<Your_Telegram_Bot_Token>

## Usage
1. Start the bot by executing the Python script:
python bot.py
2. Open your Telegram application and find the bot by searching for its name.
3. Start a conversation with the bot.
4. Use the `/start` command to initiate the bot and select a phone model from the provided options or enter another model.
5. Receive search results directly in the Telegram chat.

## Functionality
- `/start` command: Initiates the bot and provides options to select a phone model or enter another model.
- Search: Retrieves advertisements from Kufar based on the provided keyword.
- Results: Sends the search results to the user in chunks to avoid message length limits.
- Error Handling: Provides error messages in case of any issues during the search process or when saving results to Excel.
- Excel Export: Saves the search results to an Excel file named `<keyword>_results.xlsx` for further analysis.

## Author
- Developed by [Your Name]

