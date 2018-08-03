import sys

EPSILON = sys.float_info.epsilon  # smallest possible difference
COLORS = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]


def convert_to_rgb(minval, maxval, val):
    fi = float(val - minval) / float(maxval - minval) * (len(COLORS) - 1)
    i = int(fi)
    f = fi - i
    if f < EPSILON:
        return COLORS[i]
    else:
        (r1, g1, b1), (r2, g2, b2) = COLORS[i], COLORS[i + 1]
        return int(r1 + f * (r2 - r1)), int(g1 + f * (g2 - g1)), int(b1 + f * (b2 - b1))


def clip(min_, max_, val):
    return max(min(val, max_), min_)
