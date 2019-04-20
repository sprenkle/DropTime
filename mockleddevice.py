class MockLedDevice:

    def __init__(self):
        self.last_display = ""
        self.num_pixels = 24

    def show(self, led_patterns):
        display = ""
        for i in range(self.num_pixels):
            display = display + str(led_patterns[i][0] + led_patterns[i][1] * 255 + led_patterns[i][2] * 255 * 255) + " "
        if self.last_display != display:
            print(display)
            self.last_display = display

    def clear(self):
        print("Clear")
