#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

def LED_example():
    led_pin = [3,5]
                                    
    GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.LOW) 
    GPIO.output(led_pin, GPIO.HIGH)                    

    
    while True:
        
        GPIO.output(3, GPIO.HIGH)
        GPIO.output(5, GPIO.LOW)
        time.sleep(1)
        GPIO.output(3, GPIO.LOW)
        GPIO.output(5, GPIO.HIGH)
        time.sleep(1)
       
    GPIO.output(led_pin, GPIO.LOW)
    GPIO.cleanup()
if __name__ == "__main__":
    LED_example()
