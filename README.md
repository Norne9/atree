# Christmas Tree

I tried to make [atree](https://github.com/anvaka/atree) on python.

Here is the result:

![tree](https://user-images.githubusercontent.com/4660466/71518891-e9de6500-28d6-11ea-8b76-442839b20378.gif)

## How to run

You need Python 3.7 (I haven't test other versions) and pyglet

Install pyglet as follows: `pip install pyglet`

And now run the application: `python atree.py`

## How it's built?

The tree is built of two spirals. These [11 lines of code](https://github.com/anvaka/atree/blob/2937249242a0204929aca45cdb8b937cfb5af3e5/index.js#L86-L97) render one line on spiral. It includes 3d projection and background shadow. _Almost_ the same as this [wiki image](http://en.wikipedia.org/wiki/File:ComplexSinInATimeAxe.gif):

![spiral](http://upload.wikimedia.org/wikipedia/commons/a/a5/ComplexSinInATimeAxe.gif)

# Happy Holidays!
