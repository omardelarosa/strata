import random
import math

STRONG_PATH_THRESHOLD = 4.0
RANDOM_BIRTH_PROBABILITY = 0.2


def generate_random_value(prob=RANDOM_BIRTH_PROBABILITY):
    if random.random() <= prob:
        return 1.0
    else:
        return 0.0

# A function that uses the balance between children and neighbors to determin alive-ness


def gamma(node):
    n_sum = 0.0
    for n in node.neighbors:
        n_sum += n.value

    # add parent to n_sum
    if node.parent:
        n_sum += node.parent.value

    # children detract
    if node.children:
        for c in node.children:
            n_sum -= c.value

    result = 0.0
    # case 0: random death
    if generate_random_value(0.0001) == 1.0:
        result = 0.0
    # case 1: alive and 1 live neighbor -> die (underpopulation)
    elif node.value == 1.0 and n_sum <= 0.0:
        result = 0.0
    # case 2: alive and 2 live neighbors -> live (okay)
    elif node.value == 1.0 and n_sum > 0.0:
        result = 1.0
    # case 2: alive and 3 live neighbors -> dead (overpopulation)
    elif node.value == 0.0 and n_sum >= 1.0:
        result = 1.0
    # case 3: dead and 3 live neighbors -> live (reproduction)
    elif node.value == 0.0 and n_sum <= 1.0:
        result = generate_random_value(0.01)
    else:
        print("unhandled case: value: ", node.value, "n_sum: ", n_sum)
        result = node.value
    return result

# A function inspired by conway's game of life


def conway(node):
    n_sum = 0.0
    for n in node.neighbors:
        n_sum += n.value
    # case 1: alive and 1 live neighbor -> die (underpopulation)
    if node.value == 1.0 and n_sum <= 1.0:
        return 1.0
    # case 2: alive and 2 live neighbors -> live (okay)
    elif node.value == 1.0 and n_sum == 2.0:
        return 1.0
    # case 2: alive and 3 live neighbors -> dead (overpopulation)
    elif node.value == 1.0 and n_sum >= 3.0:
        return 0.0
    # case 3: dead and 3 live neighbors -> live (reproduction)
    elif node.value == 0.0 and n_sum >= 3.0:
        return 1.0
    # case 4: n_sum is 0 and is dead, randomly become born if its a strong path
    elif node.value == 0.0 and n_sum < 3.0:
        return generate_random_value()
    elif not node.children and node.path_sum > STRONG_PATH_THRESHOLD:
        return 1.0
    else:
        print("unhandled case: value: ", node.value, "n_sum: ", n_sum)
        return node.value
        # return 0.0

    # if node.path_sum < STRONG_PATH_THRESHOLD:
    #     return generate_random_value()
    # else:
    #     return result


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return str((self.x, self.y))


class Node():
    # box = array of points
    def __init__(self, parent, box=[], val=0.0, f=lambda x: x):
        self.parent = parent
        self.value = val
        if parent:
            self.level = parent.level + 1
            self.path_sum = parent.path_sum + parent.value
            self.f = parent.f  # inherited generator function
        else:
            self.level = 0
            self.path_sum = 0.0
            self.f = f  # generator function

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
        self.next_value = self.f(self)

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
    def __init__(self, w, h, f):
        box = [
            Point(0, 0),
            Point(w, 0),
            Point(0, h),
            Point(w, h)
        ]
        self.root = Node(None, box, generate_random_value(), f)
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
