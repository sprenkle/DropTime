import board
import neopixel
pixels = neopixel.NeoPixel(board.D18, 30)
from configuration import Configuration


class LedDevice:
    def __init__(self, configuration):
        pixel_pin = board.D18
        self.num_pixels = 24
        if configuration.get_value("led_device", "order") == "RGB":
            order = neopixel.RGB
        else:
            order = neopixel.GRB
        self.pixels = neopixel.NeoPixel(pixel_pin, self.num_pixels, brightness=0.2, auto_write=False,
                                   pixel_order=order)

    def show(self, led_patterns):
        print(led_patterns)
        for i in range(self.num_pixels):
            p1 = led_patterns[i][0]
            p2 = led_patterns[i][1]
            p3 = led_patterns[i][2]

            self.pixels[i] = (p1, p2, p3)
        self.pixels.show()

    def clear(self):
        for i in range(self.num_pixels):
            self.pixels[i] = (0, 0, 0)
        self.pixels.show()
