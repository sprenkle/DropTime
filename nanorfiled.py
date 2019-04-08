import serial


class NanoRfiLed:

    def __init__(self):
        self.s = serial.Serial(port='COM4', baudrate=9600, bytesize=serial.EIGHTBITS,
                               parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
        #self.s.open()

    def read_card(self):
        if self.s.inWaiting() > 0:
            out = str(self.s.readline())
            out = out[2:len(out)-5]
            return int(out)

    def show(self, led_patterns):
        outstring = ""
        for i in range(24):
            pixels = (led_patterns[i][0] * 256 * 256) + (led_patterns[i][1] * 256) + led_patterns[i][2]
            outstring = outstring + " " + str(pixels)
        outstring = outstring + " "
        encodeString = outstring.encode()
        print(encodeString)
        self.s.write(encodeString)

    def clear(self):
        self.show([[0, 0, 255], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])


if __name__ == "__main__":
    nano = NanoRfiLed()
    # while True:
    #     out = nano.read_card()
    #     if out is not None:
    #         print(str(out))
    leds = [[0, 0, 255], [255, 0, 0], [0, 0, 255], [255, 0, 0], [0, 0, 255],
     [255, 0, 0], [0, 0, 255], [255, 0, 0], [0, 0, 255], [255, 0, 0],
     [0, 0, 255], [255, 0, 0], [0, 0, 255], [255, 0, 0], [0, 0, 255],
     [255, 0, 0], [0, 0, 255], [255, 0, 0], [0, 0, 255], [255, 0, 0],
     [0, 0, 255], [255, 0, 0], [0, 0, 255], [255, 0, 0]]
    nano.clear()


