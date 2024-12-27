from telebot import TeleBot, types

# Initialize bot
bot = TeleBot("YOUR_BOT_TOKEN")

# Main Menu Markup
def main_menu_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Feedback", "About us", "Our services")
    markup.add("Continue to register", "Already Registered?")
    return markup

# Start command
@bot.message_handler(commands=['start'])
def start_registration(message):
    print(f"Chat ID: {message.chat.id}")
    bot.reply_to(
        message,
        f"""👋 Hi {message.chat.first_name}! 
Welcome to EasyGate! Your Gateway to Global Opportunities.

We specialize in:
- Scholarship and admissions
- Passport and visa applications
- Career and e-commerce services
- Travel consultancy
- Online courses and tests

Select a service to proceed:""",
        reply_markup=main_menu_markup()
    )

# Handle main menu options
@bot.message_handler(func=lambda msg: msg.text in ["Feedback", "About us", "Our services", "Continue to register", "Already Registered?"])
def handle_menu_choice(message):
    if message.text == "Feedback":
        feedback_menu(message)
    elif message.text == "About us":
        about_us(message)
    elif message.text == "Our services":
        our_services(message)
    elif message.text == "Continue to register":
        registration_menu(message)
    elif message.text == "Already Registered?":
        already_registered(message)

# Feedback Menu
def feedback_menu(message):
    markup = types.ForceReply()
    bot.reply_to(message, "Please provide your feedback. It will be sent to the admin.", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.reply_to_message and "feedback" in msg.reply_to_message.text.lower())
def handle_feedback(message):
    admin_id = "YOUR_ADMIN_CHAT_ID"  # Replace with actual admin chat ID
    try:
        bot.send_message(admin_id, f"New feedback from {message.chat.first_name}:\n\n{message.text}")
        bot.reply_to(message, "Thank you for your feedback!")
    except Exception as e:
        bot.reply_to(message, "An error occurred while sending your feedback. Please try again.")

# About Us
def about_us(message):
    bot.reply_to(
        message,
        """About EasyGate:
We are a global service provider assisting with:
- Admissions and scholarships
- Passport and visa services
- Career guidance
- E-commerce solutions
- Travel consultancy
- Online courses and tests

We aim to make global opportunities accessible to everyone!""",
        reply_markup=main_menu_markup()
    )

# Our Services
def our_services(message):
    bot.reply_to(
        message,
        """Our Services:
1. Scholarship and admissions assistance
2. Passport and visa application support
3. Career and e-commerce solutions
4. Travel consultancy
5. Online courses and test preparation

Select "Continue to register" to get started.""",
        reply_markup=main_menu_markup()
    )

# Registration Menu
def registration_menu(message):
    bot.reply_to(
        message,
        "To register, please provide your details in the following format:\n"
        "<First Name>, <Father's Name>, <Phone Number>, <Email>, <Payment Receipt>",
        reply_markup=types.ForceReply()
    )

@bot.message_handler(func=lambda msg: msg.reply_to_message and "provide your details" in msg.reply_to_message.text.lower())
def handle_registration_details(message):
    try:
        details = message.text.split(",")
        if len(details) != 5:
            raise ValueError("Invalid format. Please provide all details as instructed.")

        first_name = details[0].strip()
        fathers_name = details[1].strip()
        phone_number = details[2].strip()
        email = details[3].strip()
        payment_receipt = details[4].strip()

        # Save to database (pseudo-code)
        save_registration_to_db(first_name, fathers_name, phone_number, email, payment_receipt)

        bot.reply_to(message, "Your registration is successful!")
    except Exception as e:
        bot.reply_to(message, f"Error: {e}\nPlease try again.")

# Already Registered
def already_registered(message):
    bot.reply_to(
        message,
        "You are already registered! If you have any questions, please contact our support team.",
        reply_markup=main_menu_markup()
    )

# Save registration details to the database
def save_registration_to_db(first_name, fathers_name, phone_number, email, payment_receipt):
    # Implement the actual database save logic here
    print("Saving to DB:", first_name, fathers_name, phone_number, email, payment_receipt)

# Start the bot
bot.polling()
