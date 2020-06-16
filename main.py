# This is the first code to run on the controller. i:

# - This file is only a call to dynamically generated main folder

# i:\
#       main.py <-- This file
#       config.json <-- File for storing controller settings,
#                       so they don't get overridden by OTA update

#       main/ <-- main folder, which gets overridden when OTA update happens
#               main.py <-- Dynamic (Git updated) main.py - where program actually starts

#               

from main import main