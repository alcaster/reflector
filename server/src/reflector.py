from tools import convert_to_rgb


class Reflector:
    def __init__(self, memory_count):
        self.values = []
        self.memory_count = memory_count

    def append(self, val) -> [int, int, int]:
        self.values.append(val)
        self.values = self.values[-self.memory_count:]
        return convert_to_rgb(0, max(max(self.values), 1000), val) if val != 0 else (0, 0, 0)
