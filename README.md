# Strata

Experiments and visualizations of hierarchical cellular automata to simulate tiered or tree-based dynamical systems

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

## Examples

### QuadTrees

![quadtree clustering](images/quad_gamma_0.gif)

### QuadNoise

![quadtree pixel noise](images/quad_pixels_noise.gif)

### Vertex Triangulation

![triangles](images/quad_triangles.gif)
