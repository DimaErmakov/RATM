# RATM - Reminder Automation Text Messaging

RATM is a simple Python script that automates the process of sending text messages as reminders. The script reads messages from a file and sends them to a specified phone number. The execution is scheduled using launchd on macOS. Special thanks to [Nick King](https://github.com/nrking0)

## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/your-username/RATM.git
    cd RATM
    ```

2. Install any required dependencies (if needed).

### Configuration

Create a configuration file named `config.ini` in the project root with the following content:

```ini
[Credentials]
PRIVATE_PHONE_NUMBER = "PHONE_NUMBER"
```

Replace `"PHONE_NUMBER"` with the actual private phone number.

**Note:** Ensure that `config.ini` is added to your `.gitignore` to avoid exposing sensitive information on your version-controlled repository.

### Scheduling

Use the following commands to schedule and unschedule the script using launchd:

```bash
# Schedule the script to run
launchctl bootstrap gui/501 /Users/dimaermakov/RATM/automated_Text_Script.plist

# Unschedule the script
launchctl bootout gui/501 /Users/dimaermakov/RATM/automated_Text_Script.plist
```

### Execution

Run the script manually or wait for it to be triggered by launchd. `all_Messages.py` is for sending all the lines in `text.txt` while `one_Message.py` is for just sending one random message from `text.txt`.

```bash
python3 all_Messages.py
```

```bash
python3 one_Message.py
```

## Important

- Make sure to keep your sensitive information, such as the phone number, secure. Avoid exposing it in version control and only share it with trusted collaborators.

- Adjust the timing and behavior of your reminders by modifying the script and the launchd plist file as needed.

## License

This project is licensed under the [MIT License](https://opensource.org/license/mit/).
