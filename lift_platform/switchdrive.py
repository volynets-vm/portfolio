import RPi.GPIO as GPIO
import time
import tkinter as tk
import threading
from tkinter import ttk


DIR1_PIN = 17  # direction1
DIR2_PIN = 27  # dir2
PWM_PIN = 13   # PWM
ENCA_PIN = 23  # encoderA
ENCB_PIN = 24  # encoderB
FAULT_PIN = 25 # fault 
LIMITSWITCH1_PIN = 6 # switch1
LIMITSWITCH2_PIN = 5 # switch2
PWM_FREQUENCY = 500  # in Hz
PWM_DUTY_CYCLE = 25   # In %

up_pressed = False #GUI btn states
down_pressed = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR1_PIN, GPIO.OUT)
GPIO.setup(DIR2_PIN, GPIO.OUT)
GPIO.setup(PWM_PIN, GPIO.OUT)
GPIO.setup(ENCA_PIN, GPIO.IN)
GPIO.setup(ENCB_PIN, GPIO.IN)
GPIO.setup(FAULT_PIN, GPIO.IN)
GPIO.setup(LIMITSWITCH1_PIN, GPIO.IN)
GPIO.setup(LIMITSWITCH2_PIN, GPIO.IN)

pwm = GPIO.PWM(PWM_PIN, PWM_FREQUENCY)
pwm.start(0)


def start_motor_up():
    global up_pressed
    up_pressed = True
    GPIO.output(DIR1_PIN, GPIO.HIGH)  #Set direction 1
    GPIO.output(DIR2_PIN, GPIO.LOW)   #Clear direction 2
    pwm.ChangeDutyCycle(PWM_DUTY_CYCLE)  #Start PWM
    print("Motor going up")

def start_motor_down():
    global down_pressed
    down_pressed = True
    GPIO.output(DIR2_PIN, GPIO.HIGH)  #Set direction 2
    GPIO.output(DIR1_PIN, GPIO.LOW)   #Clear direction 1
    pwm.ChangeDutyCycle(PWM_DUTY_CYCLE)  #Start PWM
    print("Motor going down")

def stop_motor():
    pwm.ChangeDutyCycle(0)  #Stop PWM
    print("Motor stopped")

def upthread():
    global up_pressed
    start_motor_up()
    while not GPIO.input(LIMITSWITCH1_PIN) == GPIO.HIGH:
        pass #waiting for switch
    print("Swtich 1 is pressed") 
    stop_motor()
    up_pressed = False

def downthread():
    global down_pressed
    start_motor_down()
    while not GPIO.input(LIMITSWITCH2_PIN) == GPIO.HIGH:
        pass #waiting for switch
    print("Swtich 2 is pressed") 
    stop_motor()
    down_pressed = False   

#Main window
root = tk.Tk()
root.attributes("-fullscreen", True)
root.title("Motor Control")
root.configure(bg="black")

#Frame config
frame = tk.Frame(root, bg="black")
frame.pack(expand=True)

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 24), padding=50, width=10)

#Up button
btn_up = ttk.Button(frame, text="Up", style="TButton", command=lambda: threading.Thread(target=upthread).start())
btn_up.grid(row=0, column=0, padx=50, pady=50)

#Down button
btn_down = ttk.Button(frame, text="Down", style="TButton", command=lambda: threading.Thread(target=downthread).start())
btn_down.grid(row=0, column=1, padx=50, pady=50)

exit_btn = ttk.Button(frame, text="Exit", style="TButton", command=root.destroy)
exit_btn.grid(row=2, column=0, columnspan=2, pady=(10, 50))

try:
    root.mainloop()
except KeyboardInterrupt:
    pass

finally:
    pwm.stop()
    GPIO.cleanup()
    root.protocol("WM_DELETE_WINDOW")
