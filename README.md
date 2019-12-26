# Strata

QuadTree-based cellular automata rendering in Python.

## Installation

Python3+ is recommended.

```bash
pip install pyglet numpy
```

## Usage

```
usage: strata [-h] [--width WIDTH] [--height HEIGHT] [--depth DEPTH]
              [--slice SLICE] [--out OUT] [--steps STEPS]

Renderer for hierarchical cellular automata

optional arguments:
  -h, --help       show this help message and exit
  --width WIDTH    Width of window
  --height HEIGHT  Height of window
  --depth DEPTH    Maximum recursion depth of tree
  --slice SLICE    Show only a 1-layer slice
  --out OUT        Output directory for screenshots
  --steps STEPS    Number of steps before terminating (-1 == infinity)}
```

```bash
# 128x128 matrix, levels 0-7 only, 10 iterations
python3 . \
--width 128 \
--height 128 \
--depth 7 \
--out screenshots \
--steps 10
```

## Examples

#### Sparse Initial Matrix

`PROBABILITY_OF_LEAF_ALIVE_ON_START=0.000001`

| `t` | screenshot                              | notes                             |
| --- | --------------------------------------- | --------------------------------- |
| 0   | ![](examples/gamma_000001init/t_0.png)  | Initialization, hardly any pixels |
| 1   | ![](examples/gamma_000001init/t_1.png)  |                                   |
| 2   | ![](examples/gamma_000001init/t_2.png)  |                                   |
| 3   | ![](examples/gamma_000001init/t_3.png)  |                                   |
| 4   | ![](examples/gamma_000001init/t_4.png)  | Grid emerges                      |
| 5   | ![](examples/gamma_000001init/t_5.png)  | Grid of grids emerges             |
| 6   | ![](examples/gamma_000001init/t_6.png)  |                                   |
| 7   | ![](examples/gamma_000001init/t_7.png)  |                                   |
| 8   | ![](examples/gamma_000001init/t_8.png)  |                                   |
| 9   | ![](examples/gamma_000001init/t_9.png)  | Grids oscillate                   |
| 10  | ![](examples/gamma_000001init/t_10.png) |                                   |

#### Dense Initial Matrix

`PROBABILITY_OF_LEAF_ALIVE_ON_START=0.05`

| `t` | screenshot                          | notes                             |
| --- | ----------------------------------- | --------------------------------- |
| 0   | ![](examples/gamma_05init/t_0.png)  | Initialization, hardly any pixels |
| 1   | ![](examples/gamma_05init/t_1.png)  |                                   |
| 2   | ![](examples/gamma_05init/t_2.png)  |                                   |
| 3   | ![](examples/gamma_05init/t_3.png)  |                                   |
| 4   | ![](examples/gamma_05init/t_4.png)  | Grid emerges                      |
| 5   | ![](examples/gamma_05init/t_5.png)  | Noisier grid of grids emerges     |
| 6   | ![](examples/gamma_05init/t_6.png)  |                                   |
| 7   | ![](examples/gamma_05init/t_7.png)  |                                   |
| 8   | ![](examples/gamma_05init/t_8.png)  |                                   |
| 9   | ![](examples/gamma_05init/t_9.png)  |                                   |
| 10  | ![](examples/gamma_05init/t_10.png) | Less defined grids?               |

### Other Neat-Looking Artifacts

Here are a couple of neat looking artifacts that came out of the process:

### QuadTrees

![quadtree clustering](images/quad_gamma_0.gif)

### QuadNoise

![quadtree pixel noise](images/quad_pixels_noise.gif)

### Vertex Triangulation

![triangles](images/quad_triangles.gif)

### Timeseries
