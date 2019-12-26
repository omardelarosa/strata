from pyglet import *
from pyglet.gl import *
import numpy as np
import time
import math
from PIL import Image
from quadtree import QTree, conway, gamma, upward, generate_random_value
import argparse

key = pyglet.window.key

# ARG Parsing
parser = argparse.ArgumentParser(
    description='Renderer for hierarchical cellular automata', prog='strata')
parser.add_argument('--width', default=256, action='store',
                    help='Width of window')
parser.add_argument('--height', default=256, action='store',
                    help='Height of window')
parser.add_argument('--depth', default=7, action='store',
                    help='Maximum recursion depth of tree')
parser.add_argument('--slice', default=False, action='store',
                    help='Show only a 1-layer slice')
parser.add_argument('--out', default='', action='store',
                    help='Output directory for screenshots')
parser.add_argument('--steps', default=-1, action='store',
                    help='Number of steps before terminating (-1 == infinity)')

args = parser.parse_args()

BLACK = np.array([0, 0, 0], dtype='uint8')
WHITE = np.array([1, 1, 1], dtype='uint8')

INITIAL_LEAF_BIRTH_PROBABILIY = 0.05


class main(pyglet.window.Window):
    def __init__(self, width=256, height=256, depth=5, slice_only=False, out_dir='', steps=-1, fps=False, *args, **kwargs):
        super(main, self).__init__(width, height, *args, **kwargs)
        self.x, self.y = 0, 0
        self.is_rendering = False
        self.keys = {}

        self.mouse_x = 0
        self.mouse_y = 0

        if steps == -1:
            self.steps = math.inf
        else:
            self.steps = steps
        self.pic = None
        self.t = 0
        self.cell_size = 100
        self.aspect_ratio = width / height

        # maximum resolution of levels to draw
        self.depth = depth
        self.slice_only = slice_only
        self.out_dir = out_dir

        # self.q_tree = QTree(self.width, self.height, upward)
        self.q_tree = QTree(self.width, self.height, gamma, self.depth)

        # Initialize the tree
        self.q_tree.setup(lambda x: self.tree_setup(x))
        # self.q_tree = QTree(self.width, self.height, conway)

        # self.grid_size = int(height / 2)
        self.image_dimensions = (height, width, 3)
        self.make_arr()
        self.update_array()
        self.alive = 1

        # GL Options
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA,
                              pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

        # Render initial state
        if self.out_dir != '':
            self.draw_pixels()

        self.is_rendering = False

    def tree_setup(self, node):
        # use init function on itself
        if not node.children:
            node.value = generate_random_value(INITIAL_LEAF_BIRTH_PROBABILIY)

    def make_arr(self):
        dim = self.image_dimensions
        self.arr = np.uint8(np.zeros(dim))
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

    def draw_tree(self):
        # Batch drawing
        batch = pyglet.graphics.Batch()
        levels = min(self.depth, int(math.log(self.width, 2)) + 1)
        colors = [(100, 100, 255), (0, 255, 0), (255, 0, 255), (127, 0, 0)]
        color = colors[0]  # TODO: make this configurable
        alpha = int(255 / levels)
        if self.slice_only:
            # Single layer per frame
            d = self.depth
            al = 255
            self.q_tree.walk(self.q_tree.root,
                             lambda n: self.add_to_batch(
                                 n, d, batch, color, al))
        else:
            # # Multi-layers per frame
            for i in range(levels):
                self.q_tree.walk(self.q_tree.root,
                                 lambda n: self.add_to_batch(n, i, batch, color, alpha))

        batch.draw()

    # Used to generate an image from a quad tree
    def draw_pixels(self):
        dim = self.image_dimensions
        arr = self.arr
        for l in self.q_tree.leaves:
            x = l.ipos[0]
            y = l.ipos[1]
            arr[x][y] = np.uint8((l.path_sum / l.level) * 255)

        im = Image.fromarray(arr)
        im.save(self.out_dir + "/t_" + str(self.t) + ".png")

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

        # set frame label t
        self.t = self.t + 1

        self.clear()
        self.update_array()

        # draw vertices from tree
        self.draw_tree()

        if self.out_dir != '':
            self.draw_pixels()

        self.flip()

        self.is_rendering = False

        # Terminate after steps
        if self.t >= self.steps:
            exit()

    def run(self):
        pyglet.clock.schedule_interval(lambda x: self.render(), 1/60.0)
        pyglet.app.run()


if __name__ == '__main__':
    x = main(int(args.width), int(args.height),
             int(args.depth), bool(args.slice), str(args.out), int(args.steps))
    x.run()
