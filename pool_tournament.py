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


def create_bracket(
    participants: pd.DataFrame,
) -> List[Tuple[pd.Series, Optional[pd.Series]]]:
    """Create the tournament bracket."""
    num_participants = len(participants)
    bracket = []

    for i in range(0, num_participants, 2):
        if i + 1 < num_participants:
            bracket.append((participants.iloc[i], participants.iloc[i + 1]))
        else:
            bracket.append(
                (participants.iloc[i], None)
            )  # Handle odd number of participants

    return bracket


def draft_messages(
    bracket: List[Tuple[pd.Series, Optional[pd.Series]]]
) -> List[Tuple[str, str]]:
    """Draft messages for the tournament participants based on their preferred communication method."""
    messages = []

    for match in bracket:
        player1 = match[0]
        player2 = match[1]
        # print(player1["First and Last Name"])
        if player2 is not None:
            print(player2["First and Last Name"])

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
            deadline_date = (datetime.now() + timedelta(weeks=1)).strftime("%B %d, %Y")

            message1 = (
                f"Hello {player1['First and Last Name']}, you are matched with {player2['First and Last Name']} "
                f"for the upcoming round of the pool tournament. Please contact them at their {method2.lower()}: {contact_info2}. "
                "You have one week to complete your match. Please make sure to play your match and report the results to Dimitry Ermakov (440-403-5929) "
                f"by {deadline_date}. Failure to do so will result in disqualification for both you and your opponent. Good luck!"
            )

            message2 = (
                f"Hello {player2['First and Last Name']}, you are matched with {player1['First and Last Name']} "
                f"for the upcoming round of the pool tournament. Please contact them at their {method1.lower()}: {contact_info1}. "
                "You have one week to complete your match. Please make sure to play your match and report the results to Dimitry Ermakov (440-403-5929) "
                f"by {deadline_date}. Failure to do so will result in disqualification for both you and your opponent. Good luck!"
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
        module_dir = "C:/Users/ermak/OneDrive/Documents/ATDP"
        sys.path.append(module_dir)
        from windowsDailyPolls import find_and_click_image

        find_and_click_image("RATM_images/start.png")
        find_and_click_image("RATM_images/to.png")
        time.sleep(1)
        keyboard.write(to_number)
        time.sleep(0.25)
        pyautogui.press("enter")
        time.sleep(0.25)
        keyboard.write(message)
        time.sleep(0.25)
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


def main():
    input_file_path = "Pool Tournament Sign Up  (Responses) - Form Responses 1.csv"
    output_file_path = "tournament_messages.txt"

    # Load and process data
    df = load_data(input_file_path)
    df = map_skill_levels(df)

    # Generate the bracket and draft messages
    bracket = create_bracket(df)
    messages = draft_messages(bracket)

    intro_message = (
        f"Welcome to the Hillsdale Pool Tournament!\n\n"
        "Here is what you can expect:\n\n"
        "1. Opponent Communication: You will receive a message via your preferred form of communication "
        "(email or phone) that will contain details about your opponent for each round. The message will include "
        "their contact information, so you can arrange the match at a convenient time.\n\n"
        "2. Tournament Format: The tournament will be conducted in a knockout format, where each participant "
        "will face another in each round. Winners will advance to the next round until a champion is determined.\n\n"
        "3. Match Scheduling: Matches should be scheduled and played within the designated timeframe for each round. "
        "If you are unable to schedule your match, please inform Dimitry Ermakov (440-403-5929) as soon as possible.\n\n"
        "Best of luck in the tournament! Keep an eye out for your first match details, which will be "
        "sent to you shortly.\n\n"
        "Best regards,\nDimitry Ermakov"
    )

    for contact_info, message in messages:
        if "@" in contact_info:
            send_email(contact_info, message)  # Handle email sending
        else:
            send_sms(contact_info, message)  # Handle SMS sending

    # Save messages to a text file
    save_messages_to_file(messages, output_file_path)

    print(f"All messages have been saved to {output_file_path}.")


if __name__ == "__main__":
    main()
