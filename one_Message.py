import os
import sys
import time
import random
import configparser

random_delay = random.randint(0, 10)
print("Delaying for {} seconds".format(random_delay))
time.sleep(random_delay)

file_path = "/Users/dimaermakov/RATM/text.txt"

# Ensure the path to the config file is correct
config_path = "/Users/dimaermakov/RATM/config.ini"

# Check if the config file exists
if not os.path.exists(config_path):
    print("Error: Configuration file 'config.ini' not found.")
    sys.exit(1)

# Attempt to load the configuration file
config = configparser.ConfigParser()
try:
    config.read(config_path)
    number = config.get("Credentials", "PRIVATE_PHONE_NUMBER")
except (configparser.Error, KeyError) as e:
    print("Error: Unable to read the configuration file:", e)
    sys.exit(1)

script_path = "/Users/dimaermakov/RATM/sendMessage.scpt"

with open(file_path, "r") as file:
    lines = file.readlines()

# Check if the text file is empty
if not lines:
    print("Error: Text file 'text.txt' is empty.")
    sys.exit(1)

random_line = random.choice(lines).strip()

command = f'osascript {script_path} {number} "{random_line}"'
os.system(command)
