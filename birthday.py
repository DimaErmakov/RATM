import configparser
from datetime import datetime
from twilio.rest import Client

# Read configuration file
config = configparser.ConfigParser()
config.read("config.ini")

# Twilio credentials from config file
TWILIO_ACCOUNT_SID = config["twilio"]["account_sid"]
TWILIO_AUTH_TOKEN = config["twilio"]["auth_token"]
TWILIO_PHONE_NUMBER = config["twilio"]["phone_number"]

# Recipient information
birthdays = [
    {"name": "Dima", "birthday": "06-06", "phone": "+14404035929"},
    {"name": "Bob", "birthday": "12-05", "phone": "+14404035929"},
]


def send_sms(to, message):
    """Send an SMS using Twilio."""
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(to=to, from_=TWILIO_PHONE_NUMBER, body=message)
        print(f"Message sent to {to}")
    except Exception as e:
        print(f"Failed to send message to {to}: {e}")


def send_happy_birthday():
    """Check for birthdays and send SMS."""
    today = datetime.now().strftime("%m-%d")
    for person in birthdays:
        if person["birthday"] == today:
            message = f"Happy Birthday, {person['name']}! Have a wonderful day!"
            send_sms(person["phone"], message)


# Test run
print("Running test for Birthday SMS service...")
send_happy_birthday()
