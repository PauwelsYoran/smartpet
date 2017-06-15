class Read:


    def __init__(self):
        import RPi.GPIO as GPIO
        import MFRC522
        import signal

        GPIO.setwarnings(False)
        self.continue_reading = True
        self.MIFAREReader = MFRC522.MFRC522()

    def continue_reading(self):

        while self.continue_reading:
            (status,TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
            (status,uid) = self.MIFAREReader.MFRC522_Anticoll()
            if status == self.MIFAREReader.MI_OK:
                part1 ='{:02x}'.format(uid[0])
                part2 ='{:02x}'.format(uid[1])
                part3 ='{:02x}'.format(uid[2])
                part4 ='{:02x}'.format(uid[3])
                RFIDrecoNumb = str(part1)+str(part2)+str(part3)+str(part4)
                print("Card read UID: "+ RFIDrecoNumb)
                self.continue_reading = False