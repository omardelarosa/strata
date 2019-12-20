from pyglet import *
from pyglet.gl import *
import numpy as np
import time
from PIL import Image

key = pyglet.window.key


class main(pyglet.window.Window):
    def __init__(self, width=800, height=600, fps=False, *args, **kwargs):
        super(main, self).__init__(width, height, *args, **kwargs)
        self.x, self.y = 0, 0

        self.keys = {}

        self.mouse_x = 0
        self.mouse_y = 0

        # self.base_pic = np.array(Image.open("rabbit.jpg", ))

        self.pic = None
        self.t = 0.0
        self.cell_size = 100
        self.aspect_ratio = width / height
        self.grid_size = int(height / 2)
        # self.image_dimensions = self.base_pic.shape
        self.image_dimensions = (
            height, width, 3)
        # print("base pic", )
        self.arr = self.make_rand_arr()
        print("dimensions", self.image_dimensions, self.arr[0][0])
        self.alive = 1

    def make_rand_arr(self):
        dim = self.image_dimensions
        # self.arr = self.base_pic
        arr = np.uint8(np.random.uniform(size=dim) * 255)
        # arr = np.uint8(np.zeros(dim) + (0.1 * self.t) * 255)
        raw_im = Image.fromarray(arr).tobytes()
        pitch = -dim[0] * 3
        self.pic = pyglet.image.ImageData(
            dim[0], dim[1], 'RGB', raw_im)
        self.pic.width = self.width
        self.pic.height = self.height
        self.arr = arr
        return self.arr
        # return np.uint8((np.zeros(dim) + 1.0) * 0.5 * 255)

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
        self.pic.blit(0, 0, 0)
        # pic.blit(self.t % self.width, self.t % self.height, 0)

        self.flip()
        self.t = self.t + 1

    def run(self):
        pyglet.clock.schedule_interval(lambda x: self.render(), 1/60.0)
        pyglet.app.run()


if __name__ == '__main__':
    x = main()
    x.run()
