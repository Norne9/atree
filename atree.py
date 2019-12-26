import sys
import math
import sdl2
import sdl2.ext
from collections import namedtuple

theta_min = 0.0
theta_max = 8.0 * math.pi
period = 15
line_spacing = 1.0 / 6.0
line_length = line_spacing / 2.0
y_screen_offset = 300.0
x_screen_offset = 240.0
x_screen_scale = 700.0
y_screen_scale = 700.0
y_camera = 1.5
z_camera = -5.0

g_rate = 1.0 / (2.0 * math.pi)
g_factor = g_rate / 3.0

Point = namedtuple("Point", ["x", "y", "alpha"])
Line = namedtuple("Line", ["start", "end"])


class Spiral:
    def __init__(self, foreground: int, angle_offset: float, factor: float):
        self.foreground = sdl2.ext.rgba_to_color(foreground)
        self.angle_offset = angle_offset
        self.factor = factor
        self.offset = 0
        self.segments = self._compute_segments()

    def _compute_segments(self):
        segments = []
        for offset in range(0, -period, -1):
            lines = []
            theta = theta_min + d_theta(theta_min, offset * line_spacing / period, g_rate, self.factor)
            while theta < theta_max:
                theta_old = theta if theta > theta_min else theta_min
                theta += d_theta(theta, line_length, g_rate, self.factor)

                if theta < theta_min:
                    continue

                lines.append(
                    Line(
                        start=get_point(theta_old, self.factor, self.angle_offset, g_rate),
                        end=get_point((theta_old + theta) / 2.0, self.factor, self.angle_offset, g_rate),
                    )
                )
            segments.append(lines)
        return segments

    def _draw_segment(self, segment: Line, surface):
        color = sdl2.ext.prepare_color(mul_color(self.foreground, segment.start.alpha), surface)
        line = list(map(round, [segment.start.x, segment.start.y, segment.end.x, segment.end.y]))
        sdl2.ext.line(surface, color, line)

    def render(self, surface):
        self.offset -= 1
        if self.offset <= -period:
            self.offset += period
        for s in self.segments[self.offset]:
            self._draw_segment(s, surface)


def get_point(theta, factor, angle_offset, rate):
    x = theta * factor * math.cos(theta + angle_offset)
    y = rate * theta
    z = -theta * factor * math.sin(theta + angle_offset)

    alpha = math.atan((y * factor / rate * 0.1 + 0.02 - z) * 40) * 0.35 + 0.65
    point = project2d(x, y, z, min(1.0, alpha))

    return point


def d_theta(theta, l_line_length, rate, factor):
    return l_line_length / math.sqrt(rate * rate + factor * factor * theta * theta)


def project2d(x, y, z, alpha):
    return Point(
        x=x_screen_offset + x_screen_scale * (x / (z - z_camera)),
        y=y_screen_offset + y_screen_scale * ((y - y_camera) / (z - z_camera)),
        alpha=alpha,
    )


def mul_color(color: sdl2.ext.Color, alpha: float):
    new_col = sdl2.ext.Color()
    new_col.r = round(color.r * alpha)
    new_col.g = round(color.g * alpha)
    new_col.b = round(color.b * alpha)
    new_col.a = round(color.a * alpha)
    return new_col


def make_draw():
    spirals = [
        Spiral(foreground=0x220000FF, angle_offset=math.pi * 0.92, factor=0.90 * g_factor),
        Spiral(foreground=0x002211FF, angle_offset=-math.pi * 0.08, factor=0.90 * g_factor),
        Spiral(foreground=0x660000FF, angle_offset=math.pi * 0.95, factor=0.93 * g_factor),
        Spiral(foreground=0x003322FF, angle_offset=-math.pi * 0.05, factor=0.93 * g_factor),
        Spiral(foreground=0xFF0000FF, angle_offset=math.pi, factor=g_factor),
        Spiral(foreground=0x00FFCCFF, angle_offset=0, factor=g_factor),
    ]

    def _draw(surface):
        sdl2.ext.fill(surface, 0)
        for s in spirals:
            s.render(surface)

    return _draw


def run():
    sdl2.ext.init()
    window = sdl2.ext.Window("Christmas Tree", size=(480, 800))
    window.show()

    surface = window.get_surface()
    draw = make_draw()

    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
        draw(surface)
        window.refresh()
        sdl2.SDL_Delay(1000 // 60)
    sdl2.ext.quit()
    return 0


if __name__ == "__main__":
    sys.exit(run())
