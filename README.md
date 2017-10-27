# A build tool for research code

I am a big fan of [pybuilder](http://pybuilder.github.io/): It creates
a unified workflow for all your projects and it makes sure that you really
run those unit tests every time you actually want to use your package. It
also does a lot more and it is great for a lot of other things as well.

Yet, much of my code is research code. Most of it should run quickly on
a local machine a small fraction of it should easily run on one or more
remote machines. Before running remotely, I really want to make sure the
unit tests run. When I run remotely, I don't want to bother with too much
detail, but I'd like the code to run in a virtual environment. Some of the
code I use has different dependencies for my remote and my local machine
(e.g. [pytorch](http://pytorch.org/) would like to know which cuda version
I have installed.

I often keep my editor (vim) open and try out things in the
code---potentially doing short remote runs. Because pybuilder is designed
to support really serious software projects, this workflow requires that
you jump through a couple of loopholes.

Resco (short for research code) is a bit of a simplified version of
pybuilder, a bit of a wrapper around fabric3, and a bit of a helper to
structure your code. It's meant for the iterative workflow that's typical
for many research projects, where you work on the code for a bit, write
the paper, wait for reviews and come back to the code to realize that you
don't remember what you did. Resco is trying to help with that.

## Installation

It's on pypi and you can simply run

    pip install resco

## Getting started

Use the resco cli tool to create a basic project like this

    resco <projectname>

This will create a folderstructure and a `fabfile.py`. The fabfile is your
central starting point. Let's add a script

    echo 'print("Hello world")' > scripts/tools/hello.py

We can obviously run it locally by

    python scripts/tools/hello.py

Alternatively, we can run it remotely by

    fab run_script:tools/hello.py
