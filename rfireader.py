import RPi.GPIO as GPIO
import MFRC522
import signal


class RfiReader:
    # arr = array.array('i', [1, 2, 3])
    def __init__(self):
        self.MIFAREReader = MFRC522.MFRC522()

    def read_card(self):
        (status, TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
        (status, uid) = self.MIFAREReader.MFRC522_Anticoll()
        if status == self.MIFAREReader.MI_OK:
            return "%s-%s-%s-%s" % (uid[0], uid[1], uid[2], uid[3])
        return None


if __name__ == "__main__":
    reader = RfiReader()
    value = reader.read_card()
    while value is None:
        value = reader.read_card()
    print(value)
