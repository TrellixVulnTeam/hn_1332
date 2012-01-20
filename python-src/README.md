HyperNova
=========

Installation
------------

To install HyperNova, you'll need Python 3.x. Any version in the 3.x series
should work, though we've developed and tested it primarily with version 3.2.2,
the latest available release.

The installation procedure uses setuptools, so you'll want to install
Distribute:

    sudo python3.2 < <(curl -s http://python-distribute.org/distribute_setup.py)

Then generate an egg from our source code:

    cd python-src
    python3.2 setup.py bdist_egg

Which can be installed like so:

    sudo easy_install-3.2 dist/hypernova-VERSION-py3.2.egg

Execution
---------

Since the fanciness is starting to come together, you can now run the server via
a shell script in the python-src directory:

    cd python-src
    bin/agent
  
Hit Ctrl-C to kill it when you're done.

By default, the server will listen on 0.0.0.0:8080, so making an HTTP request to
port 8080 on the target machine should yield some form of output.
