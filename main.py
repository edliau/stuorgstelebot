from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import asyncio
from datetime import datetime
from sao_bot_tokens import TELEGRAM_TOKEN, USERNAME
from faqs import faq_command, faq_funding_command, faq_payments_command, faq_people_to_contact_command, faq_quickguide_command, funding_cif_command, funding_general_command, funding_travel_command, payment_rfp_command, payment_copay_command, payment_invoice_command, payment_pcard_command


# Telegram Bot Token and API
TOKEN: Final = TELEGRAM_TOKEN
BOT_USERNAME: Final = USERNAME

# Google Sheets API Credentials
GOOGLE_SHEETS_CREDS: Final = 'stuorgs-telegram-bot-test-4510b304b71e.json'
MASTER_SPREADSHEET: Final = 'StuOrgs Tele Bot Master Sheet'

# Initialize Google Sheets API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_CREDS, scope)
client = gspread.authorize(creds)

# GLOBAL VARIABLES AND STATES
# Global variable for Engie's status
engie_status = False

# Define conversation states
NAME, BOOKING_DATE, ORGANISATION, LOCATION, TIME_START, TIME_END = range(6)

# Dictionary to store collected data, used for booking info and checking identity of who is using the /engiestatus command
user_data = {}

#function to start the bot
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''Hello! I'm Stu, your go-to bot for all things Stuorgs related! Please click the menu to use the various functions we have available. You may view this message again at any time using the /help command :-)
                                     
/faq: Provides a list of FAQs you can check before contacting us
/booking: Allows for submission of classroom booking requests
/engie: Checks if Engie is in the office today
/events: Provides a list of upcoming campus events''')

#function to return list of commands
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''Hello! Please click the menu to use the various functions we have available. Our feedback form is in the profile description.
                                     
/faq: Provides a list of FAQs you can check before contacting us
/booking: Allows for submission of classroom booking requests
/engie: Checks if Engie is in the office today
/events: Provides a list of upcoming campus events''')

#command to cancel the booking request
async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get('cancel', False):
        context.user_data['cancel'] = True  # Set the cancel flag
        await update.message.reply_text('The current booking process has been cancelled.')

#command for starting booking, asks for requester's name
async def booking_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['cancel'] = False
    await update.message.reply_text('Thank you for using the booking system! Please make sure that your chosen slot is available on FBS before submitting your request. At any point, input /cancel_booking to cancel the process. Please give your full name.')
    return NAME

#updates data with name, asks for date of booking
async def booking_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('cancel', False):
        await cancel_command(update, context)
        return ConversationHandler.END
    user_name = update.message.text
    user_data['user_name'] = user_name
    await update.message.reply_text('Please give the date of your booking.')
    return BOOKING_DATE

#updates data with date of booking, asks for organisation
async def booking_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('cancel', False):
        await cancel_command(update, context)
        return ConversationHandler.END
    booking_date = update.message.text
    user_data['booking_date'] = booking_date
    await update.message.reply_text('What organisation are you making this booking for?')
    return ORGANISATION

#updates data with organisation, asks for booking space
async def booking_organisation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('cancel', False):
        await cancel_command(update, context)
        return ConversationHandler.END
    organisation = update.message.text
    user_data['organisation'] = organisation
    await update.message.reply_text('What space would you like to book?')
    return LOCATION

#updates data with booking location, asks for booking start time
async def booking_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('cancel', False):
        await cancel_command(update, context)
        return ConversationHandler.END    
    location = update.message.text
    user_data['location'] = location
    await update.message.reply_text('Please provide the booking start time (e.g., 10:00 AM)')
    return TIME_START

#updates data with start time, asks for end time
async def booking_time_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('cancel', False):
        await cancel_command(update, context)
        return ConversationHandler.END
    time_start = update.message.text
    user_data['time_start'] = time_start
    await update.message.reply_text('Please provide the booking end time (e.g., 12:00 PM)')
    return TIME_END

#updates data with end time, writes data to spreadsheet
async def booking_time_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('cancel', False):
        await cancel_command(update, context)
        return ConversationHandler.END
    time_end = update.message.text
    user_data['time_end'] = time_end

    # calls the items defined under user_data
    user_name = user_data['user_name']
    booking_date = user_data['booking_date']
    organisation = user_data['organisation']
    location = user_data['location']
    time_start = user_data['time_start']
    time_end = user_data['time_end']

    #put the items into a single array and writes them to the spreadsheet
    data = [update.message.from_user.id, user_name, booking_date, organisation, location, time_start, time_end]
    write_booking_data(data)

    # once the end time has been written and the data is uploaded to the spreadsheet, return confirmation message 
    await update.message.reply_text("Your booking request has been submitted! Do note that your booking remains unconfirmed until we reply you with a confirmation email, and that booking attempts made for timeslots which are listed as unavailable on Halcyon Hub will be disregarded. ")
    return ConversationHandler.END

#function to write data to master google sheet
def write_booking_data(data):
    try:
        booking_spreadsheet = client.open(MASTER_SPREADSHEET)
        booking_worksheet = booking_spreadsheet.get_worksheet(0)
    except Exception as e:
        print("Error opening the spreadsheet:", str(e))
        exit(1)
    try:
        booking_worksheet.append_row(data)
    except Exception as e:
        print("Error writing to Google Sheets:", str(e))

#command to view upcoming events
async def events_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Call the function to get data from Google Sheets
    message = get_events_data()

    # Send the retrieved data as a message
    await update.message.reply_text(message, parse_mode = 'HTML')

#function to get data from event google sheet
def get_events_data():
    try:
        # Open the spreadsheet
        spreadsheet = client.open(MASTER_SPREADSHEET)
        worksheet = spreadsheet.get_worksheet(1)  # Assuming the first worksheet
        # Get the values from the worksheet
        values = worksheet.get_all_values()
        # get today's date
        current_date = datetime.now().date()        
        # Convert the values into a formatted message
        message = 'Upcoming Events:\n\n'
        for row in values[1:]:
            try:
                date_str = row[2]  # Adjust the index if it's in a different column    
                event_date = datetime.strptime(date_str, '%d/%m/%Y').date()
                date_obj = datetime.strptime(date_str, '%d/%m/%Y')
                formatted_date = date_obj.strftime('%d %b')
                
                if event_date >= current_date:
                    message += f'<b><i>{row[0]}</i></b>, {row[1]}, {formatted_date}, {row[3]}\n\n'
            except (ValueError, IndexError):
                # Handle the case where the date format is not as expected
                pass                
        return message
    except Exception as e:
        return f"Error retrieving data from Google Sheets: {str(e)}"

#error handling
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

# Command to update Engie's status (for authorized users)
async def update_engie_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global engie_status
    # Check if the user sending the command has the necessary permissions
    if update.message.from_user.username == 'engiewrong' and engie_status == False:
        engie_status = True  # Set Engie's status to "In the office"
        await update.message.reply_text('Your status has been updated to now be in office!')
    elif update.message.from_user.username == 'engiewrong' and engie_status == True:
        engie_status = False
        await update.message.reply_text('Your status has been updated to now be out of office!')
    else :
        await update.message.reply_text("You don't have permission to update Engie's status.")

#command to check if Engie is in
async def engie_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global engie_status
    if engie_status:
        await update.message.reply_text('Engie is in the office now!')
    else:
        await update.message.reply_text('Engie is not in the office now :(')

#main bot function
if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # visible commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('faq', faq_command))
    app.add_handler(CommandHandler('engie', engie_command))
    app.add_handler(CommandHandler('events', events_command))
    # other commands, but only accessible via other commands/ must be manually inputted, not on menu
    app.add_handler(CommandHandler('cancel_booking', cancel_command))
    app.add_handler(CommandHandler('updateengie', update_engie_status))
    app.add_error_handler(error)

    #faq-related commands
    app.add_handler(CommandHandler('funding', faq_funding_command))
    app.add_handler(CommandHandler('payments', faq_payments_command))
    app.add_handler(CommandHandler('people_to_contact', faq_people_to_contact_command))
    app.add_handler(CommandHandler('quickguide', faq_quickguide_command))
    app.add_handler(CommandHandler('cif', funding_cif_command))
    app.add_handler(CommandHandler('general', funding_general_command))
    app.add_handler(CommandHandler('travel', funding_travel_command))
    app.add_handler(CommandHandler('rfp', payment_rfp_command))
    app.add_handler(CommandHandler('copay', payment_copay_command))
    app.add_handler(CommandHandler('invoice', payment_invoice_command))
    app.add_handler(CommandHandler('pcard', payment_pcard_command))

    # Conversation handler for booking
    booking_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('booking', booking_command)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, booking_name)],
            BOOKING_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, booking_date)],
            ORGANISATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, booking_organisation)],
            LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, booking_location)],
            TIME_START: [MessageHandler(filters.TEXT & ~filters.COMMAND, booking_time_start)],
            TIME_END: [MessageHandler(filters.TEXT & ~filters.COMMAND, booking_time_end)],
        },
        fallbacks=[]
    )
    app.add_handler(booking_conversation_handler)
    # handler for messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, booking_conversation_handler))

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)