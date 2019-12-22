# Strata

Experiments and visualizations of hierarchical cellular automata to simulate tiered or tree-based dynamical systems

## Installation

Python3+ is recommended.

```bash
pip install pyglet numpy
```

## Usage

```bash
git clone {repo_url}
cd strata
python . \
    --width {pixels_wide} \
    --height {pixels_height} \
    --depth {maximum_recursion_depth}
```

## Examples

### QuadTrees

![quadtree clustering](images/quad_gamma_0.gif)

### QuadNoise

![quadtree pixel noise](images/quad_pixels_noise.gif)

### Vertex Triangulation

![triangles](images/quad_triangles.gif)
