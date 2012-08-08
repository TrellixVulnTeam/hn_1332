#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Client application package
#
# Copyright (c) 2012 TDM Ltd
#                    Laurent David <laurent@tdm.info>
#
import os
import sys

def debug_setup():
    pydev_src = os.getenv("PYDEVDGB_PATH")
    if pydev_src and os.path.exists(pydev_src):
        if not pydevSrc in sys.path:
            sys.path.append(pydev_src)
            try:
                import pydevd
                remote_debug = os.getenv("PYDEVDGB_REMOTEIP", "127.0.0.1")
                pydevd.settrace(remote_debug, stdoutToServer=True,
                                stderrToServer=True)
            except ImportError:
                pass # We carry on anyway

