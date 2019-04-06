import RPi.GPIO as GPIO
import SimpleMFRC522
import MFRC522


class RfiReader:
    # arr = array.array('i', [1, 2, 3])
    def __init__(self):
        self.reader = SimpleMFRC522.SimpleMFRC522()
        self.mfrc522 = MFRC522.MFRC522()

    def read_card(self):
        tag_id = self.reader.read_id_no_block()
        if tag_id is not None and tag_id == 474735937816:
            GPIO.cleanup()
            quit()
        return tag_id

    def read_card_block(self):
        uid = None
        while not uid:
            (status, TagType) = self.mfrc522.MFRC522_Request(self.mfrc522.PICC_REQIDL)
            if status != self.mfrc522.MI_OK:
                return None
            (status, uid) = self.mfrc522.MFRC522_Anticoll()
            if status != self.mfrc522.MI_OK:
                return None
        return uid


if __name__ == "__main__":
    reader = RfiReader()
    print(str(reader.read_card_block()))

