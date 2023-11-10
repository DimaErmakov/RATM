import os
import sys
import time
import random
import configparser

# random_delay = 1
random_delay = random.randint(0, 3600)
print(f"Delaying for {random_delay} seconds")
time.sleep(random_delay)

file_path = "text.txt"

# Load the configuration file
config = configparser.ConfigParser()
config.read("config.ini")

# Retrieve the phone number from the configuration file
try:
    number = config.get("Credentials", "PRIVATE_PHONE_NUMBER")
except configparser.Error:
    print("Error: Unable to read the configuration file.")
    sys.exit(1)

script_path = "sendMessage.scpt"

with open(file_path, "r") as file:
    lines = file.readlines()

# Select a random line
random_line = random.choice(lines).strip()

# Send the selected random line
command = f'osascript {script_path} {number} "{random_line}"'
os.system(command)
