import RPi.GPIO as GPIO
from time import sleep

def pump_on():
    GPIO.setmode(GPIO.BOARD)    #sets the pin numbering
    GPIO.setup(7, GPIO.OUT)     #setting the GPIO pin connected to the pump as an output
    GPIO.output(7, GPIO.LOW)    #initialize
    GPIO.output(7, GPIO.HIGH)   #initialize
    GPIO.output(7, GPIO.LOW)    #pump starts
    sleep(3)                    #pumps for 3 seconds
    GPIO.output(7, GPIO.HIGH)   #pump stops

def get_status():
    GPIO.setmode(GPIO.BOARD)    #sets the pin numbering
    GPIO.setup(38, GPIO.IN)     #setting the GPIO pin connected to the sesor as an input
    moisture = GPIO.input(38)   #collecting the value from the pin and saving it to a variable
    #sensor outputs 0 if wet, 1 if dry, so it needs to be switched around to make sense
    if moisture == 0:
        moisture = 1
    elif moisture == 1:
        moisture = 0
    print(moisture)
    return moisture




        

