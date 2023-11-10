import os
import sys

file = open("text.txt", "r")
Lines = file.readlines()
number = "4404035929"

script_path = "sendMessage.scpt"

for line in Lines:
    if line == "":
        continue
    command = f'osascript {script_path} {number} "{line.strip()}"'
    os.system(command)
