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

Configuration
-------------

Some security consideration is required before the agent will actually run.
Initially, you'll need to configure a GPG secret key for the server to
authenticate clients against. You'll want to do something like this to generate
the key in the agent's key store:

    sudo mkdir -p /var/lib/hypernova/gpg
    sudo gpg --homedir /var/lib/hypernova/gpg --gen-key
        Your selection? 1
        What keysize do you want? (2048) 2048
        Key is valid for? (0) 0
        Real name: server
        Email address: server@domain.com
        Comment:
        Change (N)ame, (C)omment, (E)mail or (O)kay/(Q)uit? O

Somewhere in the output, there should be a line that goes as follows; this is
what we're interested in:

    Key fingerprint = C461 B300 17B0 091E A832  177D 9433 88AC D723 87C4

We need to configure the agent's key directory now; the directory where all
authorised servers' keys are kept and where our own private key is kept.

Now, edit the file /etc/default/hn-agent, and pop the following values in:

    GNUPG_HOME='/path/to/keydir'
    GNUPG_FINGERPRINT='C461B30017B0091EA832177D943388ACD72387C4'

You'll need to make sure the agent has read/write access to the keystore, else
it won't be able to run. chown'ing the /var/lib/hypernova directory to a
dedicated hypernova user would be a good idea.

Execution
---------

Since the fanciness is starting to come together, you can now run the server via
a shell script in the python-src directory:

    cd python-src
    bin/agent

Hit Ctrl-C to kill it when you're done.

By default, the server will listen on 0.0.0.0:8080, so making an HTTP request to
port 8080 on the target machine should yield some form of output.
