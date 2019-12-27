import random
import math

STRONG_PATH_THRESHOLD = 4.0
RANDOM_BIRTH_PROBABILITY = 0.2

ALIVE = 1.0
DEAD = 0.0


def generate_random_value(prob=RANDOM_BIRTH_PROBABILITY):
    if random.random() <= prob:
        return 1.0
    else:
        return 0.0

# A function that uses the balance between children and neighbors to determin alive-ness


def upward(node):
    n_sum = 0.0
    # children detract
    if node.children:
        for c in node.children:
            n_sum += c.value

    # parent value
    p_val = 0.0
    if node.parent != None and node.parent.value:
        p_val += node.parent.value

    # propogate up from children
    if p_val == 0.0 and not node.children:
        return generate_random_value(0.001)

    if p_val == 1.0:
        return node.value

    if n_sum >= 2.0:
        return 0.0
    # if p_val == 0.0 and n_sum == 0.0:
    #     return generate_random_value(0.00003)

    # fallback
    # print("unhandled case: ", p_val, n_sum)
    return 0.0


def gamma(node):
    # initliazation, aka t=0
    if node == None:
        return DEAD

    n_sum = 0.0
    for n in node.neighbors:
        n_sum += n.value

    p_val = 0.0
    # add parent to n_sum
    if node.parent:
        p_val = node.parent.value

    c_sum = 0.0
    # children detract
    if node.children:
        for c in node.children:
            c_sum += c.value

    result = 0.0

    # Probabilitty of random birth at leaves
    BIRTH_RATE = 0.0001

    # Probability of random death at any level
    DEATH_RATE = 0.0001

    # Difference between children, parents and neighbors required to repoduce
    REPRODUCTION_THRESHOLD = 1.0

    # net value
    g_sum = n_sum + p_val - c_sum

    # case 0: random death
    if node.value == 1.0 and generate_random_value(DEATH_RATE) == 1.0:
        result = 0.0
    # case 0.1: leaf node
    elif not node.children:
        if node.value == 0.0:
            result = generate_random_value(BIRTH_RATE)
        else:
            result = node.value
    # case 1: alive and more children than neighborhood can support -> die (underpopulation)
    elif node.value == 1.0 and g_sum <= 0.0:
        result = 0.0
    # case 2: alive and more neighbors -> live (okay)
    elif node.value == 1.0 and g_sum > 0.0:
        result = 1.0
    # case 2: alive and too many neighbors -> dead (overpopulation)
    elif node.value == 0.0 and g_sum >= 1.0:
        result = 1.0
    # case 3: dead and relative equilibrium between neighbors and children -> live (reproduction)
    elif node.value == 0.0 and abs(g_sum) <= REPRODUCTION_THRESHOLD:
        result = 1.0
    # # case 4: random spawning at leaf nodes, offset by random death
    # elif not node.children:
    #     result = generate_random_value(
    #         BIRTH_RATE)  # spawn at leaves randomly
    else:
        # print("unhandled case: value: ", node.value, "n_sum: ", n_sum)
        result = node.value
    return result

# A function inspired by conway's game of life


def conway(node):
    # initliazation, aka t=0
    if node == None:
        return generate_random_value(0.5)

    # non-initialization
    n_sum = 0.0
    for n in node.neighbors:
        n_sum += n.value

    p_val = 0.0
    # add parent to n_sum
    if node.parent:
        p_val = node.parent.value

    c_sum = 0.0
    # children detract
    if node.children:
        for c in node.children:
            c_sum += c.value

    result = 0.0

    # special case: leaves
    # IDEA 1:  Immutable
    if not node.children:
        return node.value

    # IDEA 2: Scaled rules -- not working
    # if not node.children:
    #     if node.value == ALIVE and n_sum == 1.0:
    #         return node.value
    #     elif node.value == DEAD and n_sum == 2.0:
    #         return ALIVE
    #     else:
    #         return DEAD

    tot = c_sum + p_val + n_sum
    # case 1: alive, 2 or 3 neighbors
    if node.value == ALIVE and tot == 2.0 or tot == 3.0:
        result = ALIVE  # stay alive
    # case 2: dead and 3 neighbors
    elif node.value == DEAD and tot == 3.0:
        result = ALIVE
    elif node.value == ALIVE:
        result = DEAD  # die
    else:
        result = node.value  # die / stay dead
    return result


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return str((self.x, self.y))


class Node():
    # box = array of points
    def __init__(self, parent, box=[], f=lambda x: x, depth_max=math.inf):
        self.parent = parent
        if parent != None:
            self.level = parent.level + 1
            self.path_sum = parent.path_sum + parent.value
            self.f = parent.f  # inherited generator function
            self.value = f(None)
        else:
            self.level = 0
            self.path_sum = 0.0
            self.value = f(None)
            self.f = f

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

        # create  children if depth max wasn't reached
        if self.level < depth_max:
            self.create_children(depth_max)
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

    def create_children(self, depth_max):
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
            self.children.append(
                Node(self, box0, self.f, depth_max))
            self.children.append(
                Node(self, box1, self.f, depth_max))
            self.children.append(
                Node(self, box2, self.f, depth_max))
            self.children.append(
                Node(self, box3, self.f, depth_max))


class QTree():
    def __init__(self, w, h, f, d):
        box = [
            Point(0, 0),
            Point(w, 0),
            Point(0, h),
            Point(w, h)
        ]
        self.root = Node(None, box, f, d)
        self.leaves = []
        self.find_leaves(self.root, self.leaves)
        self.population = 0.0

    # Setup the tree in some way
    def setup(self, f):
        self.walk(self.root, f)

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

    def update_population(self):
        self.population = 0.0
        self.walk(
            self.root, lambda x: self.increment_population(x))

    def increment_population(self, x):
        self.population += x.value

    def update_node_next(self, node):
        self.walk(node, lambda n: n.update_next())

    def swap_node_values(self, node, f=lambda x: x):
        self.walk(node, lambda n: n.swap_values())

    def compute_path_sums(self, node):
        self.walk(node, lambda n: n.compute_path_sum())

    # recursively update all nodes
    def update(self):
        # NOTE: this is sequential in order to avoid race conditions
        self.update_node_next(self.root)
        self.swap_node_values(self.root)
        self.compute_path_sums(self.root)
        self.update_population()
