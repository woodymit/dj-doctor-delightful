import curses
import time

import rgb_funcs

import numpy as np

COLOR_BLACK = 50
COLOR_WHITE = 51
COLOR_ORANGE = 52

ORANGE_RGB = np.array([255, 105, 0])

BG_CP_IDX = 50
TEXT_CP_IDX = 51


def init_default_colors():
    curses.init_color(COLOR_BLACK, 0, 0, 0)
    curses.init_color(COLOR_WHITE, 999, 999, 999)

    o = (999. / 255. * ORANGE_RGB).astype(int)
    curses.init_color(COLOR_ORANGE, o[0], o[1], o[2])


def init_default_color_pairs():
    curses.init_pair(BG_CP_IDX, COLOR_WHITE, COLOR_BLACK)
    curses.init_pair(TEXT_CP_IDX, COLOR_ORANGE, COLOR_BLACK)


def fill_background(stdscr):
    stdscr.bkgd(ord(' '), curses.color_pair(BG_CP_IDX))


def get_keypresses(stdscr):
    kb_buffer_empty = False
    logged_keys = []
    while not kb_buffer_empty:
        char = stdscr.getch()
        if char == -1:
            kb_buffer_empty = True
        else:
            logged_keys.append(char)
    return logged_keys


def arr(a):
    return np.array(a)


def border_coords(xl, xu):

    x_l, y_l = xl
    x_u, y_u = xu

    x_r = x_u - x_l
    y_r = y_u - y_l

    # Upper left to upper right
    u = np.vstack([np.ones(x_r - 1) * y_l, np.arange(x_l, x_u - 1)]).T
    # Bottom right to bottom left
    b = np.vstack([np.ones(x_r - 1) * (y_u - 1), np.arange(x_u - 1, x_l, -1)]).T
    # Bottom left to upper left
    l = np.vstack([np.arange(y_u - 1, y_l, -1), np.ones(y_r - 1) * x_l]).T
    # Upper right to bottom right
    r = np.vstack([np.arange(y_l, y_u - 1), np.ones(y_r - 1) * (x_u - 1)]).T

    # # Debugging
    # for a, label in zip([u, r, b, l], ['u', 'r', 'b', 'l']):
    #     print('{0}:{1}:{2}'.format(label, a.shape, a))

    # Concatenate side coordinate arrays
    lights_xy = np.vstack([u, r, b, l])

    return lights_xy


class LightsArr:

    def_color_idx = COLOR_WHITE

    def __init__(self, scr, yx, BG_COLOR=100):
        self.scr = scr
        self.yx = yx
        self.n = len(self.yx)
        self.colors = [curses.color_pair(self.def_color_idx)] * self.n

    def render_lights(self):
        # User must refresh screen herself
        for yx_pair, color in zip(self.yx, self.colors):
            y, x = yx_pair
            # y = min(y, 22)
            try:
                self.scr.addch(int(y), int(x), ord('*'), color)
            except Exception as e:
                raise Exception('addch error drawing at x:{0}; y:{1}'.format(
                        int(x), int(y)))


def initialize_gradient(start_hex="#0000cc", finish_hex='#FFFFFF',
        n=20, init_idx=100, bg_color=COLOR_BLACK):

    gradient = rgb_funcs.linear_gradient(start_hex, finish_hex, n)
    gradient = (999. / 255. * arr(gradient)).astype(int)

    color_indicies = []
    for i, rgb in enumerate(gradient):

        r, g, b = rgb
        color_idx = init_idx + i
        color_indicies.append(color_idx)

        curses.init_color(color_idx, r, g, b)
        curses.init_pair(color_idx, color_idx, bg_color)

    return color_indicies


def main(stdscr):

    # Initialize color, hide cursor
    curses.start_color()
    curses.curs_set(False)

    # Make getch non-blocking
    stdscr.nodelay(1)

    # Make border
    # stdscr.border(0)

    # Initialize colors
    init_default_colors()
    init_default_color_pairs()
    fill_background(stdscr)
    stdscr.refresh()

    # Write welcome message
    msg = 'a btb "lights from the comfort of your room" comm.prod'
    y_h, x_h = stdscr.getmaxyx()
    msg_start_x = int(x_h / 2 - len(msg) / 2)
    msg_start_y = int(y_h / 2)
    stdscr.addstr(msg_start_y, msg_start_x, msg)
    stdscr.refresh()

    # Start colors
    color_indices = initialize_gradient('#FF6900')

    # Instantiate lights
    lights_xy = border_coords((1, 1), (x_h - 1, y_h - 1))
    lights = LightsArr(stdscr, np.array(lights_xy))

    # Render lights
    lights.render_lights()
    stdscr.refresh()

    # Animate
    ncycles = 200
    cycle_dur = 0.1
    for t in range(ncycles):

        for i in range(lights.n):
            color_idx = color_indices[(t + i) % len(color_indices)]
            lights.colors[i] = curses.color_pair(color_idx)
        lights.render_lights()
        stdscr.refresh()

        # Stop if keypress is logged
        logged_keys = get_keypresses(stdscr)
        if logged_keys:
            curses.endwin()
            return

        time.sleep(cycle_dur)

    # End once keyboard is pressed
    stdscr.getch()
    curses.endwin()


if __name__ == '__main__':
    curses.wrapper(main)
