import configparser
from telethon import TelegramClient, events
from telethon import Button
import MySQLdb
from datetime import datetime
from telethon.tl.custom import Button as KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

# Load Configuration
config = configparser.ConfigParser()
config.read('config.ini')

API_ID = config.get('default', 'api_id')
API_HASH = config.get('default', 'api_hash')
BOT_TOKEN = config.get('default', 'bot_token')
HOSTNAME = config.get('default', 'hostname')
USERNAME = config.get('default', 'username')
PASSWORD = config.get('default', 'password')
DATABASE = config.get('default', 'database')
ADMIN_ID = config.get('default', 'admin_id')

# Initialize Telegram Client
client = TelegramClient('session/Bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Function to get DB connection
def get_db_connection():
    return MySQLdb.connect(host=HOSTNAME, user=USERNAME, passwd=PASSWORD, db=DATABASE)

# Create Table if Not Exists (Moved outside for better structure)
def create_table():
    conn = get_db_connection()
    crsr = conn.cursor()
    crsr.execute('''CREATE TABLE IF NOT EXISTS registrations (
        id INT PRIMARY KEY AUTO_INCREMENT,
        first_name VARCHAR(100),
        fathers_name VARCHAR(100),
        phone_number VARCHAR(15),
        email VARCHAR(100),
        payment_receipt TEXT,
        submission_date DATETIME
    );''')
    conn.commit()
    conn.close()

create_table()  # Call function to create table when the bot starts

# State tracking for user registration
user_states = {}

# Start Command
@client.on(events.NewMessage(pattern="(?i)/start"))
async def start(event):
    sender = await event.get_sender()
    SENDER_ID = sender.id

    # Create the main menu with 4 buttons (without inline)
    buttons = [
        Button.text("Feedback"),
        Button.text("About Us"),
        Button.text("Our Services"),
        Button.text("Continue to Register")
    ]
    
    # Send the main menu
    await event.reply(f"""👋 Hi {sender.first_name}! 
        Welcome to EasyGate! Your Gateway to Global Opportunities.

We specialize in:
 Scholarship and admissions
 Passport and visa applications
 Career and e-commerce services
 Travel consultancy
 Online courses and tests

Select a service to proceed:""", buttons=buttons)

# Function to create main menu markup
def main_menu_markup():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton('Feedback')],
            [KeyboardButton('About Us')],
            [KeyboardButton('Our Services')],
            [KeyboardButton('Continue to Register')],
            [KeyboardButton('Already Registered?')]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

# Function to handle feedback menu
async def feedback_menu(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(
        KeyboardButton('Feedback using Google Form'),
        KeyboardButton('Feedback using Telegram Bot'),
        KeyboardButton('Main Menu')
    )
    await message.respond("How would you like to provide feedback?", buttons=markup)


# Function to handle about us menu
async def about_us(message):
    await message.respond("""
Welcome to EasyGate! 

    We are a team of young Ethiopians, currently studying and working across the globe. Our mission is to simplify the process of accessing international education and career opportunities by reducing costs and eliminating the need for expensive intermediaries. 

    We aim to make services that can be accessed easily from home, such as visa applications, scholarship opportunities, and career guidance, more affordable and accessible to you.

    At EasyGate, we're dedicated to guiding you through every step of your global journey, whether it's education, work, or travel. Let us help you unlock your future, right from the comfort of your home!.
    Stay connected with us on our social media platforms to explore our services further:

     Telegram: [@easygate](https://t.me/easygate)
     WhatsApp: [0964255107](https://wa.me/0964255107)
     Email: contact.easygate@gmail.com

    Feel free to contact us via any of the platforms above for more information or to get started! 
    """, reply_markup=main_menu_markup())


# Function to handle our services menu
async def our_services(message):
    await message.respond(""" Our Services:
    1️⃣ Embassy Interview Assistance
    2️⃣ Document Review
    3️⃣ Travel Advice
    4️⃣ Visa Application Assistance
    5️⃣ Scholarship Opportunities
    6️⃣ English Proficiency Test Preparation
    7️⃣ Passport Services
    8️⃣ E-Visa Applications
    9️⃣ International Payments
    🔟 International Career Opportunities
    1️⃣1️⃣ Recommend Educational Travel Consultancies
    1️⃣2️⃣ Assistance with Any Embassy Interview Practice
    1️⃣3️⃣ Other Services""")

# Function to handle registration menu
async def registration_menu(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(
        KeyboardButton('Register on Google Form'),
        KeyboardButton('Register on Telegram Bot'),
        KeyboardButton('Register directly through Admin Contact'),
        KeyboardButton('Main Menu')
    )
    await message.respond("Choose a registration option:", buttons=markup)

# Handle feedback options
@client.on(events.NewMessage(pattern="Feedback using Google Form|Feedback using Telegram Bot|Main Menu"))
async def handle_feedback_choice(event):
    message = event.message
    if message.text == "Feedback using Google Form":
        markup = KeyboardButton()
        markup.add(KeyboardButton("Submit Feedback", url="https://your-google-form-link.com"))
        await message.respond("Submit feedback through the form:", buttons=markup)
    elif message.text == "Feedback using Telegram Bot":
        await message.respond("Please provide your feedback. It will be sent to the admin.")
        await message.respond("Thank you for your feedback! It has been sent to the admin.", buttons=main_menu_markup())
    elif message.text == "Main Menu":
        await message.respond("Returning to main menu...", buttons=main_menu_markup())

# Function to handle already registered menu
async def Already_registered(message):
    await message.respond(message, """
    If you have already registered, please continue to make the payment to complete the registration process.
    """, reply_markup=payment_buttons())
# Handle registration options
@client.on(events.NewMessage(pattern="Register on Google Form|Register on Telegram Bot|Register directly through Admin Contact"))
async def handle_registration_option(event):
    sender = await event.get_sender()
    SENDER_ID = sender.id
    if event.message.text == "Register on Google Form":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Register", url="https://your-google-form-link.com"))
        await event.message.respond("Click below to register:", reply_markup=markup)
        user_states[SENDER_ID] = "awaiting_first_name"
        await event.respond("Please enter your first name:")
        await event.message.respond("Let's start registration. Please enter your first name:")
        user_states[SENDER_ID] = "awaiting_first_name"
        await event.message.respond("Please enter your first name:")
    elif event.message.text == "Register directly through Admin Contact":
        await event.message.respond("Contact the admin at @easygate2 for further steps.", reply_markup=start_registration())

# Handle button clicks
@client.on(events.NewMessage)
async def handle_menu_choice(event):
    sender = await event.get_sender()
    SENDER_ID = sender.id

    # Handle menu choices
    if event.message.text == "Feedback":
        feedback_menu(event.message)
        # bot.reply_to(event.message, "Please provide your feedback. It will be sent to the admin.", reply_markup=main_menu_markup())
    elif event.message.text == "About us":
        about_us(event.message)
    elif event.message.text == "Our services":
        our_services(event.message)
    elif event.message.text == "Continue to register":
        registration_menu(event.message)
    elif event.message.text == "Already Registered?":
        Already_registered(event.message)
def payment_buttons():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton('Pay Now')],
            [KeyboardButton('Main Menu')]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

async def Already_registered(message):
    await message.respond("""
    If you have already registered, please continue to make the payment to complete the registration process.
    """, buttons=payment_buttons())
# Capture Registration Details
@client.on(events.NewMessage)
async def capture_details(event):
    sender = await event.get_sender()
    SENDER_ID = sender.id

    if user_states.get(SENDER_ID) == "awaiting_details":
        try:
            # If the message contains a file (payment receipt)
            if event.message.file:
                # Download the file to store the file path
                file_path = await event.message.download_media()
                payment_receipt = file_path
            else:
                # Otherwise, extract user details from the message text
                details = event.message.text.split(",")
                if len(details) != 4:
                    raise ValueError("Invalid format. Ensure all details are separated by commas.")

                first_name = details[0].strip()
                fathers_name = details[1].strip()
                phone_number = details[2].strip()
                email = details[3].strip()
                submission_date = datetime.now()

                conn = get_db_connection()
                crsr = conn.cursor()
                sql_command = (
                    "INSERT INTO registrations (first_name, fathers_name, phone_number, email, payment_receipt, submission_date) "
                    "VALUES (%s, %s, %s, %s, %s, %s);"
                )
                params = (first_name, fathers_name, phone_number, email, payment_receipt, submission_date)
                crsr.execute(sql_command, params)
                conn.commit()
                conn.close()

                await event.reply("Your details have been submitted successfully!")
                user_states.pop(SENDER_ID, None)

                # Notify Admin
                admin_message = (
                    f"<b>New Registration:</b>\n"
                    f"First Name: {first_name}\n"
                    f"Father's Name: {fathers_name}\n"
                    f"Phone Number: {phone_number}\n"
                    f"Email: {email}\n"
                    f"Payment Receipt: {payment_receipt}\n"
                    f"Submission Date: {submission_date}"
                )
                try:
                    await client.send_message(int(ADMIN_ID), admin_message, parse_mode='html')
                except Exception as admin_error:
                    print(f"Error notifying admin: {admin_error}")

        except MySQLdb.Error as db_error:
            await event.reply(f"Database error occurred: {db_error}")
            user_states.pop(SENDER_ID, None)

        except Exception as e:
            await event.reply(f"Error: {e}\nPlease try again.")
            user_states.pop(SENDER_ID, None)

if __name__ == '__main__':
    print("Bot is running...")
    client.run_until_disconnected()
