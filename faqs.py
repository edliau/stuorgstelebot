from telegram import Update
from telegram.ext import ContextTypes

# Define FAQ functions

async def faq_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''Please choose an FAQ category by sending one of the following commands:

/funding - Available funds for application
/payments - Payment methods and information
/people_to_contact - Who should you contact for what matters?
/quickguide - View the Stuorgs funding guidelines
                          
''')

async def faq_funding_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('''Please select which fund you're interested in:
                                        
/cif - Community Initiative Funding
/travel - StuOrg Travel Funding
/general - Funding for General StuOrg Activities 
''')


async def funding_cif_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        reply = '''<u><b>What is Community Initiative Funding (CIF?)</b></u>

CIF is available for students who are not affiliated with any particular club or organisation to plan a meaningful cultural, social, and/or academic event for the Yale-NUS community. For more information, see tiny.cc/ynccif 


<u><b>How can I apply for Community Initiative Funding (CIF)? </b></u>

You should discuss your idea with SAO before applying. For contacts and the application, see tiny.cc/ynccif 
'''
        await update.message.reply_text(reply, parse_mode = 'HTML')

async def funding_travel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        reply = '''<u><b>What is Student Organisation Travel Funding? </b></u>
This fund provides an opportunity for registered student organisations to organise relevant overseas learning experiences. Funding is limited to allow support for a variety of requests. For more information, see tiny.cc/stuorgtravel


<u><b>When are the application deadlines for StuOrg Travel Funding? </b></u>

They have now passed :(
'''
        await update.message.reply_text(reply, parse_mode = 'HTML')

async def funding_general_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        reply = '''<u><b>How much can I spend on StuOrg expenses and what can I spend on?  </b></u>

You can find a quick guide to finances and spending limits using /quickguide

The full funding guidelines are available here: https://yale-nus.campuslabs.com/engage/organization/studentorganizations/documents/view/1790709  


<u><b>How much can I spend for food/refreshments? </b></u>

Maximums for each Yale-NUS student: 
- Breakfast/ Snacks/ Tea: $10/ pax 
- Lunch: $15/ pax 
- Dinner $20/ pax 

Also:
- Weekly/Recurring meetings are not eligible for food funding. 
- Welcome tea: Up to $50/ semester 
- Speaker events (open to all students): Up to $100 

More information is available at /financequickguide


<u><b>How much can I spend on internal appreciation events?  </b></u>

Up to $400 per AY, max $15 per Yale-NUS student. Internal appreciation events should be for all StuOrg members; exco-appreciation events will not be funded. 


<u><b>What if my event involves alcohol, needs funding for local transport, in outside of Singapore, or requires a co-pay?  </b></u>

Email e.ngie@nus.edu.sg for approval. If you event involves alcohol, please get in contact with Ashley at ashley.yong@yale-nus.edu.sg.


<u><b>What is the semester deadline for claiming StuOrg expenses?  </b></u>

Semester 1: 1 Dec 
Semester 2: 2 May
Summer: 15 Aug 

Please note that expenses submitted after deadline may not be reimbursed. 


<u><b>How can I print materials for my StuOrg? </b></u>

Email e.ngie@nus.edu.sg with a PDF and the number of copies needed. You can pick them up from SAO when they have been printed. 
'''
        await update.message.reply_text(reply, parse_mode = 'HTML')

async def faq_payments_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('''Please select which payment method you have questions about:
                                        
/rfp - Request for Payment / Reimbursement
/invoice - Invoiced Payments
/pcard - Payment using Corporate Purchase Card
/copay - Copayment for Programmes / Events 
                                        
If your question is unanswered or you want to find out more, you can check out tiny.cc/stuorgpayments 
''')

async def payment_rfp_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        reply = '''<u><b>How do I request reimbursement for StuOrg expenses (Request for Payment RFP)? </b></u>

Only approved expenses will be reimbursed. You must submit within 30 days of the purchase or before the semester claims deadline, whichever comes first. 

- Add event on Halcyon Hub calendar. 
- Make a purchase request on Halcyon Hub. 
- Submit the RFP (one PDF document) to the YNC StuOrgs email at studentorgs@yale-nus.edu.sg 
- Once approved and processed, you can expect reimbursement in approximately 30 days. 
                                        
The RFP should be one PDF document with the RFP form as the first page and all receipts attached. Receipts must be legible and itemized. You can find the RFP form at tiny.cc/RFP  
'''
        await update.message.reply_text(reply, parse_mode = 'HTML')

async def payment_invoice_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply = '''<u><b>How can StuOrgs pay invoices?</b></u>

Vendors can bill the student organisation through an invoice. NUS has a standard payment term of 30-days credit for all vendors. 

(1) Invoice(s) must be made attention to: 
National University of Singapore 
Yale-NUS College 
Student's address in residential college 
Attn: Engie Wong, Student Life

(2) E-invoices must say “This is an e-invoice, no original copy will be sent/This is a computer generated invoice, no signature is required” 

You should:
i. Add the event on Halcyon Hub calendar. 
ii. Make a purchase request on Halcyon Hub. 
iii. Check that the invoice meets all the requirements above.
iv. The vendor should send the email directly to ofnap@nus.edu.sg for processing.

If your planned invoice amount exceeds S$1,000, contact e.ngie@nus.edu.sg for assistance at least 1 month in advance. 


<u><b>How can I register a new vendor?</b></u>

Any new vendor who has not worked with Yale-NUS College or NUS previously will need to fill in the Vendor Creation Form.  

You can find the required forms here: https://yale-nus.my.site.com/portal/s/page-details?pageId=a1l0K00000AN5SxQAL  
'''
    await update.message.reply_text(reply, parse_mode = 'HTML')

async def payment_pcard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        reply = '''<u><b>How can I use the Corporate Purchasing Card (PCard)? </b></u>

Online purchases can be made using a corporate card and is subject to the availability of the card's credit limit. 

You should: 
i. Add the event on Halcyon Hub calendar. 
ii. Make a purchase request on Halcyon Hub. 
iii. After using the card, immediately forward the receipt to the card holder (e.g., Engie).  

Email e.ngie@nus.edu.sg to make an appointment to use the card. 

If your planned payment amount exceeds S$1,000, contact e.ngie@nus.edu.sg for assistance at least 1 month in advance. 

Please note that all accounts used to make P-Card purchases should have the user of the P-Card as the listed name of the account owner.
'''
        await update.message.reply_text(reply, parse_mode = 'HTML')

async def payment_copay_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        reply = '''<u><b>How do co-pays work? </b></u>

Standard co-pay: student pays 40%, StuOrg pays 60% 
- Required for most external events & on-campus events with high material cost. 
- Only current Yale-NUS students (including exchange students) are eligible.  
- NUSC, NUS students, alumni, etc. must pay full cost. 

Log the amount withdrawn from StuOrg account (60%) on Halcyon Hub and indicate co-pay details in notes. You should email e.ngie@nus.edu.sg for pre-approval. 


<u><b>Can students get financial assistance with co-pays? </b></u>

Students with genuine demonstrated need may receive co-pays from Student Services. Students should email studenthelp@yale-nus.edu.sg.  

Co-pay financial aid is confidential: students should make the full co-pay payment upfront and will be reimbursed by SAO to their bank account on EduRec. 
'''
        await update.message.reply_text(reply, parse_mode = 'HTML')

async def faq_people_to_contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        reply = '''<b>Email Engie (e.ngie@nus.edu.sg) for: </b>                                
- Event/ funding approvals 
- Payments/ claims (e.g., invoices, RFP, PCard use) 
- Community Initiative Funding (CIF) and StuOrg Travel Funding 
- Leadership events/ initiatives 
                                    
<b>Email StuOrgs (studentorgs@yale-nus.edu.sg) for: </b>
- General enquiries 
- StuOrg policies 
- Room booking requests 

<b>Email Shirley (shirley.thia@yale-nus.edu.sg) for: </b>
- CATS funding                                         

<b>Who should I reach out to for help with Community Initiative Funding? </b>
- For Wellness Initiatives, email wellness@yale-nus.edu.sg 
- For Intercultural Engagement, email annette.wu@yale-nus.edu.sg 
- For StuOrg & Leadership Initiatives, email e.ngie@nus.edu.sg 
'''
        await update.message.reply_text(reply, parse_mode = 'HTML')

async def faq_quickguide_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        image_path_1 = 'C:/Users/edwar/Documents/GitHub/stuorgstelebot/quickguide1.jpg'
        image_path_2 = 'C:/Users/edwar/Documents/GitHub/stuorgstelebot/quickguide2.jpg'
        with open(image_path_1, 'rb') as photo1, open(image_path_2, 'rb') as photo2:
            await update.message.reply_photo(photo=photo1)
            await update.message.reply_photo(photo=photo2)