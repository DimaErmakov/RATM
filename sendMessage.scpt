on run {targetBuddyPhone, targetMessage}
    tell application "Messages"
	set targetService to 1st service whose service type = iMessage
	send targetMessage to buddy targetBuddyPhone of targetService
    end tell
end run
