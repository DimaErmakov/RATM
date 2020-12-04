on run {targetBuddyPhone, targetMessage}
    tell application "Messages"
        send targetMessage to buddy targetBuddyPhone of service "SMS"
    end tell
end run
