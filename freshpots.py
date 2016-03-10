#!/usr/bin/env python
#
# Play freshpots.wav when you press a button on your Raspberry Pi
# Second button is delayed 6m which is how long our coffee maker takes,
# and then curls a notification to our Slack channel
#
# Original code ripped from MAKE Magazine soundboard tutorial
#

# Requires FRESHPOTS_HOOK_URL env var for Slack notification to work

import pygame.mixer
from time import sleep
import RPi.GPIO as GPIO
from sys import exit
import os
import random

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.IN)
GPIO.setup(25, GPIO.OUT)

# Play in mono, my speaker is one channel
pygame.mixer.init(48000, -16, 1, 1024)

# Setup our samples
here = os.path.dirname(os.path.realpath(__file__))
sounds = [
    pygame.mixer.Sound(here + "/freshpot1.wav"),
    pygame.mixer.Sound(here + "/freshpot2.wav"),
    pygame.mixer.Sound(here + "/freshpot3.wav")
  ]
soundChannel = pygame.mixer.Channel(1)

def post_to_slack():
  string = 'curl -X POST -H "Content-type: application/json" --data \'{"text": "FRESH POTS!!!", "username": "Cafemachine", "icon_emoji": ":coffee:", "channel": "#vhx", "attachments": [{"image_url": "http://4.bp.blogspot.com/_8HV3Czzl5Vg/TES8nVaAEII/AAAAAAAAABY/L0iLGKPSKQ0/s1600/DaveGrohlFreshPots.jpg"}]}\' ' + FRESHPOTS_HOOK_URL
  # print string
  os.system(string)
  print

print "Soundboard ready!"
print "FRESHPOTS_HOOK_URL=" + FRESHPOTS_HOOK_URL
GPIO.output(25, False)

while True:
  try:
    if (GPIO.input(23) == True):
      print "Testing fresh pots!!!!"
      GPIO.output(25, True)
      soundChannel.play(random.choice(sounds))
      GPIO.output(25, False)
      # post_to_slack()

    if (GPIO.input(24) == True):
      print "Sleeping for 6 minutes while coffee brews..."
      GPIO.output(25, True)
      sleep(360)
      print "Fresh pots!!!!!!"
      soundChannel.play(sound)
      GPIO.output(25, False)
      post_to_slack()

    sleep(0.01)
  except KeyboardInterrupt:
    exit()

