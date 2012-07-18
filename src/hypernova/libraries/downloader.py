#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Download providers.
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from urllib.request import urlopen

class DownloaderBase:
    """
    Base class for download providers.

    Downloaders provide the ability to download arbitrary files from various
    locations and store them to specific places. All download providers should
    extend this class.
    """

    def download(source, target, **options):
        """
        They provide two parameters by default which may differ, out of
        necessity, for different sources:

        * source - source URL; the format of this string will differ based on
          the downloader being used.
        * target - target file. If this file exists when download() is called,
          any existing content will be removed and the file overwritten.
        * **options any other parameters passed; some providers might use this!

        Expect a return value of None.
        """


class HTTPDownloader(DownloaderBase):
    """
    HTTP download provider.
    """

    def download(source, target, **options):
        with open(target, "wb") as l:
            with urlopen(source) as r:
                while True:
                    chunk = r.read(1024)
                    if len(chunk) == 0:
                        break
                    l.write(chunk)


def download(source, target, provider="HTTP", **options):
    """
    Download a file.

    See the documentation for DownloaderBase.download() for an understanding of
    the parameters you should pass to this function and its return value.
    """

    providers = {
        "HTTP": HTTPDownloader,
    }

    providers[provider].download(source, target, **options)
