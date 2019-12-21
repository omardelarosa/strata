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

STRONG_PATH_THRESHOLD = 10.0
RANDOM_BIRTH_PROBABILITY = 0.5
leaf_nodes = []


def generate_random_value():
    if random.random() <= 0.2:
        return 1.0
    else:
        return 0.0


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
        self.value = val
        if parent:
            self.level = parent.level + 1
            self.path_sum = parent.path_sum + parent.value
        else:
            self.level = 0
            self.path_sum = 0.0

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
        self.neighbors = self.get_neighbors()

    def __repr__(self):
        return "Node: " + str((self.x, self.y)) + " d: " + str((self.width, self.height))

    def generate_value(self):
        n_sum = 0.0
        for n in self.neighbors:
            n_sum += n.value
        # case 1: alive and 1 live neighbor -> die (underpopulation)
        if self.value == 1.0 and n_sum <= 1.0:
            return 0.0
        # case 2: alive and 2 live neighbors -> live (okay)
        elif self.value == 1.0 and n_sum == 2.0:
            return 1.0
        # case 2: alive and 3 live neighbors -> dead (overpopulation)
        elif self.value == 1.0 and n_sum >= 3.0:
            return 0.0
        # case 3: dead and 3 live neighbors -> live (reproduction)
        elif self.value == 0.0 and n_sum >= 3.0:
            return 1.0
        # case 4: n_sum is 0 and is dead, randomly become born if its a strong path
        elif self.value == 0.0 and n_sum < 3.0:
            return generate_random_value()
        elif not self.children and self.path_sum > STRONG_PATH_THRESHOLD:
            return 1.0
        else:
            print("unhandled case: value: ", self.value, "n_sum: ", n_sum)
            return self.value
            # return 0.0

    def get_neighbors(self):
        if not self.parent:
            return []
        else:
            return list(filter(lambda x: x != self, self.parent.children))

    def compute_path_sum(self):
        s = 0.0
        p = self.parent
        while p != None:
            s += p.value
            p = p.parent
        self.path_sum = s
        return s

    def update_next(self):
        # self.next_value = generate_random_value()  # DEBUG
        self.next_value = self.generate_value()

    def swap_values(self):
        self.value = self.next_value

    def update_path_sums(self):
        self.path_sum = self.compute_path_sum()

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
            self.children.append(Node(self, box0, generate_random_value()))
            self.children.append(Node(self, box1, generate_random_value()))
            self.children.append(Node(self, box2, generate_random_value()))
            self.children.append(Node(self, box3, generate_random_value()))


class QTree():
    def __init__(self, w, h):
        box = [
            Point(0, 0),
            Point(w, 0),
            Point(0, h),
            Point(w, h)
        ]
        self.root = Node(None, box, generate_random_value())
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

    def walk(self, node, f):
        # generate next values
        if node:
            f(node)
            if node.children:
                for child in node.children:
                    self.walk(child, f)
        return None  # void

    def update_node_next(self, node):
        self.walk(node, lambda n: n.update_next())

    def swap_node_values(self, node):
        self.walk(node, lambda n: n.swap_values())

    def compute_path_sums(self, node):
        self.walk(node, lambda n: n.compute_path_sum())

    # recursively update all nodes
    def update(self):
        self.update_node_next(self.root)
        self.swap_node_values(self.root)
        self.compute_path_sums(self.root)


class main(pyglet.window.Window):
    def __init__(self, width=256, height=256, fps=False, *args, **kwargs):
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

        self.q_tree = QTree(self.width, self.height)

        # self.grid_size = int(height / 2)
        self.image_dimensions = (height, width, 3)
        self.make_rand_arr()
        self.update_array()
        # print("dimensions", self.image_dimensions, self.arr[0][0])
        self.alive = 1

    def make_rand_arr(self):
        dim = self.image_dimensions
        self.arr = np.uint8(np.zeros(dim) + 1.0 * 255)
        return self.arr

    def add_to_batch(self, node, level, batch, colors):
        if node.value >= 1.0 and node.level == level:
            vs = (node.x, node.y, node.x + node.width, node.y + node.height)
            vertex_list = batch.add(2, pyglet.gl.GL_TRIANGLES, None,
                                    ('v2f', vs),
                                    ('c3B', colors)
                                    )

    def draw_triangles(self):
        # Batch drawing
        batch = pyglet.graphics.Batch()
        levels = [3, 4, 5]
        colors = [(0, 0, 255, 0, 255, 0), (255, 0, 255, 127, 0, 0)]

        # # Multi-layers per frame
        # for i in range(len(levels)):
        #     self.q_tree.walk(self.q_tree.root,
        #                      lambda n: self.add_to_batch(n, levels[i], batch, colors[i % 2]))

        # Single layer per frame
        i = int(self.t) % 3
        self.q_tree.walk(self.q_tree.root,
                         lambda n: self.add_to_batch(
                             n, levels[i], batch, colors[i % 2]))

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

        self.clear()
        self.make_rand_arr()
        self.update_array()

        # draw triangles
        # self.draw_triangles()

        # draw pixels
        self.draw_pixels()

        self.flip()
        self.t = self.t + 1

    def run(self):
        pyglet.clock.schedule_interval(lambda x: self.render(), 6/60.0)
        pyglet.app.run()


if __name__ == '__main__':
    x = main(256, 256)
    x.run()
