import RPi.GPIO as GPIO
import MFRC522
import signal


class RfiDevice:
    # arr = array.array('i', [1, 2, 3])
    def __init__(self, configuration):
        self.MIFAREReader = MFRC522.MFRC522()
        self.none_count = 0
        self.last_card_id = None
        self.configuration = configuration
        self.retries = configuration.get_value("rfireader", "retries")

    def read_tag(self):
        (status, TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
        (status, uid) = self.MIFAREReader.MFRC522_Anticoll()
        card_id = None
        if status == self.MIFAREReader.MI_OK:
            card_id = uid[0] + (uid[1] << 8) + (uid[2] << 16) + (uid[3] << 24)

        if card_id is None:
            self.none_count = self.none_count + 1
        if card_id is not None:
            self.none_count = 0

        if card_id is not None or self.none_count > self.retries:
            self.last_card_id = card_id
            return card_id

        return self.last_card_id


if __name__ == "__main__":
    reader = RfiDevice()
    value = reader.read_tag()
    while value is None:
        value = reader.read_tag()

