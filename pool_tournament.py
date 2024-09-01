import pandas as pd
import random
import os
from typing import List, Tuple, Optional

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


def draft_messages(bracket: List[Tuple[pd.Series, Optional[pd.Series]]]) -> List[str]:
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
            messages.append(message1)
            messages.append(message2)
        else:
            # Handle odd participant advancing
            message = f"Hello {player1['First and Last Name']}, you have automatically advanced to the next round due to an odd number of participants."
            messages.append(message)

    return messages


def save_messages_to_file(messages: List[str], file_path: str) -> None:
    """Save the drafted messages to a text file."""
    with open(file_path, "w") as f:
        for message in messages:
            f.write(message + "\n")


def main():
    # Define file paths
    input_file_path = "Pool Tournament Sign Up  (Responses) - Form Responses 1.csv"
    output_file_path = "tournament_messages.txt"

    # Load and process data
    df = load_data(input_file_path)
    df = map_skill_levels(df)

    # Generate the bracket and draft messages
    bracket = create_bracket(df)
    messages = draft_messages(bracket)

    # Print messages
    for message in messages:
        print(message)

    # Save messages to a text file
    save_messages_to_file(messages, output_file_path)


if __name__ == "__main__":
    main()
