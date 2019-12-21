from pyglet import *
from pyglet.gl import *
import numpy as np
import time
from PIL import Image
import random
import math

key = pyglet.window.key

BLACK = np.array([0, 0, 0], dtype='uint8')
WHITE = np.array([1, 1, 1], dtype='uint8')

leaf_nodes = []


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return str((self.x, self.y))


class Node():
    # box = array of points
    def __init__(self, parent, box=[], val=0.0):
        self.parent = parent
        par_val = 0.0

        if parent:
            par_val = parent.value

        self.value = random.random() + par_val

        """
        points in box:

        p0 --- p1
        |      |
        p2 --- p3

        """
        self.box = box
        self.pos = box[0]  # "position" is top left corner
        self.ipos = (math.floor(self.pos.x), math.floor(self.pos.y))
        self.x = self.pos.x
        self.y = self.pos.y
        self.width = box[1].x - box[0].x
        self.height = box[2].y - box[0].y
        self.children = []
        self.create_children()

    def __repr__(self):
        return "Node: " + str((self.x, self.y)) + " d: " + str((self.width, self.height))

    def set_value(self, val):
        self.value = val

    def create_children(self):
        if self.width > 1.0 and self.height > 1.0:
            h_width = self.width / 2
            h_height = self.height / 2

            """
            points in children:

            p0 --- p1 --- p2
            |  b0  |   b1  |
            p3 --- p4 --- p5
            |  b2  |   b3  |
            p6 --- p7 --- p8

            """

            # TODO: make this a loop
            p0 = Point(self.x, self.y)
            p1 = Point(self.x + h_width, self.y)
            p2 = Point(self.x + self.width, self.y)
            p3 = Point(self.x, self.y + h_height)
            p4 = Point(self.x + h_width, self.y + h_height)
            p5 = Point(self.x + self.width, self.y + h_height)
            p6 = Point(self.x, self.y + self.height)
            p7 = Point(self.x + h_width, self.y + self.height)
            p8 = Point(self.x + self.width, self.y + self.height)

            # TODO: aggregate child points into list

            # make boxes
            box0 = [p0, p1, p3, p4]
            box1 = [p1, p2, p4, p5]
            box2 = [p3, p4, p6, p7]
            box3 = [p4, p5, p7, p8]

            # append children
            self.children.append(Node(self, box0))
            self.children.append(Node(self, box1))
            self.children.append(Node(self, box2))
            self.children.append(Node(self, box3))


class QTree():
    def __init__(self, w, h):
        box = [
            Point(0, 0),
            Point(w, 0),
            Point(0, h),
            Point(w, h)
        ]
        self.root = Node(None, box)
        self.leaves = []
        self.find_leaves(self.root, self.leaves)

    def find_leaves(self, node, leaves):
        if node and not node.children:
            leaves.append(node)
            return None
        else:
            for child in node.children:
                self.find_leaves(child, leaves)
        return leaves


class main(pyglet.window.Window):
    def __init__(self, width=256, height=256, fps=False, *args, **kwargs):
        super(main, self).__init__(width, height, *args, **kwargs)
        self.x, self.y = 0, 0

        self.keys = {}

        self.mouse_x = 0
        self.mouse_y = 0

        self.pic = None
        self.t = 0.0
        self.cell_size = 100
        self.aspect_ratio = width / height

        self.q_tree = QTree(self.width, self.height)

        # self.grid_size = int(height / 2)
        self.image_dimensions = (height, width, 3)
        self.make_rand_arr()
        self.update_array()
        # print("dimensions", self.image_dimensions, self.arr[0][0])
        self.alive = 1

    def make_rand_arr(self):
        dim = self.image_dimensions
        # self.arr = self.base_pic
        # arr = np.uint8(np.random.uniform(size=dim) * 255)
        self.arr = np.uint8(np.zeros(dim) + 1.0 * 255)
        return self.arr

    def update_array(self):
        dim = self.image_dimensions
        arr = self.arr

        for l in self.q_tree.leaves:
            x = l.ipos[0]
            y = l.ipos[1]
            if l.value >= 5.0:
                arr[x][y] = BLACK
            # else:
            #     arr[x][y] = WHITE
        print("frame:", self.t)
        # for x in range(dim[0]):
        #     t = 0
        #     for y in range(dim[1]):
        #         if x % 10 == 0 and y % 10 == 0:
        #             if self.t % 12 == 0:
        #                 arr[x][y] = BLACK

        raw_im = Image.fromarray(arr).tobytes()
        pitch = -dim[0] * 3
        self.pic = pyglet.image.ImageData(
            dim[0], dim[1], 'RGB', raw_im)
        self.pic.width = self.width
        self.pic.height = self.height

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
        self.clear()
        self.make_rand_arr()
        self.update_array()
        self.pic.blit(0, 0, 0)
        # pic.blit(self.t % self.width, self.t % self.height, 0)

        self.flip()
        self.t = self.t + 1

    def run(self):
        pyglet.clock.schedule_interval(lambda x: self.render(), 15/60.0)
        pyglet.app.run()


if __name__ == '__main__':
    x = main()
    x.run()
