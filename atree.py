import math
import pyglet
from dataclasses import dataclass

theta_min = 0.0
theta_max = 8.0 * math.pi
period = 40
line_spacing = 1.0 / 10.0
line_length = line_spacing / 2.0
y_screen_offset = 300.0
x_screen_offset = 240.0
x_screen_scale = 700.0
y_screen_scale = 700.0
y_camera = 1.5
z_camera = -5.0

g_rate = 1.0 / (2.0 * math.pi)
g_factor = g_rate / 3.0


@dataclass
class Point:
    x: float = 0
    y: float = 0
    alpha: float = 0


@dataclass
class Line:
    start: Point
    end: Point


class Spiral:
    def __init__(self, foreground: tuple, angle_offset: float, factor: float):
        self.foreground = foreground
        self.angle_offset = angle_offset
        self.factor = factor
        self.offset = 0
        segments = self._compute_segments()
        self.v_lists = [self._compute_buffer(s) for s in segments]

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

    def _compute_buffer(self, lines):
        vertices, colors = [], []
        for line in lines:
            vertices.extend([line.start.x, 800 - line.start.y, line.end.x, 800 - line.end.y])
            colors.extend(mul_color(self.foreground, line.start.alpha) + mul_color(self.foreground, line.end.alpha))
        return pyglet.graphics.vertex_list(len(vertices) // 2, ("v2f/static", vertices), ("c3f/static", colors))

    def render(self):
        self.v_lists[self.offset].draw(pyglet.gl.GL_LINES)

    def update(self, dt: float):
        self.offset -= 1
        if self.offset <= -period:
            self.offset += period


def get_point(theta, factor, angle_offset, rate):
    x = theta * factor * math.cos(theta + angle_offset)
    y = rate * theta
    z = -theta * factor * math.sin(theta + angle_offset)

    point = project2d(x, y, z)
    point.alpha = math.atan((y * factor / rate * 0.1 + 0.02 - z) * 40) * 0.35 + 0.65

    return point


def d_theta(theta, l_line_length, rate, factor):
    return l_line_length / math.sqrt(rate * rate + factor * factor * theta * theta)


def project2d(x, y, z):
    return Point(
        x=x_screen_offset + x_screen_scale * (x / (z - z_camera)),
        y=y_screen_offset + y_screen_scale * ((y - y_camera) / (z - z_camera)),
    )


def mul_color(color: tuple, alpha: float):
    r, g, b = color
    return r * alpha, g * alpha, b * alpha


def run():
    config = pyglet.gl.Config(sample_buffers=1, samples=4)
    window = pyglet.window.Window(480, 800, caption="Christmas Tree", config=config)

    spirals = [
        Spiral(foreground=(34 / 255, 0, 0), angle_offset=math.pi * 0.92, factor=0.90 * g_factor),
        Spiral(foreground=(0, 34 / 255, 17 / 255), angle_offset=-math.pi * 0.08, factor=0.90 * g_factor),
        Spiral(foreground=(102 / 255, 0, 0), angle_offset=math.pi * 0.95, factor=0.93 * g_factor),
        Spiral(foreground=(0, 51 / 255, 34 / 255), angle_offset=-math.pi * 0.05, factor=0.93 * g_factor),
        Spiral(foreground=(1, 0, 0), angle_offset=math.pi, factor=g_factor),
        Spiral(foreground=(0, 1, 204 / 255), angle_offset=0, factor=g_factor),
    ]

    @window.event
    def on_draw():
        window.clear()
        pyglet.gl.glLineWidth(2.0)
        for s in spirals:
            s.render()

    def update(dt):
        for s in spirals:
            s.update(dt)

    pyglet.clock.schedule_interval(update, 1 / 60.0)

    pyglet.app.run()


if __name__ == "__main__":
    run()
