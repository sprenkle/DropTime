import serial
import time


class NanoRfiLed:

    def __init__(self):
       # self.arduino = serial.Serial(port='COM4', baudrate=9600)
        try:
            self.arduino = serial.Serial()
            self.arduino.port = "COM4"
            self.arduino.baudrate = 19200
            self.arduino.timeout = 1
            self.arduino.setDTR(False)
            #self.arduino.setRTS(False)
            self.arduino.open()

            print("Connection to 9600 established succesfully!\n")
        except Exception as e:
            print(e)

    def read_tag(self):
        self.arduino.read_all()
        self.arduino.write("r".encode())
       # time.sleep(1)
        out = self.arduino.readline().decode().strip()
        if out == '':
            return 0
        num = int(out) & 0xffffffff
        if num == 0:
            return None
        return num

    def show(self, led_patterns):
        p = "l "
        self.arduino.write(p.encode())
        #time.sleep(1)
        for i in range(24):
           # print(i)
            value = led_patterns[i][0]
            value1 = led_patterns[i][1]
            value2 = led_patterns[i][2]
            pixels = (led_patterns[i][0] * 256 * 256) + (led_patterns[i][1] * 256) + led_patterns[i][2]
            p = (str(pixels) + " ")
         #   print(p)
            self.arduino.write(p.encode())
            #time.sleep(1)

    def clear(self):
        self.show([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])


if __name__ == "__main__":
    nano = NanoRfiLed()
    nano.clear()
    # while True:
    #     out = nano.read_card()
    #     if out is not None:
    #         print(str(out))
    leds = [[0, 0, 255], [255, 0, 0], [0, 0, 255], [255, 0, 0], [0, 0, 255],
            [255, 0, 0], [0, 0, 255], [255, 0, 0], [0, 0, 255], [255, 0, 0],
            [0, 0, 255], [255, 0, 0], [0, 0, 255], [255, 0, 0], [0, 0, 255],
            [255, 0, 0], [0, 0, 255], [255, 0, 0], [0, 0, 255], [255, 0, 0],
            [0, 0, 255], [255, 0, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0]]

    # leds = [[0, 0, 255], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
    #                           [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
    #                           [0, 0, 0], [0, 255, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
    #                           [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
    #                           [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    nano.show(leds)
    time.sleep(5)
