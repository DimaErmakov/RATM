import os
import sys

file = open('text.txt', 'r')
Lines = file.readlines()
number = sys.argv[1]

try:
	if sys.argv[2] == "sms":
		str1 = "osascript sendText.scpt " + number + " \""
		print("SMS")
except:
	print('iMessage')
	str1 = "osascript sendMessage.scpt " + number + " \""

for line in Lines:
	if line == '':
		continue
	os.system(str1 + line + "\"")

