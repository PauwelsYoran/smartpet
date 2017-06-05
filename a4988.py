import time
import RPi.GPIO as GPIO

step=26
dir=19
transistro = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(step,GPIO.OUT)
GPIO.setup(dir,GPIO.OUT)
GPIO.setup(transistro,GPIO.OUT)

GPIO.output(dir,GPIO.HIGH)
while True:
    GPIO.output(transistro,GPIO.HIGH)
    for i in range(0,50):
        GPIO.output(step,GPIO.HIGH)
        time.sleep(0.005)
        GPIO.output(step,GPIO.LOW)
        time.sleep(0.005)
    GPIO.output(transistro, GPIO.LOW)
    time.sleep(2)