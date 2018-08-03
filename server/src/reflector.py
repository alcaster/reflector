from tools import convert_to_rgb, clip


class Reflector:
    def __init__(self, memory_count):
        self.values = []
        self.memory_count = memory_count

    def append(self, val) -> [int, int, int]:
        self.values.append(val)
        self.values = self.values[-self.memory_count:]
        max_values = max(self.values)
        color = convert_to_rgb(0, max_values, clip(0, max_values, val)) if val != 0 else (0, 0, 0)
        return color
