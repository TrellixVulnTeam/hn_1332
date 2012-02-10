HyperNova
=========

Installation
------------

To install HyperNova, you'll need Python 3.x. Any version in the 3.x series
should work, though we've developed and tested it primarily with version 3.2.2,
the latest available release.

The installation procedure uses setuptools, so you'll want to install
Distribute. We also depend on a few modules not shipped as part of the Python
standard library:

    sudo python3.2 < <(curl -s http://python-distribute.org/distribute_setup.py)
    sudo easy_install-3.2 python_gnupg

Then generate an egg from our source code:

    cd python-src
    python3.2 setup.py bdist_egg

Which can be installed like so:

    sudo easy_install-3.2 dist/hypernova-VERSION-py3.2.egg

Configuration
-------------

Upon launch, the HyperNova agent loads configuration files in
/etc/hypernova/agent in alphabetical order. To simplify running in development,
you can run the chroot/bin/agent script with the CONFDIR environment variable
set to test it:

    cd chroot
    CONFDIR=etc/hypernova/agent usr/bin/hn-agent

To configure the daemon initially, it'd be a good idea to copy the agent.ini
file to a new location (like local-agent.ini!) in the same directory and make
your changes there, since they'll take precedence over those specified in files
loaded before it.

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

You'll need to make sure the agent has read/write access to the keystore, else
it won't be able to run. chown'ing the /var/lib/hypernova directory to a
dedicated hypernova user would be a good idea.

Configuring elevator
--------------------

THe elevator tool enables the HyperNova agent to execute commands as root
despite actually running as an unprivileged user. Its configuration options can
only be set at configure-time, so we have to compile it ourselves. The
installation procedure is relatively simple though:

    git submodule init
    git submodule update

    cd python-src/chroot/src/elevator
    ./configure --prefix=/usr/local/hn-elevator \
                --target-uid=0 \
                --target-gid=0 \
                --allow-uid=1000 \
                --allow-gid=1000
    make
    sudo make install

You'll then need to configure the agent via your local.ini file:

    [elevation]
    method = elevator
    binary = /usr/local/hn-elevator/bin/elevator

Allowing clients
----------------

All clients connecting to the server must encrypt their queries with a GPG key
that's been imported by the server. Generating the keypair can be done with the
same procedure as above (though on the frontend, not the backend). You then need
to import the public key into the agent, like so:

    # on the client
    sudo gpg --gen-key
        Your selection? 1
        What keysize do you want? (2048) 2048
        Key is valid for? (0) 0
        Real name: client
        Email address: client@domain.com
        Comment:
        Change (N)ame, (C)omment, (E)mail or (O)kay/(Q)uit? O
    gpg --export 5FBE20D3 > chroot/tmp/client.pub

    # on the server
    gpg --homedir /var/lib/hypernova/gpg --import chroot/tmp/client.pub
    gpg --homedir /var/lib/hypernova/gpg --sign-key 5FBE20D3
        Really sign? (y/N) y

To ensure that the response isn't being spoofed, similar verification checks
should occur in the client, so we'll need the client to sign the keys of the
server (to demonstrate trust):

    # on the server
    gpg --homedir /var/lib/hypernova/gpg \
        --export 4FBE20D2 > chroot/tmp/server.pub

    # on the client
    gpg --import chroot/tmp/server.pub
    gpg --sign-key 4FBE20D2
        Really sign? (y/N) y

Execution
---------

Since the fanciness is starting to come together, you can now run the server via
a shell script in the python-src directory:

    cd python-src/chroot
    CONFDIR=etc/hypernova/agent bin/hn-agent

Hit Ctrl-C to kill it when you're done.

Making requests
---------------

Since bi-directional encryption and signing now takes place in the server, you
can't query the agent using cURL any more. A primitive client is available,
however.

Requests to the agent (and responses gleaned from it) are formatted in JSON. For
now, you'll need to write the contents of the packet yourself. A basic example
that'd return the load averages would look something like so:

    {
        "action": "status.load_averages"
        "parameters": {
        }
    }

Now, we need to know the fingerprints of both the client and server keys. These
can be obtained using the --fingerprint switch with the gnupg utility:

    gpg --fingerprint

The command should look like the following:

    cd python-src/chroot
    bin/hn-client '{"action":"status.load_averages"}' CLIENTFP SERVERFP

...and the following response should be yielded (though averages may differ ;)):

    {
        "response": {
            "15m": 0.05,
            "1m": 0.0,
            "5m": 0.01
        },
        "status": {
            "error_code": 200,
            "explanation": "",
            "message": "",
            "successful": true
        }
    }
