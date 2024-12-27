import telebot
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telebot import types
from dotenv import load_dotenv
import sqlite3
# Load environment variables from .env file
load_dotenv()

# Access the API key from the environment
API_KEY = os.getenv("API_KEY")
ADMIN_CHAT_ID  = os.getenv("ADMIN_CHAT_Id")

bot = telebot.TeleBot(API_KEY)
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
# Create the tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        fathers_name TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS receipts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        payment_receipt BLOB NOT NULL,
        file_type TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS receipts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        payment_receipt TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')
conn.commit()

# Load environment variables from .env file
load_dotenv()

# Access the API key from the environment
API_KEY = os.getenv("API_KEY")
ADMIN_CHAT_ID  = os.getenv("ADMIN_CHAT_Id")
# Temporary storage for user data
user_data = {}
pending_verifications = {}
# Log the chat ID of all users
# @bot.message_handler(func=lambda message: True)
# def log_chat_id(message):
#     print(f"Chat ID: {message.chat.id}")
    



# Start command
@bot.message_handler(commands=['start'])
def start_registration(message):
    print(f"Chat ID: {message.chat.id}")
    bot.reply_to(
        message,
        f"""👋 Hi {message.chat.first_name}! 
        Welcome to EasyGate! Your Gateway to Global Opportunities.

We specialize in:
 Scholarship and admissions
 Passport and visa applications
 Career and e-commerce services
 Travel consultancy
 Online courses and tests

Select a service to proceed:""",
        reply_markup=main_menu_markup()
    )

# Handle main menu options
@bot.message_handler(func=lambda msg: msg.text in ["Feedback", "About us", "Our services", "Continue to register" , "Already Registered?"])
def handle_menu_choice(message):
    if message.text == "Feedback":
        feedback_menu(message)
        # bot.reply_to(message, "Please provide your feedback. It will be sent to the admin.", reply_markup=main_menu_markup())
    elif message.text == "About us":
        about_us(message)
    elif message.text == "Our services":
        our_services(message)
    elif message.text == "Continue to register":
        registration_menu(message)
    elif message.text == "Already Registered?":
        Already_registered(message)

# Command handler for /help
@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.reply_to(message, """🆘 Help Menu:
    - Type '/start' to restart the bot
    - Type '/service' to view available services
    - Type '/contact' to contact us""")

# Command handler for /service
@bot.message_handler(commands=['service'])
def handle_service(message):
    bot.reply_to(message, """ Our Services:
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

# Command handler for /contact
@bot.message_handler(commands=['contact'])
def handle_contact(message):
    bot.reply_to(message, """📞 Contact Us:
    - Email: contact.easygate@gmail.com
    - Phone: +251964255107
    - Telegram: @easygate2""")
# Default handler for unrecognized inputs

# Feedback menu
def feedback_menu(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(
        KeyboardButton('Feedback using Google Form'),
        KeyboardButton('Feedback using Telegram Bot'),
        KeyboardButton('Main Menu')
    )
    bot.reply_to(message, "How would you like to provide feedback?", reply_markup=markup)

# About Us information
def about_us(message):
    bot.reply_to(message, """
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

# Our Services information
def our_services(message):
    bot.reply_to(message, """
 Our Services:
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
    1️⃣3️⃣ Other Services

📞 Contact us to learn more.
    """, reply_markup=main_menu_markup())

def Already_registered(message):
    bot.reply_to(message, """
    If you have already registered, please continue to make the payment to complete the registration process.
    """, reply_markup=payment_buttons())
# Registration menu
def registration_menu(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(
        KeyboardButton('Register on Google Form'),
        KeyboardButton('Register on Telegram Bot'),
        KeyboardButton('Register directly through Admin Contact'),
        KeyboardButton('Main Menu')
    )
    bot.reply_to(message, "Choose a registration option:", reply_markup=markup)

# Handle feedback options
@bot.message_handler(func=lambda msg: msg.text in ["Feedback using Google Form", "Feedback using Telegram Bot", "Main Menu"])
def handle_feedback_choice(message):
    if message.text == "Feedback using Google Form":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Submit Feedback", url="https://your-google-form-link.com"))
        bot.reply_to(message, "Submit feedback through the form:", reply_markup=markup)
    elif message.text == "Feedback using Telegram Bot":
        bot.reply_to(message, "Please provide your feedback. It will be sent to the admin.")
        bot.register_next_step_handler(message, collect_feedback)
        bot.reply_to(message, "Thank you for your feedback! It has been sent to the admin.", reply_markup=main_menu_markup())
    elif message.text == "Main Menu":
        bot.reply_to(message, "Returning to main menu...", reply_markup=main_menu_markup())

# Collect and send feedback to admin
def collect_feedback(message):
    feedback = message.text
    bot.reply_to(message, "Thank you for your feedback! It has been sent to the admin.")
    bot.send_message(ADMIN_CHAT_ID, f"📩 **New Feedback:**\n{feedback}")





# Handle registration options
@bot.message_handler(func=lambda msg: msg.text in ["Register on Google Form", "Register on Telegram Bot", "Register directly through Admin Contact"])
def handle_registration_option(message):
    if message.text == "Register on Google Form":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Register", url="https://your-google-form-link.com"))
        bot.reply_to(message, "Click below to register:", reply_markup=markup)
    elif message.text == "Register on Telegram Bot":
        bot.reply_to(message, "Let's start registration. Please enter your first name:")
        bot.register_next_step_handler(message, get_first_name)
    elif message.text == "Register directly through Admin Contact":
        bot.reply_to(message, "Contact the admin at @easygate2 for further steps.", reply_markup=start_registration())

# Registration process
def get_first_name(message):
    first_name = message.text.strip()
    if len(first_name) < 3:
        bot.reply_to(message, "First name must be at least 3 characters. Try again:")
        bot.register_next_step_handler(message, get_first_name)
        return
    user_data['first_name'] = first_name
    bot.reply_to(message, "Please enter your father's name:")
    bot.register_next_step_handler(message, get_fathers_name)
def get_fathers_name(message):
    fathers_name = message.text.strip()
    if len(fathers_name) < 3:
        bot.reply_to(message, "First name must be at least 3 characters. Try again:")
        bot.register_next_step_handler(message, get_fathers_name)
        return
    user_data['fathers_name'] = fathers_name
    bot.reply_to(message, "Please enter your phone number:")
    bot.register_next_step_handler(message, get_phone_number)
def get_phone_number(message):
    phone_number = message.text
    if len(phone_number) != 10 or not phone_number.isdigit():
        bot.send_message(message.chat.id, "Phone number must be exactly 10 digits. Please try again.")
        bot.register_next_step_handler(message, get_phone_number)
        return
    user_data['phone_number'] = phone_number
    bot.send_message(message.chat.id, "Please enter your email address (must contain @gmail.com):")
    bot.register_next_step_handler(message, get_email)

def get_email(message):
    email = message.text.strip()
    if not email.endswith('@gmail.com'):
        bot.reply_to(message, "Email must contain @gmail.com. Please try again:")
        bot.register_next_step_handler(message, get_email)
        return
    user_data['email'] = email
    bot.send_message(
        message.chat.id,
        "Registration complete. Now you have to make the payment of 1000 INR to complete the registration process. Please contact the admin at @easygate2 for payment details."
    )
    show_payment_buttons(message)

    # Check for missing data before sending to admin
    required_keys = ['first_name', 'fathers_name', 'phone_number', 'email']
    missing_keys = [key for key in required_keys if key not in user_data]
    if missing_keys:
        bot.reply_to(message, f"Missing information: {', '.join(missing_keys)}")
        return

    send_data_to_admin(message)

    # Save data to the database
    try:
        cursor.execute('''
            INSERT INTO users (first_name, fathers_name, phone_number, email)
            VALUES (?, ?, ?, ?)
        ''', (
            user_data[message.chat.id]['first_name'],
            user_data[message.chat.id]['fathers_name'],
            user_data[message.chat.id]['phone_number'],
            user_data[message.chat.id]['email']
        ))
        conn.commit()

        bot.send_message(message.chat.id, "Registration complete! Now, please send your payment receipt:")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")
        del user_data[message.chat.id]

def send_data_to_admin(message):
    admin_id = ADMIN_CHAT_ID  # Use the admin's Telegram ID from the constant
    registration_details = (
        f"New Registration:\n"
        f"First Name: {user_data['first_name']}\n"
        f"Father's Name: {user_data['fathers_name']}\n"
        f"Phone Number: {user_data['phone_number']}\n"
        f"Email: {user_data['email']}\n"
    )
    bot.send_message(admin_id, registration_details)

    # Store payment receipt in the database
    try:
        user_id = cursor.lastrowid  # Get the last inserted user ID
        receipt = message.text if message.content_type == 'text' else "Receipt attached"
        
        cursor.execute('''
            INSERT INTO receipts (user_id, payment_receipt)
            VALUES (?, ?)
        ''', (user_id, receipt))
        conn.commit()

        # Notify the admin
        user_info = user_data[message.chat.id]
        admin_message = f"""
        New Registration:
        First Name: {user_info['first_name']}
        Father's Name: {user_info['fathers_name']}
        Phone: {user_info['phone_number']}
        Email: {user_info['email']}
        Payment Receipt: {receipt}
        """
        bot.send_message(ADMIN_CHAT_ID, admin_message)
        bot.send_message(message.chat.id, "Your payment receipt has been sent to the admin.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

    # Clear user data
    del user_data[message.chat.id]
# Main menu markup
def main_menu_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = KeyboardButton('Feedback')
    btn2 = KeyboardButton('About us')
    btn3 = KeyboardButton('Our services')
    btn4 = KeyboardButton('Continue to register')
    btn5 = KeyboardButton('Already Registered?')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup

def show_payment_buttons(message):
    # Create buttons
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    make_payment_button = KeyboardButton("Make Payment")
    cancel_registration_button = KeyboardButton("Cancel Registration")
    markup.add(make_payment_button, cancel_registration_button)

    # Send the buttons to the user
    bot.send_message(message.chat.id, "Please choose an option:", reply_markup=markup)
# Handle user response to the buttons
@bot.message_handler(func=lambda message: message.text in ["Make Payment", "Cancel Registration"])
def handle_payment_choice(message):
    if message.text == "Make Payment":
        bot.reply_to(message, """Thank you for choosing to make the payment. Please contact @easygate2 for further instructions.
                     or you can pay directly through the following payment methods:""", reply_markup=payment_buttons())
    elif message.text == "Cancel Registration":
        bot.reply_to(message, "Your registration has been canceled. If you wish to register again, please start the process from the beginning.", reply_markup=main_menu_markup())
def payment_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Bank Transfer')
    btn2 = types.KeyboardButton('Telebirr')
    btn3 = types.KeyboardButton('Already Paid? (Submit receipt)')
    btn4 = types.KeyboardButton('Main Menu')
    markup.add(btn1, btn2, btn3, btn4)
    return markup

@bot.message_handler(func=lambda message: message.text in ['Bank Transfer', 'Telbirr', 'PayPal', 'Already Paid? (Submit receipt)', 'Choose Different Payment Method'])
def handle_payment_methods(message):
    if message.text == 'Bank Transfer':
        bot.reply_to(message, """Please make the payment to the following account:
Bank Name: XYZ Bank
Account Number: 1234567890
SWIFT/BIC: ABCDEF123

Once you have made the payment, please send us the receipt (PDF or image) on this username @easygate2 or you can send it directly through the bot by clicking the Already Paid button.""")
        bot.reply_to(message, "Do you want to choose a different payment method or confirm payment? Select an option.", reply_markup=payment_buttons())

    elif message.text == 'Telebirr':
        bot.reply_to(message, """Please use the following Telebirr number to make the payment:
Telebirr Number: 0912345678
                     
Once you have made the payment, please send us the receipt (PDF or image)  on this username @easygate2 or you can send it directly through the bot by clicking the Already Paid button.""")
        bot.reply_to(message, "Do you want to choose a different payment method or confirm payment? Select an option.", reply_markup=payment_buttons())


    elif message.text == 'Already Paid? (Submit receipt)':
        bot.reply_to(message, """Please send your payment receipt (PDF or image) to confirm your payment.""")
        # Save the user receipt or process further to verify the payment with the admin
        bot.register_next_step_handler(message, process_receipt)

    elif message.text == 'Choose Different Payment Method':
        bot.reply_to(message, """Payment options:
""", reply_markup=payment_buttons())
@bot.message_handler(func=lambda message: message.text == "Telebirr")
def handle_telebirr(message):
    bot.reply_to(message, """Please use the following Telebirr number to make the payment:
Telebirr Number: 0912345678
                     
Once you have made the payment, please send us the receipt (PDF or image) on this username @easygate2 or you can send it directly through the bot by clicking the 'Already Paid' button.""")
    bot.reply_to(message, "Do you want to choose a different payment method or confirm payment? Select an option.", reply_markup=payment_buttons())

# Handle the receipt submission and forward to admin
@bot.message_handler(content_types=['document', 'photo'])
def process_receipt(message):
    user_id = message.chat.id
    user_first_name = message.chat.first_name

    if message.document:
        file_name = message.document.file_name
        file_extension = file_name.split('.')[-1].lower()  # Extract file extension
        
        # Check if the document is a PDF
        if file_extension == 'pdf':
            receipt_file = message.document.file_id
            file_type = 'PDF'
            bot.send_document(ADMIN_CHAT_ID, receipt_file)
        else:
            bot.reply_to(message, "Please send a valid receipt in PDF format.")
            return

    elif message.photo:
        receipt_file = message.photo[-1].file_id  # Get the highest quality photo
        file_type = 'Photo'
        bot.send_photo(ADMIN_CHAT_ID, receipt_file)

    else:
        bot.reply_to(message, "Please send a valid receipt in PDF or image format.")
        return

    # Inform the admin about the receipt submission
    pending_verifications[user_id] = {'file_id': receipt_file, 'file_type': file_type, 'user_name': user_first_name}
    bot.reply_to(message, "Your payment receipt has been sent for verification. The admin will confirm your payment shortly.")
    bot.send_message(ADMIN_CHAT_ID, f"📩 New Payment Receipt from {user_first_name} ({user_id}):")

    # Send Inline buttons to Admin for verification
    markup = types.InlineKeyboardMarkup()
    verify_button = types.InlineKeyboardButton("✅ Verify User", callback_data=f"verify_{user_id}")
    invalid_button = types.InlineKeyboardButton("❌ Invalid Payment", callback_data=f"invalid_{user_id}")
    markup.add(verify_button, invalid_button)
    bot.send_message(ADMIN_CHAT_ID, "Please verify the payment from the user:", reply_markup=markup)


# Handle admin verification actions
@bot.callback_query_handler(func=lambda call: call.data.startswith('verify_') or call.data.startswith('invalid_'))
def handle_admin_response(call):
    user_id = int(call.data.split('_')[1])

    if call.data.startswith('verify_'):
        if user_id in pending_verifications:
            user_data[user_id] = pending_verifications.pop(user_id)
            bot.send_message(user_id, "✅ Your payment has been verified! you will hear from us once we have processed your registration and started giving services.")
        else:
            bot.send_message(ADMIN_CHAT_ID, "The user ID is not in the pending verifications.")

    elif call.data.startswith('invalid_'):
        if user_id in pending_verifications:
            pending_verifications.pop(user_id)
            bot.send_message(user_id, "❌ Your payment could not be verified. Please contact support.")
            bot.send_message(ADMIN_CHAT_ID, f"Payment invalid for {user_id}. User has been notified.")
        else:
            bot.send_message(ADMIN_CHAT_ID, "The user ID is not in the pending verifications.")
    # Store payment receipt as BLOB in the database
    def store_payment_receipt(message):
        try:
            file_id = message.document.file_id if message.content_type == 'document' else message.photo[-1].file_id
            file_info = bot.get_file(file_id)
            file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"
    
            # Download the file
            downloaded_file = bot.download_file(file_info.file_path)
            
            # Determine the file type (image/pdf)
            file_type = 'image' if message.content_type == 'photo' else 'pdf'
            
            # Insert the receipt into the database as a BLOB
            cursor.execute('''
                INSERT INTO receipts (user_id, payment_receipt, file_type)
                VALUES (?, ?, ?)
            ''', (message.chat.id, sqlite3.Binary(downloaded_file), file_type))
            conn.commit()
    
            # Notify the admin
            user_info = user_data[message.chat.id]
            admin_message = f"""
            New Registration:
            First Name: {user_info['first_name']}
            Father's Name: {user_info['fathers_name']}
            Phone: {user_info['phone_number']}
            Email: {user_info['email']}
            Payment Receipt: {file_url}
            """
            bot.send_message(ADMIN_ID, admin_message)
            bot.send_message(message.chat.id, "Your payment receipt has been sent to the admin.")
        except Exception as e:
            bot.send_message(message.chat.id, f"Error: {e}")
    
        # Clear user data
        del user_data[message.chat.id]

    bot.answer_callback_query(call.id)  # Close the callback button
    def handle_service_selection(message):
        user_id = message.chat.id
        service_selected = message.text
    
        # Debug log
        print(f"User {user_id} selected the service: {service_selected}")
    
        if user_id in user_data:
            receipt_details = user_data[user_id]
            file_id = receipt_details['file_id']
            file_type = receipt_details['file_type']
    
            # Forward the receipt and service selection to the admin
            bot.send_message(ADMIN_CHAT_ID, f"📩 Verified Payment Receipt from {receipt_details['user_name']} ({user_id}):\n\nService: {service_selected}")
            if file_type == 'Document':
                bot.send_document(ADMIN_CHAT_ID, file_id)
            elif file_type == 'Photo':
                bot.send_photo(ADMIN_CHAT_ID, file_id)
# Save the file to a directory on the server
def save_file_to_directory(file_id, file_type, downloaded_file):
    file_path = f"receipts/{file_id}.{file_type}"  # Example: receipts/file_id.image
    with open(file_path, 'wb') as f:
        f.write(downloaded_file)
    return file_path

# Save the file path in the database
def store_payment_receipt(message, file_id, file_type, downloaded_file):
    file_path = save_file_to_directory(file_id, file_type, downloaded_file)
    cursor.execute('''
        INSERT INTO receipts (user_id, payment_receipt, file_type)
        VALUES (?, ?, ?)
    ''', (message.chat.id, file_path, file_type))
    conn.commit()

# Example usage (ensure file_id, file_type, and downloaded_file are defined)
# store_payment_receipt(message, file_id, file_type, downloaded_file)

print("Bot is running...")
bot.polling()
