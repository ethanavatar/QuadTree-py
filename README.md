# QuadTree-py

### An interactive pygame implementation of quadtree spatial quantization

## Contents
 - [Installation](#Installation)
 - [Usage](#Usage)
 - [API Reference](#API-Reference)
 - [TODO](#TODO)

## Installation

Clone the repo and navigate into it.
```bash
git clone https://github.com/ethanavatar/QuadTree-py.git
cd QuadTree-py/
```

Install pygame if you don't have it already,
```bash
python -m pip install pygame
```

## Usage

Run the main module using:
```bash
python main.py
```

You can use:
 - `ESCAPE` to clear the current board
 - `R` to create a new random board
 - `LEFT MOUSE` to add or remove cells

By default, the window is 1200x1200 pixels, the game board is 200x200 cells, and it runs at 60fps. These constants are stored at the top of the [`locals.py`](src/quadtree/locals.py) file if you feel like changing them.

<img title="Running Example" alt="Running Example" src="images/example-1200x1200.gif">

## API Reference
### `class Point(x : int, y : int)`
 - `x` : X-position
 - `y` : Y-position
 

### `class Rect( x : int, y : int, w : int, h : int)`
 - `x` : X-position
 - `y` : Y-position
 - `w` : Width
 - `h` : Height

### `class Quad(boundary : Rect, capacity : int)`
 - `boundary` : A `Rect` representing the size of the initial quad
 - `capacity` : The number of points allowed in a quad before it subdivides
    #### `void subdivide()`
    Splits the quad into four equally sized quadrants

    #### `bool insert(point : Point)`
    Tries to insert a point into the quad. If it doesnt exist within its boundary or its at capacity, it subdivides and calls `insert` recursively to the newly made quads.
     - `point` : The `Point` to insert.

    #### `list query(rect : Rect)`
    Returns a list of Points that are within the given Rect.
     - `rect` : A `Rect` representing the space in which to query point within.

    #### `void draw(surface : pygame.surface, color)`
    Draws a wireframe rectangle for the quad, and recursively, for all of its child quads.
     - `surface` : The `pygame.surface` to draw the quadtree to.
     - `color` : The color to draw the wireframe rectangles in.

## TODO
 - Make more generic; framework agnostic
