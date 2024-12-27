import configparser #pip install config parser
from telethon import TelegramClient, events #pip install telethon
from datetime import datetime
import mysql.connector #pip install mysql-connector-python
import MySQLdb # pip install mysqlclientls

# initializing configuration
print("Initializing configuration...")
config = configparser.ConfigParser()
config.read("config.ini")


# read values for Telethon and set name(bot) and api_id and api_hash
API_ID = config('default','api_id')
API_HASH = config('default','api_hash')
API_KEY = config('default','api_key')
session_name = "bot_files/Bot"


# read values for MySQL
HOSTNAME = config('default','hostname')
USERNAME = config('default','username')
PASSWORD = config('default','password')
DATABASE = config('default','database')


# start the client (Telethon)
client = TelegramClient(session_name, API_ID, API_HASH).start(bot_token = API_KEY)

conn = mysql.connector.connect(host=HOSTNAME, user=USERNAME, password=PASSWORD, database=DATABASE)
cursor = conn.cursor()



# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(100) NOT NULL,
        fathers_name VARCHAR(100) NOT NULL,
        phone_number VARCHAR(15) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS receipts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        file_path VARCHAR(255) NOT NULL,
        upload_date DATETIME NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')
conn.commit()

# Directory for storing uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Start command
@client.on(events.NewMessage(pattern="(?i)/start"))
async def start(event):
    sender = await event.get_sender()
    SENDER = sender.id
    text = (
        "Hello! I can help you register.\n"
        "Please provide your details in the following format:\n"
        "/register FirstName FatherName PhoneNumber Email\n"
        "After that, upload your payment receipt as an image or PDF."
    )
    await client.send_message(SENDER, text)

# Register command
@client.on(events.NewMessage(pattern="(?i)/register"))
async def register(event):
    sender = await event.get_sender()
    SENDER = sender.id
    try:
        details = event.message.text.split(" ", 4)
        if len(details) < 5:
            await client.send_message(SENDER, "Please provide all required details: FirstName, FatherName, PhoneNumber, and Email.")
            return

        first_name, fathers_name, phone_number, email = details[1:]
        cursor.execute(
            "INSERT INTO users (first_name, fathers_name, phone_number, email) VALUES (%s, %s, %s, %s)",
            (first_name, fathers_name, phone_number, email)
        )
        conn.commit()

        if cursor.rowcount > 0:
            await client.send_message(SENDER, "Registration successful! Now upload your payment receipt as an image or PDF.")
        else:
            await client.send_message(SENDER, "Registration failed. Please try again.")
    except Exception as e:
        await client.send_message(SENDER, f"An error occurred: {e}")

# Handle file uploads
@client.on(events.NewMessage(incoming=True))
async def handle_file(event):
    sender = await event.get_sender()
    SENDER = sender.id
    if event.file:
        try:
            # Get the last inserted user's ID
            cursor.execute("SELECT id FROM users ORDER BY id DESC LIMIT 1")
            user = cursor.fetchone()
            if not user:
                await client.send_message(SENDER, "No user found. Please register first using /register.")
                return

            user_id = user[0]
            file_name = f"{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{event.file.name}"
            file_path = os.path.join(UPLOAD_DIR, file_name)

            # Save the file
            await event.download_media(file_path)

            # Insert file path into the database
            cursor.execute(
                "INSERT INTO receipts (user_id, file_path, upload_date) VALUES (%s, %s, %s)",
                (user_id, file_path, datetime.now())
            )
            conn.commit()

            if cursor.rowcount > 0:
                await client.send_message(SENDER, "Payment receipt uploaded successfully!")
            else:
                await client.send_message(SENDER, "Failed to upload receipt. Please try again.")
        except Exception as e:
            await client.send_message(SENDER, f"An error occurred while processing the file: {e}")
    else:
        await client.send_message(SENDER, "Please upload a valid image or PDF file.")

# Run the bot
print("Bot is running...")
client.run_until_disconnected()