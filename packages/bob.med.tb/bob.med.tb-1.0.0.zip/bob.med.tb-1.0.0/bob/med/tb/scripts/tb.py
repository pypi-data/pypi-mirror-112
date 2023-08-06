#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""The main entry for bob med tb (click-based) scripts."""

import os
import sys
import time
import tempfile
import urllib.request

import pkg_resources
import click
from click_plugins import with_plugins
from tqdm import tqdm

from bob.extension.scripts.click_helper import AliasedGroup

import logging
logger = logging.getLogger(__name__)

def download_to_tempfile(url, progress=False):
    """Downloads a file to a temporary named file and returns it

    Parameters
    ----------

    url : str
        The URL pointing to the file to download

    progress : :py:class:`bool`, Optional
        If a progress bar should be displayed for downloading the URL.


    Returns
    -------

    f : tempfile.NamedTemporaryFile
        A named temporary file that contains the downloaded URL

    """

    file_size = 0
    response = urllib.request.urlopen(url)
    meta = response.info()
    if hasattr(meta, "getheaders"):
        content_length = meta.getheaders("Content-Length")
    else:
        content_length = meta.get_all("Content-Length")

    if content_length is not None and len(content_length) > 0:
        file_size = int(content_length[0])

    progress &= bool(file_size)

    f = tempfile.NamedTemporaryFile()

    with tqdm(total=file_size, disable=not progress) as pbar:
        while True:
            buffer = response.read(8192)
            if len(buffer) == 0:
                break
            f.write(buffer)
            pbar.update(len(buffer))

    f.flush()
    f.seek(0)
    return f

@with_plugins(pkg_resources.iter_entry_points("bob.med.tb.cli"))
@click.group(cls=AliasedGroup)
def tb():
    """Active Tuberculosis Detection On CXR commands."""