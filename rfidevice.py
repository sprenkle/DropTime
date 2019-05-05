import RPi.GPIO as GPIO
import MFRC522
import signal
import logging
import datetime


class RfiDevice:
    # arr = array.array('i', [1, 2, 3])
    def __init__(self, configuration):
        self.MIFAREReader = MFRC522.MFRC522()
        self.last_card_id = None
        self.last_card_delay = int(configuration.get_value("rfireader", "delay"))
        self.last_time_read = datetime.datetime.now()
        logging.info("RFI Device delay = {}".format(str(self.last_card_delay)))

    def read_tag(self):
        (status, TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
        (status, uid) = self.MIFAREReader.MFRC522_Anticoll()
        card_id = None
        if status == self.MIFAREReader.MI_OK:
            card_id = uid[0] + (uid[1] << 8) + (uid[2] << 16) + (uid[3] << 24)
        logging.debug("RFI Device read {} {}".format(card_id, (self.last_time_read - datetime.datetime.now()).seconds))

        if card_id is not None:
            self.last_time_read = datetime.datetime.now()

        if card_id is not None or self.last_time_read < datetime.datetime.now() - \
                datetime.timedelta(seconds=self.last_card_delay):
            self.last_card_id = card_id
            return card_id

        return self.last_card_id


if __name__ == "__main__":
    reader = RfiDevice()
    value = reader.read_tag()
    while value is None:
        value = reader.read_tag()

