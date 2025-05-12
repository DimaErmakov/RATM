import challonge
import csv
from datetime import datetime, timedelta
import pyautogui
import time
import keyboard
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

# Retrieve the phone number from the configuration file
try:
    username = config.get("Credentials", "username")
    api = config.get("Credentials", "api")
except configparser.Error:
    print("Error: Unable to read the configuration file.")


def find_and_click_image(
    image_filename,
    biasx=0,
    biasy=0,
    up_or_down=None,
    max_attempts=20,
    DELAY=0.5,
):
    confidence = 0.7
    screen_width, screen_height = pyautogui.size()

    box = None
    attempt = 0
    while box is None and attempt < max_attempts:

        try:
            box = pyautogui.locateOnScreen(
                image_filename,
                confidence=confidence,
                region=(0, 0, screen_width, screen_height),
            )

        except pyautogui.ImageNotFoundException:
            print(f"{image_filename} not found.")

        if up_or_down is not None and box is None:
            print(f"{image_filename} not found. Scrolling...")
            factor = 400 if up_or_down == "up" else -400
            pyautogui.scroll(factor)
            time.sleep(DELAY)

        time.sleep(DELAY)
        attempt += 1

    if box is not None:
        x, y, width, height = box
        x = box.left + width / 2 + biasx
        y = box.top + height / 2 + biasy

        pyautogui.click(x, y)
        return x, y
    else:
        print("Image not found after multiple attempts.")


challonge.set_credentials(username, api)

# Replace with your tournament's URL
tournament = challonge.tournaments.show("ssz2fy7s")

# Retrieve participants and create a mapping from participant ID to their details
participants = challonge.participants.index(tournament["id"])
participant_info = {
    p["id"]: {"name": p["name"], "seed": p["seed"]} for p in participants
}

# Load phone numbers from your CSV file
phone_numbers = {}
with open("participants.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        full_name = f"{row['First and Last Name']}".strip()
        phone_numbers[full_name] = row["Phone Number"]

# Retrieve all matches
matches = challonge.matches.index(tournament["id"])

# Determine the current round (e.g., the lowest round number among open matches)
open_matches = [m for m in matches if m["state"] == "open"]
if not open_matches:
    print("No open matches found.")
    exit()

for match in open_matches:
    # Skip matches without two players
    if not match["player1_id"] or not match["player2_id"]:
        continue

    player1_id = match["player1_id"]
    player2_id = match["player2_id"]

    player1 = participant_info.get(player1_id)
    player2 = participant_info.get(player2_id)

    if not player1 or not player2:
        continue  # Skip if participant info is missing

    player1_name = player1["name"]
    player2_name = player2["name"]

    def format_phone(phone):
        digits = "".join(filter(str.isdigit, phone))
        if len(digits) == 10:
            return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits.startswith("1"):
            return f"{digits[0]}-{digits[1:4]}-{digits[4:7]}-{digits[7:]}"
        return phone  # fallback if format is unexpected

    player1_phone_raw = phone_numbers.get(player1_name, "N/A")
    player2_phone_raw = phone_numbers.get(player2_name, "N/A")
    player1_phone = (
        format_phone(player1_phone_raw) if player1_phone_raw != "N/A" else "N/A"
    )
    player2_phone = (
        format_phone(player2_phone_raw) if player2_phone_raw != "N/A" else "N/A"
    )

    # Calculate the deadline (4 days from now)
    deadline = (datetime.now() + timedelta(days=4)).strftime("%B %d at 11:59 PM")

    # Message for player 1
    message1 = (
        f"Hello {player1_name}, your opponent for this round of the pool tournament is {player2_name} "
        f"({player2_phone}). Please coordinate with him or her to schedule your match. "
        f"Don’t forget to text me the result with the score before {deadline}. Good luck."
    )

    # Message for player 2
    message2 = (
        f"Hello {player2_name}, your opponent for this round of the pool tournament is {player1_name} "
        f"({player1_phone}). Please coordinate with him or her to schedule your match. "
        f"Don’t forget to text me the result with the score before {deadline}. Good luck."
    )

    # https://voice.google.com/u/0/messages

    print(message1)
    find_and_click_image(
        r"C:\Users\ermak\OneDrive\Documents\RATM\RATM_images\sendNewMessage.png"
    )
    time.sleep(2)
    keyboard.write("4404035929")
    # keyboard.write(player1_phone_raw)
    time.sleep(2)
    pyautogui.press("down")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(2)
    pyautogui.press("tab", presses=3)
    keyboard.write(message1)
    time.sleep(2)
    pyautogui.press("tab")
    time.sleep(2)
    pyautogui.press("enter")
    # exit()

    print(message2)
    find_and_click_image(
        r"C:\Users\ermak\OneDrive\Documents\RATM\RATM_images\sendNewMessage.png"
    )
    time.sleep(2)
    keyboard.write("4404035929")
    # keyboard.write(player2_phone_raw)
    time.sleep(2)
    pyautogui.press("down")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(2)
    pyautogui.press("tab", presses=3)
    keyboard.write(message1)
    time.sleep(2)
    pyautogui.press("tab")
    time.sleep(2)
    pyautogui.press("enter")
    # exit()

    # Save messages to a txt file
    with open("messages.txt", "a", encoding="utf-8") as f:
        f.write(message1 + "\n")
        f.write(message2 + "\n")
