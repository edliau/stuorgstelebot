# stuorgstelebot
## Commands:
- FAQs : view a list of common FAQs related to booking and SAO events
- Booking: Takes in information which is used to streamline the classroom booking process
- Is Engie In? : Checks if Engie is currently in SAO
- Events : Returns a list of upcoming campus events

## Setup (For Windows, VSCode):
After cloning the repository, open the folder using the text editor of your choice and navigate to the folder in your command prompt terminal. (This can be done using File > Open Folder > stuorgstelebot , and then in the opened file, Terminal > New Terminal. By default, this should open a terminal instance in the current folder.)

You can then optionally start a virtual environment for the current project before installing the following dependencies:
```bash
pip install python-telegram-bot
pip install gspread
pip install oauth2client
```
After installing the dependencies, the bot can now be run by either clicking on the Run Python File play button in the top right of the VSCode interface, or by inputting
```bash
python main.py
```
into the terminal.

The following files are also required for the bot to run:
 
Google API credentials for your Google Sheet of choice.
The API key and name for your Telegram Bot.
