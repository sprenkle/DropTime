import board
import neopixel
pixels = neopixel.NeoPixel(board.D18, 30)
import logging



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
        logging.debug("Led pattern {}".format(led_patterns))
        for i in range(self.num_pixels):
            self.pixels[i] = (led_patterns[i][0], led_patterns[i][1], led_patterns[i][2])
        self.pixels.show()

    def clear(self):
        logging.debug("Led Clear")
        for i in range(self.num_pixels):
            self.pixels[i] = (0, 0, 0)
        self.pixels.show()
