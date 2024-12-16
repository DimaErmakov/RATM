import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import configparser

# Read configuration file
config = configparser.ConfigParser()
config.read("config.ini")

# Email credentials from config file
SMTP_SERVER = config["EMAIL"]["smtp_server"]
SMTP_PORT = config["EMAIL"]["smtp_port"]
EMAIL_ADDRESS = config["EMAIL"]["email_address"]
EMAIL_PASSWORD = config["EMAIL"]["email_password"]

# Recipient information with carrier's email-to-SMS gateway domain
birthdays = [
    {"name": "Dima", "birthday": "06-06", "phone": "4404035929", "carrier": "tmobile"},
    {"name": "Bob", "birthday": "12-16", "phone": "4404035929", "carrier": "tmobile"},
]

# Carrier gateways for email-to-SMS
CARRIER_GATEWAYS = {
    "verizon": "vtext.com",  # For Verizon
    "att": "txt.att.net",  # For AT&T
    "tmobile": "tmomail.net",  # For T-Mobile
    "sprint": "messaging.sprintpcs.com",  # For Sprint
}


def send_email_sms(to, message):
    """Send SMS using an email-to-SMS gateway."""
    try:
        # Connect to the SMTP server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            # Create the message
            msg = MIMEText(message)
            msg["From"] = EMAIL_ADDRESS
            msg["To"] = to
            msg["Subject"] = ""

            # Send the message
            server.sendmail(EMAIL_ADDRESS, to, msg.as_string())
            print(f"Message sent to {to}")
    except Exception as e:
        print(f"Failed to send message to {to}: {e}")


def send_happy_birthday():
    """Check for birthdays and send SMS."""
    today = datetime.now().strftime("%m-%d")
    for person in birthdays:
        if person["birthday"] == today:
            carrier_gateway = CARRIER_GATEWAYS.get(person["carrier"], "")
            if not carrier_gateway:
                print(f"Carrier for {person['name']} is not supported.")
                continue

            # Construct email-to-SMS address
            sms_address = f"{person['phone']}@{carrier_gateway}"
            message = f"Happy Birthday, {person['name']}. Congrats on leveling up."
            send_email_sms(sms_address, message)

        else:
            print(f"No birthday today.")


# try:
#     with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#         server.starttls()
#         server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
#         print("SMTP connection successful.")
# except Exception as e:
#     print(f"SMTP connection failed: {e}")
# Test run
print("Running test for Birthday SMS service...")
send_happy_birthday()
