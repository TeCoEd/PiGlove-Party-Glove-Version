###TeCoEd FINAL VERSION###
###PI PARTY GLOVE###
###Project New York###

import time
import random
import os
import sys
import subprocess
import urllib
import tweepy
import picamera
import RPi.GPIO as GPIO
from sys import exit
#import espeak
from espeak import espeak

import energenie
from energenie import switch_on
from energenie import switch_off
energenie.switch_off(1)

# == OAuth Authentication ==###############
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key= ''
consumer_secret= ''

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located 
# under "Your access token")
access_token= ''
access_token_secret= ''
#
#
###########################################

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

######Set up the GPIO Pins ######
GPIO.setmode(GPIO.BCM)

###sets the pin to high ###
#GPIO.cleanup()

GPIO.setup(4, GPIO.IN, GPIO.PUD_UP) ##7 on the BOARD CAMERA Green Wire
GPIO.setup(6, GPIO.IN, GPIO.PUD_UP)  ##31 on the BOARD TWEET Brown Wire
GPIO.setup(18, GPIO.IN, GPIO.PUD_UP)  ##12 on the BOARD MUSIC Blue Wire 
GPIO.setup(9, GPIO.IN, GPIO.PUD_UP) ##21 on the DISCO LIGHTS Orange Wire
GPIO.setwarnings(False)##switch off other ports

###Introduction###
###welcome messages###

espeak.synth ("Welcome to the RASPERRY PI PARTY GLOVE")
time.sleep(2)
espeak.synth ("Please make a selection")
time.sleep(2)
espeak.synth ("Button 1 - take a picture,")
time.sleep(2)
espeak.synth ("Button 2 - tweet the picture")
time.sleep(2)
espeak.synth ("Button 3 - Play some Tunes")
time.sleep(3)
espeak.synth ("Button 4 - Engage the light show")
time.sleep(3)
espeak.synth ("Please select your button")

###Code for MP3 random play list###
songs_list = ["1", "2", "3", "4", "5"]
#song = (random.choice(songs_list))

###Code for the Camera to take a picture###
def take_a_pic():
    with picamera.PiCamera() as camera:
        camera.start_preview()
        time.sleep(2)
        camera.capture("newpic.jpg")

###Code for the Picture added to the Tweet and sent###        
def tweet_the_picture():
    api = tweepy.API(auth)
    photo_path = "/home/pi/newpic.jpg" ###will need to change name after test
    text = "Photo taken with the Pi Glove @ the Pi Party " + time_of_tweet
    api.update_with_media(photo_path, text)

def lights_on():
    espeak.synth("Let's Party")
    energenie.switch_on(1)
    
    
###Grabs the current time and day to add to the Tweet###
time_of_tweet = time.asctime( time.localtime(time.time()) )        

while True:
    if GPIO.input(4) == 0:
        #os.system('sudo killall mpg321') don't kill mp3s, it's a PARTY!
        time.sleep(1)
        espeak.synth("Preparing the Camera")
        time.sleep(2)
        espeak.synth(" Camera Ready, smile")
        time.sleep(2)
        take_a_pic() ###enables the camera def and takes a picture 
        espeak.synth("Picture Taken and Saved")
        time.sleep(3)
        espeak.synth("Press Button Two to tweet your picture")

    if GPIO.input(6) == 0:
        time.sleep(2)
        espeak.synth("Preparing your Tweet")
        tweet_the_picture() ###attach the picture to a tweet and sends it
        time.sleep(2)
        espeak.synth ("Your Tweet was sent")
        
    if GPIO.input(18) == 0:
        os.system('sudo killall mpg321')
        espeak.synth ("Music Player ")
        print""
        song_play = "yes"
        if song_play == "yes":
            os.system('mpg321 '+ (random.choice(songs_list)) + '.mp3 &') ##change the song!
            if GPIO.input(18) == 0: #turns off song longer hold
                os.system('sudo killall mpg321')
                song_play = "no"
                espeak.synth ("MP3 player stopped")
        

    if GPIO.input(9) == 0:
        #espeak.synth("Let's start the party")
        lights = "yes"
        if lights == "yes":
            lights_on()
            if GPIO.input(9) == 0:
                espeak.synth ("Lights off")
                energenie.switch_off(1)
    
        
       

        
        

    

    
    
        

        
        

        
