import time
import RPi.GPIO as GPIO
class a4988:
    def __init__(self):
        self.step=26
        self.dir=19
        self.transistor = 13

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.step,GPIO.OUT)
        GPIO.setup(self.dir,GPIO.OUT)
        GPIO.setup(self.transistor,GPIO.OUT)

    def turn_motor(self):
        GPIO.output(self.dir,GPIO.HIGH)

        GPIO.output(self.transistor,GPIO.HIGH)
        for i in range(0,25):
            GPIO.output(self.step,GPIO.HIGH)
            time.sleep(0.005)
            GPIO.output(self.step,GPIO.LOW)
            time.sleep(0.005)
        GPIO.output(self.transistor, GPIO.LOW)


mot=a4988(
)

