########################################
# Name: Tarun Vigneswaran and Ryan Soroka
# Date: 
# Description: 
########################################
import RPi.GPIO as GPIO
from time import sleep
from random import randint
import pygame

# set to True to enable debugging output
DEBUG = False

# initialize the pygame library
pygame.init()

# set the GPIO pin numbers
# the LEDs (R, B, Y, G)
leds = [ 17, 16, 13, 6 ]
# the switches (R, B, Y, G)
switches = [ 18, 19, 20, 21 ]
# the sounds that map to each LED (from L to R)
sounds = [ pygame.mixer.Sound("one.wav"), pygame.mixer.Sound("two.wav"), pygame.mixer.Sound("three.wav"), pygame.mixer.Sound("four.wav") ]

# use the Broadcom pin mode
GPIO.setmode(GPIO.BCM)

# setup the input and output pins
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(switches, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# this function turns the LEDs on
def all_on():
    for i in leds:
        GPIO.output(leds, True)

# this function turns the LEDs off
def all_off():
    for i in leds:
        GPIO.output(leds, False)

# this functions flashes the LEDs a few times when the player loses the game
def lose():
    for i in range(0, 4):
        all_on()
        sleep(0.5)
        all_off()
        sleep(0.5)

# the main part of the program
# initialize the Simon sequence
# each item in the sequence represents an LED (or switch), indexed at 0 through 3
seq = []
# Best Score of the user
best_score=0
score=0
# randomly add the first two items to the sequence
seq.append(randint(0, 3))
seq.append(randint(0, 3))


print("Welcome to Simon!")
print("Try to play the sequence back by pressing the switches.")
print("Press Ctrl+C to exit...")

try:
    # keep going until the user presses Ctrl+C
    while (True):
        # randomly add one more item to the sequence
        seq.append(randint(0, 3))
        if (DEBUG):
            # display the sequence to the console
            if (len(seq) >= 3):
                print()
            print("seq={}".format(seq))
        # Adjust speed based on sequence length
        speed = 1.0
        if len(seq) >= 13:
            speed = 0.6
        elif len(seq) >= 10:
            speed = 0.7
        elif len(seq) >= 7:
            speed = 0.8
        elif len(seq) >= 5:
            speed = 0.9

        if (DEBUG):
            print("speed={}".format(speed))   
        
        # display the sequence using the LEDs
        for s in seq:
            # turn the appropriate LED on but don't turn on led if sequence is greater than 15
            if len(seq) < 15:
                GPIO.output(leds[s], True)
            # play its corresponding sound
            sounds[s].play()
            # wait and turn the LED off again

            sleep(speed)
            # turn the appropriate LED off but don't turn off led if sequence is greater than 15

            if len(seq) < 15:
                GPIO.output(leds[s], False)
            sleep(0.5 * speed)

        # wait for player input (via the switches)
        # initialize the count of switches pressed to 0
        switch_count = 0
        # keep accepting player input until the number of items in the sequence is reached
        while (switch_count < len(seq)):
            # initially note that no switch is pressed
            # this will help with switch debouncing
            pressed = False
            # so long as no switch is currently pressed...
            while (not pressed):
                # ...we can check the status of each switch
                for i in range(len(switches)):
                    # if one switch is pressed
                    while (GPIO.input(switches[i]) == True):
                        # note its index
                        val = i
                        # note that a switch has now been pressed
                        # so that we don't detect any more switch presses
                        pressed = True


            if (DEBUG):
                # display the index of the switch pressed
                print(val, end=" ")

            # light the matching LED only if the sequence is less than 15
            if len(seq) <= 15:
                GPIO.output(leds[val], True)
            # play its corresponding sound
            sounds[val].play()
            # wait and turn the LED off again if the sequence is less than 15
            if len(seq) <= 15:
                sleep(speed)
            GPIO.output(leds[val], False)
            sleep(0.25)

            # check to see if this LED is correct in the sequence
            if (val != seq[switch_count]):
                # player pressed the wrong switch
                lose()
                # display score and reset game
                if score > best_score:
                    best_score = score
                    print("Your Score was: {} ****New Best Score****".format(score))
                else:
                    print("Your score was : {} === Best Score : =====".format(score,best_score))
                score=0
                print("Let's start over. Get ready!")
                seq = []
                score = 0  # Reset score for new game
                speed = 1.0  # Reset speed to initial value
                sleep(2)  # Give player a moment before starting new sequence
                break

            # if the player has this item in the sequence correct, increment the count
            switch_count += 1
            score+=1
# detect Ctrl+C
except KeyboardInterrupt:
    all_off()    
    # reset the GPIO pins
    GPIO.cleanup()
