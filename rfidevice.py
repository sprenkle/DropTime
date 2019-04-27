import RPi.GPIO as GPIO
import MFRC522
import signal
import logging


class RfiDevice:
    # arr = array.array('i', [1, 2, 3])
    def __init__(self, configuration):
        self.MIFAREReader = MFRC522.MFRC522()
        self.none_count = 0
        self.last_card_id = None
        self.retries = int(configuration.get_value("rfireader", "retries"))
        logging.info("RFI Device retries = {}".format(str(self.retries)))

    def read_tag(self):
        (status, TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
        (status, uid) = self.MIFAREReader.MFRC522_Anticoll()
        card_id = None
        if status == self.MIFAREReader.MI_OK:
            card_id = uid[0] + (uid[1] << 8) + (uid[2] << 16) + (uid[3] << 24)
        logging.debug("RFI Device read {} none_count={}".format(card_id, self.none_count))

        if card_id is None:
            self.none_count = self.none_count + 1
        else:
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

