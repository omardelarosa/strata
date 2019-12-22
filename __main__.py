from pyglet import *
from pyglet.gl import *
import numpy as np
import time
import math
from PIL import Image
from quadtree import QTree, conway, gamma, upward
import argparse

key = pyglet.window.key

# ARG Parsing
parser = argparse.ArgumentParser(
    description='Draw quadcell graphics', prog='quadcells')
parser.add_argument('--width', default=256, action='store')
parser.add_argument('--height', default=256, action='store')
parser.add_argument('--depth', default=7, action='store')

args = parser.parse_args()

BLACK = np.array([0, 0, 0], dtype='uint8')
WHITE = np.array([1, 1, 1], dtype='uint8')


class main(pyglet.window.Window):
    def __init__(self, width=256, height=256, depth=5, fps=False, *args, **kwargs):
        super(main, self).__init__(width, height, *args, **kwargs)
        self.x, self.y = 0, 0
        self.is_rendering = False
        self.keys = {}

        self.mouse_x = 0
        self.mouse_y = 0

        self.pic = None
        self.t = 0.0
        self.cell_size = 100
        self.aspect_ratio = width / height

        # maximum resolution of levels to draw
        self.depth = depth

        # self.q_tree = QTree(self.width, self.height, upward)
        self.q_tree = QTree(self.width, self.height, gamma, self.depth)
        # self.q_tree = QTree(self.width, self.height, conway)

        # self.grid_size = int(height / 2)
        self.image_dimensions = (height, width, 3)
        self.make_rand_arr()
        self.update_array()
        self.alive = 1

        # GL Options
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA,
                              pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

        self.is_rendering = False

    def make_rand_arr(self):
        dim = self.image_dimensions
        self.arr = np.uint8(np.zeros(dim) + 1.0 * 255)
        return self.arr

    def add_to_batch(self, node, level, batch, color, alpha):
        if node.value >= 1.0 and node.level == level:
            vs = []
            colors = []
            idxs = [0, 1, 2, 2, 1, 3]
            for i in idxs:
                p = node.box[i]
                vs.append(p.x)
                vs.append(p.y)
                colors.append(color[0])
                colors.append(color[1])
                colors.append(color[2])
                colors.append(alpha)
            vertex_list = batch.add(len(idxs), pyglet.gl.GL_TRIANGLES, None,
                                    ('v2f', vs),
                                    ('c4B', colors)
                                    )

    def draw_triangles(self):
        # Batch drawing
        batch = pyglet.graphics.Batch()
        levels = min(self.depth, int(math.log(self.width, 2)) + 1)
        colors = [(100, 100, 255), (0, 255, 0), (255, 0, 255), (127, 0, 0)]
        color = colors[0]  # TODO: make this configurable
        alpha = int(255 / levels)
        # # Multi-layers per frame
        for i in range(levels):
            self.q_tree.walk(self.q_tree.root,
                             lambda n: self.add_to_batch(n, i, batch, color, alpha))

        # Single layer per frame
        # i = int(self.t) % 3
        # self.q_tree.walk(self.q_tree.root,
        #                  lambda n: self.add_to_batch(
        #                      n, levels[i], batch, colors[i % 4]))

        batch.draw()

    def draw_pixels(self):
        dim = self.image_dimensions
        arr = self.arr
        for l in self.q_tree.leaves:
            x = l.ipos[0]
            y = l.ipos[1]
            # # Automata based
            # if l.value >= 1.0:
            #     arr[x][y] = BLACK
            # Threshold based
            if l.path_sum >= 4.0:
                arr[x][y] = BLACK

        raw_im = Image.fromarray(arr).tobytes()
        pitch = -dim[0] * 3
        self.pic = pyglet.image.ImageData(
            dim[0], dim[1], 'RGB', raw_im)
        self.pic.width = self.width
        self.pic.height = self.height
        self.pic.blit(0, 0, 0)

    def update_array(self):
        dim = self.image_dimensions
        self.q_tree.update()

    def on_draw(self):
        self.render()

    def on_close(self):
        self.alive = 0

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x

    def on_key_release(self, symbol, modifiers):
        try:
            del self.keys[symbol]
        except:
            pass

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:  # [ESC]
            self.alive = 0

        self.keys[symbol] = True

    def render(self):
        # end when escape is pressed
        if self.alive == 0:
            exit()

        if self.is_rendering:
            return
        self.is_rendering = True

        self.clear()
        # self.make_rand_arr()
        self.update_array()
        # print("Population: ", self.q_tree.population)
        # draw triangles
        self.draw_triangles()

        # # draw pixels
        # self.draw_pixels()

        self.flip()
        self.t = self.t + 1
        self.is_rendering = False

    def run(self):
        pyglet.clock.schedule_interval(lambda x: self.render(), 1/60.0)
        pyglet.app.run()


if __name__ == '__main__':
    x = main(int(args.width), int(args.height), int(args.depth))
    x.run()
