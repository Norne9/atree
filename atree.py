import math
import pygame
from dataclasses import dataclass

theta_min = 0.0
theta_max = 8.0 * math.pi
period = 20
line_spacing = 1.0 / 12.0
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
    black = pygame.Color("#000000")

    def __init__(self, foreground: pygame.Color, angle_offset: float, factor: float):
        self.foreground = foreground
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

    def _draw_segment(self, screen, segment):
        for line in segment:
            color = self.black.lerp(self.foreground, line.start.alpha)
            pygame.draw.aaline(screen, color, [line.start.x, line.start.y], [line.end.x, line.end.y])

    def render(self, screen):
        self.offset += 1
        if self.offset >= period:
            self.offset -= period
        self._draw_segment(screen, self.segments[self.offset])


def get_point(theta, factor, angle_offset, rate):
    x = theta * factor * math.cos(theta + angle_offset)
    y = rate * theta
    z = -theta * factor * math.sin(theta + angle_offset)

    point = project2d(x, y, z)
    point.alpha = min(1.0, math.atan((y * factor / rate * 0.1 + 0.02 - z) * 40) * 0.35 + 0.65)

    return point


def d_theta(theta, l_line_length, rate, factor):
    return l_line_length / math.sqrt(rate * rate + factor * factor * theta * theta)


def project2d(x, y, z):
    return Point(
        x=x_screen_offset + x_screen_scale * (x / (z - z_camera)),
        y=y_screen_offset + y_screen_scale * ((y - y_camera) / (z - z_camera)),
    )


def run():
    spirals = [
        Spiral(foreground=pygame.Color("#220000"), angle_offset=math.pi * 0.92, factor=0.90 * g_factor),
        Spiral(foreground=pygame.Color("#002211"), angle_offset=-math.pi * 0.08, factor=0.90 * g_factor),
        Spiral(foreground=pygame.Color("#660000"), angle_offset=math.pi * 0.95, factor=0.93 * g_factor),
        Spiral(foreground=pygame.Color("#003322"), angle_offset=-math.pi * 0.05, factor=0.93 * g_factor),
        Spiral(foreground=pygame.Color("#ff0000"), angle_offset=math.pi, factor=g_factor),
        Spiral(foreground=pygame.Color("#00ffcc"), angle_offset=0, factor=g_factor),
    ]

    pygame.init()
    screen = pygame.display.set_mode((480, 800))
    pygame.display.set_caption("Christmas Tree")

    done = False
    clock = pygame.time.Clock()

    while not done:
        clock.tick(60)
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

        screen.fill(0)
        for s in spirals:
            s.render(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    run()
