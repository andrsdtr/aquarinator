import RPi.GPIO as GPIO
from time import sleep

def pump_on():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.OUT)
    GPIO.output(7, GPIO.LOW)
    GPIO.output(7, GPIO.HIGH)
    GPIO.output(7, GPIO.LOW)
    sleep(3)
    GPIO.output(7, GPIO.HIGH)

def get_status():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(38, GPIO.IN)
    moisture = GPIO.input(38)
    #sensor outputs 0 if wet, 1 if dry, so it needs to be switched around to make sense
    if moisture == 0:
        moisture = 1
    elif moisture == 1:
        moisture = 0
    print(moisture)
    return moisture




        

