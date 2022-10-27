import RPi.GPIO as GPIO
from time import sleep

#----- PINS ------#
# Uses 3v3 pin 17 
# Uses ground pin 20
buzzerPin = 24 # IO pin 18

# Settings
cur_freq = 3500
freqPerCycle = 2
maxFreq = 25000

# Produce a cycle of a tone
def tone(freq):
    cycleDuration = 1 / freq
    
    GPIO.output(buzzerPin, GPIO.HIGH)
    sleep(cycleDuration/2)
    GPIO.output(buzzerPin, GPIO.LOW)
    sleep(cycleDuration/2)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzerPin, GPIO.OUT)

#Play an initial high frequency for a tiny duration
for cycle in range(200):
    tone(50000)

#A tiny pause
sleep(0.02)

#Produce a rising tone until max frequency is reached
while True:
    cur_freq += freqPerCycle
    
    tone(cur_freq)
    
    if cur_freq > maxFreq:
        break