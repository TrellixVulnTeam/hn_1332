#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Process library
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

import os
import resource
import signal
import sys

# Max file descriptors per process
#
# Should the developer not pass a value for the max_fd parameter and
# resource.getrlimit() return RLIM_INFINITY, we'll fall back on this value. It's
# a sane default that _may_ have been changed on some systems as a performance
# tweak. You can check it with:
#
#     ulimit -n
MAX_FD = 1024

def daemonise(std_stream_target=None, work_dir=None, umask=None, max_fd=None,
              keep_fds=[]):
    """
    Daemonise a process.

    Lots of work takes place in this method to ensure that the process is
    isolated entirely from its shell:

    * Fork once to detach from the shell and hand control back to the parent
      process
    * Become the leader of the new session and process group, which now has no
      controlling terminal.
    * Ignore hangup signals from zombies to prevent any child processes from
      crashing or exiting prematurely.
    * Fork a second time to orphan the process (causing init to take ownership),
      thus preventing acquiring a controlling terminal in the future.
    * Close all open file descriptors and switch directories to allow unmounting
      any filesystems we might be chrooted in.
    """

    if not std_stream_target:
        std_stream_target = os.devnull

    if not work_dir:
        work_dir = '/'

    if not umask:
        umask = 0

    if not max_fd:
        max_fd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
        if max_fd == resource.RLIM_INFINITY:
            max_fd = MAX_FD

    # Exit the first process
    pid = os.fork()
    if pid:
        os._exit(0)

    # Become the session and process leader; drop terminal
    os.setsid()

    # Ignore SIGHUPs whilst fighting a possible zombie invasion
    signal.signal(signal.SIGHUP, signal.SIG_IGN)
    pid = os.fork()
    if pid:
        os._exit(0)

    # Prevent the ugly solution of preventing unmounting a volume
    os.chdir(work_dir)
    os.umask(umask)

    # Close file descriptors
    #
    # os.close() raises an OSError when we try to close an FD that wasn't open,
    # but since we have no way of determining which FDs are in use, that's
    # tough.
    for fd in range(0, max_fd):
        if fd not in keep_fds:
            try:
                os.close(fd)
            except OSError:
                pass

    # Redirect stdin, stdout (1) and stderr (2)
    os.open(std_stream_target, os.O_RDWR)
    os.dup2(0, 1)
    os.dup2(0, 2)

    return True
