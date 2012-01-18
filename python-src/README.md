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

Until initialisation scripts and other fanciness arrive, you can launch the
agent using the Python CLI. The fastest way is to do this, which passes the
command to execute straight to the Python interpreter and doesn't open the
interactive shell:

    python3.2 -c 'from hypernova.agent import Agent; Agent().execute()'

By default, the server will listen on 0.0.0.0:8080, so making an HTTP request to
port 8080 on the target machine should yield somje form of output.
