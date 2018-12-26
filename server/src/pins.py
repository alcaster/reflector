class PINS:
    RED = 22
    GREEN = 27
    BLUE = 17

    def __init__(self, pi):
        self.pi = pi
        self.current_values = {
            PINS.RED: 0,
            PINS.GREEN: 0,
            PINS.BLUE: 0
        }

    def set_value(self, pin: int, value: int):
        if self.current_values[pin] != value and 0 <= value <= 255:
            self.current_values[pin] = value
            self.pi.set_PWM_dutycycle(pin, value)

    def set_value_to_all(self, r: int, g: int, b: int):
        for pin, value in zip([PINS.RED, PINS.GREEN, PINS.BLUE], [r, g, b]):
            if value is not None:
                self.set_value(pin, value)
