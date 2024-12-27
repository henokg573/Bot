from flask import Flask, request
# import telebot
# from telegram import Bot, Update
# from telebot import types
# from telegram.ext import CommandHandler, Updater, CallbackContext, Application
import os
# # from telegram.ext import Dispatcher
# from telebot.types import ForceReply
# import telegram
# from telebot import types

API_KEY = "7759515826:AAFKPIz6SVVBT8Owvk9cVW4yema2alXjtII"
# ADMIN_CHAT_ID = "793034140"
# API_KEY = os.getenv("API_KEY")
# ADMIN_CHAT_ID  = os.getenv("ADMIN_CHAT_Id"")
bot = telebot.TeleBot(API_KEY)




app = Flask(__name__)

WEBHOOK_HOST = 'https://registration-bot.onrender.com'
WEBHOOK_PATH = f'webhook/{API_KEY}'
DB_URL = 'postgresql://easygate_db_user:EezQHIycha07Xfq6DVHS7QLbt7D0BiLo@dpg-ctn8ont2ng1s73bi6ir0-a.oregon-postgres.render.com/easygate_db'
WEBHOOK_URL = f'{WEBHOOK_HOST}/{WEBHOOK_PATH}'
WEBAPP_HOST = '0.0.0.0'


# Set Webhook
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)


@app.route(f'/{WEBHOOK_PATH}', methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200
if __name__ == "__main__":
    app.run(host=WEBAPP_HOST, port=5000)



import email
from flask import Flask, request
import telebot
from telegram import Bot
from telegram import Update
from telebot import types
from telebot import types
from telegram.ext import CommandHandler, Updater, CallbackContext, Application
import os
# from telegram.ext import Dispatcher
from telebot.types import ForceReply
import telegram
from telebot import types
# from keep_alive import keep_alive
# keep_alive()



# Replace with your API key
API_KEY = '7759515826:AAFKPIz6SVVBT8Owvk9cVW4yema2alXjtII'
bot = telebot.TeleBot(API_KEY)

# Admin's chat ID (replace with the actual admin chat ID)
ADMIN_CHAT_ID = '793034140'  # You should use your actual chat ID here

# bot = telebot.TeleBot(token=os.environ.get("API_KEY"))

app = Flask(__name__)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    print(f"Received /start from {message.chat.id}")  # Debugging

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('About Us')
    btn2 = types.KeyboardButton('Our Services')
    btn3 = types.KeyboardButton('Continue to  Register')
    btn4 = types.KeyboardButton('Feedback')
    markup.add(btn1, btn2, btn3, btn4)
    # markup.add(btn12, btn13, btn14, btn15)


    bot.reply_to(
        message,
        f"""👋 Hi {message.chat.first_name}! 
        👋 Welcome to EasyGate!, 
        welcome to Your 
                        \t\t\t\t\tGateway to Global Opportunities.
                        \t\t\t\t\tSimplifying Your Path to Success.
                        \t\t\t\t\tFrom Dreams to Destinations.
                        \t\t\t\t\tOpen Doors, Easy Journeys.
We’re thrilled to have you here! 🎉

At EasyGate, we specialize in making your goals more accessible, whether it’s education, travel, or career growth. Here's what we can help you with:
             Scholarship and admission opportunities
             Passport and visa applications
             International career and e-commerce services
             Embassy appointments and travel consultancy
             Online courses and proficiency tests

Let us guide you every step of the way! Simply explore the options below and get started on your journey with us.

Feel free to reach out if you have any questions—we’re here to make things easy for you!
        \n\nwe are currently on registration period and you can continue to register or see our services. 
        if you need help, please typle /help
        if you need to contact us, use this commant /contact
        if you need guide how to use our services, we have prepared tour guide her /guide
        """,
        reply_markup=markup,    
    )

    
    # Guide Command
@bot.message_handler(commands=['guide'])
@bot.message_handler(func=lambda message: message.text == "Guide")
def send_guide(message):
    bot.reply_to(
        message,
        """ Guide to EasyGate registration bot:
1️⃣ See our services, get to know our bot, contact us and learn more.
2️⃣ Follow instructions to register.
3️⃣ Use 'Payment' to handle transactions securely.

Explore and simplify your journey with EasyGate! 🌟""", reply_markup = main_menu_markup()
    )

 # Help Command
@bot.message_handler(commands=['help'])
@bot.message_handler(func=lambda message: message.text == "Help")
def send_guide(message):
    bot.reply_to(
        message,
        """ to use this service, please hit /start
        for guide, use this /guide
        to  contact us, use this /contact
""", reply_markup = main_menu_markup()
    )
    # Contact Command
@bot.message_handler(commands=['contact'])
@bot.message_handler(func=lambda message: message.text == "Contact")
def send_guide(message):
    bot.reply_to(
        message,
        """Contact us via:
        @easygate2
        0964255107
        contact.easygate@gmail.com
        for help, use this /help
        to start using this service, use this /start""",reply_markup = main_menu_markup())


@bot.message_handler(func=lambda message: True)
def handle_options(message):
    print(f"Message received: {message.text}")  # Debugging
    service_selected = message.text  # Define service_selected
    if message.text == 'About Us':
        bot.reply_to(
        message,
        """Welcome to EasyGate! 

    We are a team of young Ethiopians, currently studying and working across the globe. Our mission is to simplify the process of accessing international education and career opportunities by reducing costs and eliminating the need for expensive intermediaries. 

    We aim to make services that can be accessed easily from home, such as visa applications, scholarship opportunities, and career guidance, more affordable and accessible to you.

    At EasyGate, we're dedicated to guiding you through every step of your global journey, whether it's education, work, or travel. Let us help you unlock your future, right from the comfort of your home!.
    Stay connected with us on our social media platforms to explore our services further:

     Telegram: [@easygate](https://t.me/easygate)
     WhatsApp: [0964255107](https://wa.me/0964255107)
     Email: contact.easygate@gmail.com

    Feel free to contact us via any of the platforms above for more information or to get started! 
    """, reply_markup = main_menu_markup())
    elif message.text == "Our Services":
        bot.reply_to(
        message,
        """ Our Services:
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

📞 Contact us to learn more.""", reply_markup = main_menu_markup())
    elif message.text == "Continue to  Register":
        bot.reply_to(
        message,
            """To register, we offer three ways, you can register through
            our google form link, you can contact us and register, and you can register through our bot.
            please choose one of the options below to continue.""", reply_markup = register_markup())
    elif message.text == "Feedback":
        bot.reply_to(
        message,
            """We value your feedback!. you can directly send your feedbacks to Admin
            or you can send your feedbacks using our Google form link: please choose what suits you well"""
            , reply_markup = feedback_markup())
    elif message.text == "Already Registered?":
        bot.reply_to(
        message,
            """If you have already registered, please continue to the payment method""", reply_markup = payment_markup())
    elif message.text == "Google Form":
        bot.reply_to(
        message,
            """Please fill out the Google form to register: [Google Form](https://forms.gle/7oZ6z5f4v5ZnUv8dA)""", reply_markup = register_markup())
    elif message.text == "Directly on Telegram":
        bot.reply_to(
            message,
                """please use this username
                @easygate2 or 0964255107 to register""", reply_markup = register_markup())
    elif message.text == "Bot Registration":
        start_registration(message)
    elif message.text == "Google Form feedback":
        bot.reply_to(
            message,
                """Please fill out the Google form to provide feedback: [Google Form](https://forms.gle/7oZ6z5f4v5ZnUv8dA)""", reply_markup = feedback_markup())
    elif message.text == "Directly to Admin":
        bot.reply_to(
            message,
                """Please send your feedback directly to the admin.""", reply_markup = feedback_markup())
    elif message.text == "Bank Transfer":
        bot.reply_to(
            message,
                """Please transfer the payment to the following bank account:
                Bank Name: CBE
                Account Number: 1000000000000
                Account Name: EasyGate
                Please provide the receipt after payment.""", reply_markup = payment_markup())
    elif message.text == "Telebirr":
        bot.reply_to(
            message,
                """Please transfer the payment to the following Telebirr account:
                Telebirr Number: 0964255107
                Account Name: EasyGate
                Please provide the receipt after payment.""", reply_markup = payment_markup())
    elif message.text == "PayPal":
        bot.reply_to(
            message,
                """Please transfer the payment to the following PayPal account:
                PayPal Email: contact.easygate@gmail.com""", reply_markup = payment_markup())
    elif message.text == "Already Paid? (Submit receipt)": 
        bot.reply_to(
            message,
                """Please submit the receipt after payment.""", reply_markup = payment_markup())
    elif message.text == "Choose Different Payment Method":
        bot.reply_to(
            message,
                """Please choose a different payment method.""", reply_markup = payment_markup())
    elif message.text == "main menu":
        bot.reply_to(
            message,
                """Welcome to EasyGate!
                We are a team of young Ethiopians, currently studying and working across the globe. Our mission is to simplify the process of accessing international education and career opportunities by reducing costs and eliminating the need for expensive intermediaries.   
                We aim to make services that can be accessed easily from home, such as visa applications, scholarship opportunities, and career guidance, more affordable and accessible to you.
                At EasyGate, we're dedicated to guiding you through every step of your global journey, whether it's education, work, or travel. Let us help you unlock your future, right from the comfort of your home!.
                Stay connected with us on our social media platforms to explore our services further:
                Telegram: [@easygate](https://t.me/easygate)
                WhatsApp: [0964255107](https://wa.me/0964255107)
                Email: contact.easygate@gmail.com
                Feel free to contact us via any of the platforms above for more information or to get started!""", reply_markup = main_menu_markup())
    else:
        bot.reply_to(
                message,
                "I don't understand that command. Please use the help commant."
            )
    

@bot.message_handler(func=lambda message: message.text == "Bot Registration")
def start_registration(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}  # Initialize user data for this chat
    bot.send_message(chat_id, "Please provide your first name:")
    bot.register_next_step_handler(message, collect_first_name)



user_data = {}
pending_verifications = {}
user_states = {}



def collect_first_name(message):
    chat_id = message.chat.id
    first_name = message.text.strip()
    if len(first_name) < 3:
        bot.reply_to(message, "First name must be at least 3 characters. Try again:")
        bot.register_next_step_handler(message, collect_first_name)
        return
    user_data['first_name'] = first_name
    bot.reply_to(message, "Please enter your father's name:")
    bot.register_next_step_handler(message, collect_fathers_name)
def collect_fathers_name(message):
    chat_id = message.chat.id
    fathers_name = message.text.strip()
    if len(fathers_name) < 3:
        bot.reply_to(message, "First name must be at least 3 characters. Try again:")
        bot.register_next_step_handler(message, collect_fathers_name)
        return
    user_data['fathers_name'] = fathers_name
    bot.reply_to(message, "Please enter your phone number:")
    bot.register_next_step_handler(message, collect_phone_number)
def collect_phone_number(message):
    chat_id = message.chat.id
    phone_number = message.text
    if len(phone_number) != 10 or not phone_number.isdigit():
        bot.send_message(message.chat.id, "Phone number must be exactly 10 digits. Please try again.")
        bot.register_next_step_handler(message, collect_phone_number)
        return
    user_data['phone_number'] = phone_number
    bot.send_message(message.chat.id, "Please enter your email address (must contain @gmail.com):")
    bot.register_next_step_handler(message, collect_email)
def collect_email(message):
    chat_id = message.chat.id
    email = message.text.strip()
    if not email.endswith('@gmail.com'):
        bot.reply_to(message, "Email must contain @gmail.com. Please try again:")
        bot.register_next_step_handler(message, collect_email)
        return
    user_data['email'] = email
    bot.send_message(chat_id, "Thank you! Now, please select a payment method or submit your receipt.", reply_markup=payment_markup())



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
    # bot.send_message(ADMIN_CHAT_ID, registration_details)

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
            bot.send_message(user_id, "✅ Your payment has been verified! Please proceed to select your service. this is our channel, please join us [channel](https://t.me/easygate)", reply_markup=main_menu_markup())
        else:
            bot.send_message(ADMIN_CHAT_ID, "The user ID is not in the pending verifications.")

    elif call.data.startswith('invalid_'):
        if user_id in pending_verifications:
            pending_verifications.pop(user_id)
            bot.send_message(user_id, "❌ Your payment could not be verified. Please contact support.")
            bot.send_message(ADMIN_CHAT_ID, f"Payment invalid for {user_id}. User has been notified.")
        else:
            bot.send_message(ADMIN_CHAT_ID, "The user ID is not in the pending verifications.")

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

        # Inform the user about the service selection

        # Clear the user's data after the service has been provided
        del user_data[user_id]
    else:
        bot.reply_to(message, "We could not find your payment details. Please resend your receipt.")


def process_receipt(message):
    # Process receipt logic here
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        "Thank you for submitting your receipt. Please choose a payment method or let us know if you've already paid:",
        reply_markup=payment_markup()  # Show the payment options
    )

def main_menu_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('About Us')
    btn2 = types.KeyboardButton('Our Services')
    btn3 = types.KeyboardButton('Continue to  Register')
    btn4 = types.KeyboardButton('Feedback')
    btn5 = types.KeyboardButton('Already Registered?')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup
def register_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Google Form')
    btn2 = types.KeyboardButton('Bot Registration')
    btn3 = types.KeyboardButton('Directly on Telegram')
    btn4 = types.KeyboardButton('main menu')
    markup.add(btn1, btn2, btn3, btn4)
    return markup
def feedback_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Google Form feedback')
    btn2 = types.KeyboardButton('Directly to Admin')
    btn3 = types.KeyboardButton('main menu')
    markup.add(btn1, btn2, btn3)
    return markup
def payment_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Bank Transfer')
    btn2 = types.KeyboardButton('Telebirr')
    btn3 = types.KeyboardButton('PayPal')
    btn4 = types.KeyboardButton('Already Paid? (Submit receipt)')
    btn5 = types.KeyboardButton('Choose Different Payment Method')
    btn6 = types.KeyboardButton('main menu')
    btn7 = types.KeyboardButton('Feedback')
    btn8 = types.KeyboardButton('back')
    markup.add(btn1, btn2, btn3, btn4, btn5,btn6, btn7, btn8)
    return markup




    print("Bot is running...")
bot.polling()
