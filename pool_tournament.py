import pandas as pd
from typing import List, Tuple, Optional
import sys
import time
import keyboard
import pyautogui

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
    """Draft text messages for the tournament participants."""
    messages = []

    for match in bracket:
        player1 = match[0]
        player2 = match[1]

        if player2 is not None:
            message1 = (
                f"Hello {player1['First and Last Name']}, you are matched with {player2['First and Last Name']} "
                f"for the upcoming round of the pool tournament. Please contact them at {player2['Phone Number']} to arrange your match time. Good luck!"
            )
            message2 = (
                f"Hello {player2['First and Last Name']}, you are matched with {player1['First and Last Name']} "
                f"for the upcoming round of the pool tournament. Please contact them at {player1['Phone Number']} to arrange your match time. Good luck!"
            )
            messages.append((player1["Phone Number"], message1))
            messages.append((player2["Phone Number"], message2))
        else:
            # Handle odd participant advancing
            message = f"Hello {player1['First and Last Name']}, you have automatically advanced to the next round due to an odd number of participants."
            messages.append((player1["Phone Number"], message))

    return messages


def send_sms(to_number: str, message: str) -> None:
    """Send SMS message. Here, this function will print messages for testing."""
    # Here we only send a simulated SMS to Dimitry for testing
    to_number = str(to_number)
    if to_number == "4404035929":
        print("test")
        print(f"Sending SMS to {to_number}: {message}")
    else:
        print(f"Simulating SMS to {to_number}... [Testing Mode]")


def send_sms(to_number: str, message: str) -> None:
    to_number = str(to_number)
    # if to_number == "4404035929":
    if True:

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


def main():
    input_file_path = "Pool Tournament Sign Up  (Responses) - Form Responses 1.csv"

    # Load and process data
    df = load_data(input_file_path)
    df = map_skill_levels(df)

    # Generate the bracket and draft messages
    bracket = create_bracket(df)
    messages = draft_messages(bracket)

    for phone_number, message in messages:
        send_sms(phone_number, message)


if __name__ == "__main__":
    main()
