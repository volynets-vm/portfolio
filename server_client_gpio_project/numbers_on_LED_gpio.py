#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
from random import randrange
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

one = [21,11]
two=[23,21,31,15,13]
three=[23,21,31,11,13]
four=[29,31,21,11]
five=[23,29,31,11,13]
six=[23,29,15,13,11,31]
seven=[29,23,21,11]
eight=[31,29,23,21,15,13,11]
nine=[29,23,21,31,11]
zero=[29,23,21,15,13,11]
led_pin=[31,29,23,21,15,13,11]
led_pins=[zero,one,two,three,four,five,six,seven,eight,nine]
led_pins_r=led_pins.copy()
led_pins_r.reverse()
button_pin= 36
state = 0
numbercounter=0
GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def callback_func(channel):
    global state
    if GPIO.input(channel) == GPIO.HIGH:
        state+=1
        if state==3: 
            state=0
        print(state)

GPIO.add_event_detect(button_pin, GPIO.RISING, callback=callback_func,bouncetime=300)

    
def timesleep():
    start = time.time()
    while time.time() < start + .5:
        pass

def lab1_task4():
    global state, numbercounter
    try:
        while True:
            if state ==0:
                GPIO.output(led_pins[numbercounter], GPIO.LOW)
                timesleep()
                GPIO.output(led_pins[numbercounter], GPIO.HIGH)
                if numbercounter < 9:
                    numbercounter +=1
                else:
                    numbercounter = 0
            elif state ==1:
                for led in led_pins_r[9-numbercounter:]:
                    if state != 1: break

                    GPIO.output(led, GPIO.LOW)
                    timesleep()
                    GPIO.output(led, GPIO.HIGH)
                    numbercounter=9

            elif state ==2:
                GPIO.output(led_pins[numbercounter], GPIO.LOW)
                timesleep()
                GPIO.output(led_pins[numbercounter], GPIO.HIGH)
                numbercounter=randrange(10)


    except KeyboardInterrupt:
        print("\n keyboard interrupt")
        GPIO.cleanup()



if __name__ == "__main__":
    lab1_task4()
