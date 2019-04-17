import serial


class NanoRfiLed:

    def __init__(self):
        self.s = serial.Serial(port='COM4', baudrate=9600)
        #self.s.open()

    def read_card(self):
        if self.s.inWaiting() > 0:
            out = str(self.s.readline())
            out = out[2:len(out)-5]
            return int(out)

    def show(self, led_patterns):
        self.s.write("led".encode())

        print(self.s.readline())

      #  print(self.s.read_all())
        # for i in range(1):
        #     #pixels = (led_patterns[i][0] * 256 * 256) + (led_patterns[i][1] * 256) + led_patterns[i][2]
        #     self.s.write("255".encode())

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
    nano.show(leds)


