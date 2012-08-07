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
    pydevSrc = os.getenv("PYDEVDGB_PATH")
    if pydevSrc != None and  os.path.exists(pydevSrc): 	
        if not pydevSrc in sys.path:
            sys.path.append(pydevSrc)
            try:
                import pydevd
                remotedebg = os.getenv("PYDEVDGB_REMOTEIP", "127.0.0.1")
                pydevd.settrace(remotedebg, stdoutToServer=True, stderrToServer=True)
            except ImportError:
                pass # We carry on anyway
