import pandas as pd
from typing import List, Tuple, Optional
import sys
import time
import keyboard
import pyautogui
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
import configparser

# Define skill levels with corresponding numerical values
SKILL_LEVEL_MAP = {
    "I do not know how to even use a pool cue.": 1,
    "I have only played a few times.": 2,
    "I know most rules and have played occasionally.": 3,
    "I play regularly and can hold my own in most games.": 4,
    "I am skilled or have experience in competitive play.": 5,
}


def load_data(file_path: str) -> pd.DataFrame:
    """Load the CSV file into a DataFrame."""
    return pd.read_csv(file_path)


def map_skill_levels(df: pd.DataFrame) -> pd.DataFrame:
    """Map skill levels to numeric values and sort participants."""
    df["Skill Level Value"] = df[
        "How would you rate your pool-playing skill level?"
    ].map(SKILL_LEVEL_MAP)
    return df.sort_values(by="Skill Level Value", ascending=False).reset_index(
        drop=True
    )


import random
import pandas as pd
from typing import List, Tuple, Optional


def create_bracket(
    participants: pd.DataFrame,
) -> List[Tuple[pd.Series, Optional[pd.Series]]]:
    """Create the tournament bracket with random matchups and specific constraints."""
    num_participants = len(participants)
    bracket = []

    # Shuffle participants to randomize matchups
    shuffled_indices = list(participants.index)
    random.shuffle(shuffled_indices)
    shuffled_participants = participants.loc[shuffled_indices].reset_index(drop=True)

    # Ensure specific constraints
    def find_index(name):
        matches = shuffled_participants[
            shuffled_participants["First and Last Name"] == name
        ]
        if not matches.empty:
            return matches.index[0]
        return None

    # dimitry_index = find_index("Dimitry Ermakov")
    # cass_index = find_index("Cass Dobrowolski")
    # isaac_index = find_index("Isaac Doughty")

    # Ensure Dimitry Ermakov and Cass Dobrowolski do not face each other
    # if dimitry_index is not None and cass_index is not None:
    #     if abs(dimitry_index - cass_index) == 1:
    #         # Swap Cass with the next participant if they are adjacent
    #         if cass_index + 1 < num_participants:
    #             shuffled_participants.iloc[[cass_index, cass_index + 1]] = (
    #                 shuffled_participants.iloc[[cass_index + 1, cass_index]]
    #             )
    #         else:
    #             # If Cass is the last participant, swap with the previous one
    #             shuffled_participants.iloc[[cass_index, cass_index - 1]] = (
    #                 shuffled_participants.iloc[[cass_index - 1, cass_index]]
    #             )

    # # Ensure Cass Dobrowolski and Isaac Doughty do not face each other
    # cass_index = find_index("Cass Dobrowolski")  # Update index after potential swap
    # if cass_index is not None and isaac_index is not None:
    #     if abs(cass_index - isaac_index) == 1:
    #         # Swap Isaac with the next participant if they are adjacent
    #         if isaac_index + 1 < num_participants:
    #             shuffled_participants.iloc[[isaac_index, isaac_index + 1]] = (
    #                 shuffled_participants.iloc[[isaac_index + 1, isaac_index]]
    #             )
    #         else:
    #             # If Isaac is the last participant, swap with the previous one
    #             shuffled_participants.iloc[[isaac_index, isaac_index - 1]] = (
    #                 shuffled_participants.iloc[[isaac_index - 1, isaac_index]]
    #             )

    # Create the bracket
    for i in range(0, num_participants, 2):
        if i + 1 < num_participants:
            bracket.append(
                (shuffled_participants.iloc[i], shuffled_participants.iloc[i + 1])
            )
        else:
            bracket.append(
                (shuffled_participants.iloc[i], None)
            )  # Handle odd number of participants

    return bracket


import re


# def create_bracket(file_path):
#     # Dictionary to hold the matchups
#     matchups = {}

#     with open(file_path, "r") as f:
#         lines = f.readlines()

#     # Iterate through lines in pairs (contact info and message)
#     for i in range(0, len(lines), 2):
#         contact_info = lines[i].strip()
#         message = lines[i + 1].strip()

#         # Extract the player and opponent names
#         player_match = re.search(r"Hello (.+?),", contact_info)
#         opponent_match = re.search(
#             r"matched with (.+?) for the upcoming round", message
#         )

#         if player_match and opponent_match:
#             player = player_match.group(1)
#             opponent = opponent_match.group(1).split(" ")[
#                 0
#             ]  # Extract only the first part of the opponent's name

#             # Store matchups
#             matchups[player] = opponent
#             matchups[opponent] = player

#     # Create bracket structure
#     bracket = {}
#     for player, opponent in matchups.items():
#         if (
#             player not in bracket
#             and opponent in matchups
#             and matchups[opponent] == player
#         ):
#             bracket[player] = opponent

#     return bracket


def draft_messages(
    bracket: List[Tuple[pd.Series, Optional[pd.Series]]]
) -> List[Tuple[str, str]]:
    """Draft messages for the tournament participants based on their preferred communication method."""
    messages = []

    for match in bracket:
        player1 = match[0]
        player2 = match[1]

        if player2 is not None:
            # Player 1 prefers email
            if (
                player1[
                    "What is your preferred form of communication that your opponent can contact you with: "
                ]
                == "Email"
            ):
                contact_info1 = player2["Email"]
                method1 = "Email"
            else:
                contact_info1 = player2["Phone Number"]
                method1 = "Phone Number"

            # Player 2 prefers email
            if (
                player2[
                    "What is your preferred form of communication that your opponent can contact you with: "
                ]
                == "Email"
            ):
                contact_info2 = player1["Email"]
                method2 = "Email"
            else:
                contact_info2 = player1["Phone Number"]
                method2 = "Phone Number"

            from datetime import datetime, timedelta

            # Calculate the deadline date (one week from today)
            deadline_date = (datetime.now() + timedelta(days=6)).strftime("%B %d, %Y")

            message1 = (
                f"{player1['First and Last Name']}, you are matched with {player2['First and Last Name']} "
                f"for the upcoming round of the pool tournament. Please contact them at their {method1.lower()}: {contact_info1}. "
                "You have one week to complete your match. Please make sure to report the results to Dimitry Ermakov (440-403-5929) "
                f"by {deadline_date} 11:59PM. "
                # Failure to do so will result in disqualification for both you and your opponent."
            )

            message2 = (
                f"{player2['First and Last Name']}, you are matched with {player1['First and Last Name']} "
                f"for the upcoming round of the pool tournament. Please contact them at their {method2.lower()}: {contact_info2}. "
                "You have one week to complete your match. Please make sure to report the results to Dimitry Ermakov (440-403-5929) "
                f"by {deadline_date} 11:59PM. "
                # Failure to do so will result in disqualification for both you and your opponent."
            )

            messages.append((contact_info1, message1))
            messages.append((contact_info2, message2))
        else:
            # Handle odd participant advancing
            message = f"Hello {player1['First and Last Name']}, you have automatically advanced to the next round due to an odd number of participants."
            preferred_method = player1[
                "What is your preferred form of communication that your opponent can contact you with: "
            ]
            contact_info = (
                player1["Email"]
                if preferred_method == "Email"
                else player1["Phone Number"]
            )
            messages.append((contact_info, message))

    return messages


def save_messages_to_file(messages: List[Tuple[str, str]], file_path: str) -> None:
    """Save the drafted messages to a text file."""
    with open(file_path, "w") as f:
        for contact_info, message in messages:
            f.write(message + "\n")


def send_sms(to_number: str, message: str) -> None:
    """Send SMS message using the provided phone number."""
    to_number = str(to_number)
    # Only execute if the number is not empty
    if to_number and to_number != "nan":
        if to_number == "4404035929":
            module_dir = "C:/Users/ermak/OneDrive/Documents/ATDP"
            sys.path.append(module_dir)
            from windowsDailyPolls import find_and_click_image

            find_and_click_image("RATM_images/start.png")
            find_and_click_image("RATM_images/to.png")
            time.sleep(1)
            keyboard.write(to_number)
            time.sleep(0.25)
            pyautogui.press("enter")
            time.sleep(3)
            keyboard.write(message)
            time.sleep(10)
            pyautogui.press("enter")


def send_email(
    email_address: str, message: str, subject: str = "Pool Tournament Opponent Matchup"
) -> None:
    """Send an email to the given address with the provided message and subject."""

    if not email_address or email_address == "nan":
        print("Invalid email address. Email not sent.")
        return

    config = configparser.ConfigParser()
    config.read("config.ini")

    EMAIL = config["EMAIL"]["email"]
    PASSWORD = config["EMAIL"]["password"]
    SMTP_SERVER = config["EMAIL"]["smtp_server"]
    SMTP_PORT = config.getint("EMAIL", "smtp_port", fallback=587)

    msg = MIMEMultipart()
    msg["From"] = EMAIL
    # msg["To"] = "ermakovd06@gmail.com"
    msg["To"] = email_address
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)  # Secure the connection
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
            print(f"Email sent to {email_address}")
    except Exception as e:
        print(f"Failed to send email to {email_address}. Error: {e}")


def to_single_line(text):
    """
    Converts a multi-line string into a single-line string by replacing newline characters with spaces.

    Parameters:
    - text (str): The multi-line string to be converted.

    Returns:
    - str: The single-line string.
    """
    # Replace newline characters with a space
    single_line_text = text.replace("\n", " ")

    # Optionally, you might want to strip any extra whitespace from the ends
    single_line_text = single_line_text.strip()

    return single_line_text


def main():
    input_file_path = "Pool Tournament Sign Up  (Responses) - Form Responses 1.csv"
    output_file_path = "tournament_messages.txt"

    # # Load and process data
    df = load_data(input_file_path)
    df = map_skill_levels(df)

    # Generate the bracket and draft messages
    bracket = create_bracket(df)
    messages = draft_messages(bracket)
    # get the messages from tournament_messages.txt
    # messages = []
    # with open("tournament_messages.txt", "r") as f:
    #     lines = f.readlines()

    #     # Ensure there are no extra blank lines at the end of the file
    #     lines = [line.strip() for line in lines if line.strip()]

    #     # Iterate through the lines in pairs
    #     for i in range(0, len(lines), 2):
    #         if i + 1 < len(lines):
    #             contact_info = lines[i]
    #             message = lines[i + 1]
    #             messages.append((contact_info, message))
    # print(messages)

    intro_message = (
        "Welcome to the Hillsdale Pool Tournament!\n\n"
        "Here is what you can expect:\n\n"
        "1. Opponent Communication: You will receive a message via your preferred form of communication "
        "(email or phone) that will contain details about your opponent for each round. The message will include "
        "their contact information, so you can arrange the match at a convenient time.\n\n"
        "2. Tournament Format: The tournament will be conducted in a knockout format, where each participant "
        "will face another in each round. Winners will advance to the next round until a champion is determined.\n\n"
        "3. Match Scheduling: Matches should be scheduled and played within the designated timeframe for each round. "
        "If you are unable to schedule your match, please inform Dimitry Ermakov (440-403-5929) as soon as possible.\n\n"
        "4. Reporting Results: After each match, both players are responsible for reporting the results to Dimitry Ermakov.\n\n"
        "5. Remember, 1st place = $25 Amazon gift card, 2nd place = $10 Amazon gift card, 3rd & 4th place = $5 Amazon gift card.\n\n"
        "Best of luck in the tournament! The first-round tournament matchups are:\n"
        "Nathaniel Osborne vs. Dimitry Ermakov\n"
        "Seth Jankowski vs. Tara Townsend\n"
        "Madeline Blake vs. Chris Chavey\n"
        "Lucy Minning vs. Anna Roberts\n"
        "Isaac Doughty vs. Noah Gazmin\n"
        "Tommy Flud vs. Regan Wight\n"
        "Cass Dobrowolski vs. Francesca Federici\n"
        "Katie Sayles vs. Ben Haas\n"
        "Matt Riehle vs. Mark Masaka\n"
        "Alfonso Garcia vs. Parker Reed\n"
        "Taylor Bordeaux vs. Aaleyah Welman\n\n"
        "Best regards,\nDimitry Ermakov"
    )
    intro_message_text = to_single_line(intro_message)
    # print(intro_message_text)
    # for contact_info, message in messages:
    #     if "@" in contact_info:
    #         # send_email(contact_info, intro_message)  # Handle email sending
    #         print(contact_info)
    #     #         pass
    #     else:
    #         print(f"\n{message}")
    # send_sms(contact_info, intro_message_text)  # Handle SMS sending

    # Save messages to a text file
    save_messages_to_file(messages, output_file_path)

    # print(f"All messages have been saved to {output_file_path}.")


if __name__ == "__main__":
    main()
