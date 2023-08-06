"""This module contains utilities for litcorpt API"""

import os
import re
import logging

from itertools import cycle

from urllib.parse import urlparse

from pathlib import Path
from dotenv import load_dotenv

import requests

logger: logging.Logger = logging.getLogger(__name__)

def spinning_wheel():
    """Print a frame of a spinning wheel"""
    for frame in cycle(r'-\|/'):
        print(f'\b{frame}', sep='', end='', flush=True)
        yield


def download_file(url: str, dstdir: str = '.', filename: str = None):
    """Download file from url and save as dstdir/filepath. If filename is omitted
       check if http requests gives a filename, otherwise use url path
       filename and save at dstdir. This do not create the
       dir structure, that must be created beforehand.

    Input:
        url (str): Url to download
        filename (str): Filename to download to. If missing try to figure out.
        dstdir (str): Directory to store data

    Outputs:
        filepath (str): Filepath to downloaded file
        filesize (int): Ammount of bytes downloaded
    """

    with requests.get(url, stream=True) as req:
        req.raise_for_status()
        # Check if filepath was given, otherwise find from request
        if filename is None:
            # Name from http headers
            if 'content-disposition' in req.headers:
                disposition = req.headers['content-disposition']
                filename = re.findall("filepath=(.+)", disposition)[0]

            # We got a redirect
            if req.history:
                hist_req = req.history[0]
                if hist_req.status_code == 302:
                    url = hist_req.headers.get('Location', url)

            # Name from url path
            if not filename:
                filename = urlparse(url).path.split('/')[-1]

        # Check filesize (only works when stream=False)
        expected_filesize = 0
        if 'Content-Length' in req.headers:
            expected_filesize = int(req.headers['Content-Length'])

        filepath = os.path.join(dstdir, filename)
        logger.info('Downloading %s to %s', url, filepath)
        if expected_filesize > 0:
            logger.info('Expected content size %s bytes', expected_filesize)

        filesize = 0
        with open(filepath, 'wb') as f:
            spinning_wheel_frame = spinning_wheel()
            for chunk in req.iter_content(chunk_size=None):
                if chunk:
                    next(spinning_wheel_frame)
                    filesize += len(chunk)
                    f.write(chunk)

    return filepath, filesize


def get_corpus_datapath() -> Path:
    """Returns a Path to CORPUS_DATAPATH"""
    load_dotenv()
    corpus_datapath_default: str = '~/litcorpt_data'
    corpus_datapath: Path = Path(os.getenv('CORPUS_DATAPATH',
                                           corpus_datapath_default))
    corpus_datapath = corpus_datapath.expanduser()
    corpus_datapath.mkdir(parents=True, exist_ok=True)

    return corpus_datapath


def get_corpus_url() -> str:
    """Returns a URL string to CORPUS source """
    # pylint: disable=line-too-long
    load_dotenv()
    corpus_url_default: str = "https://github.com/igormorgado/litcorpt_data/archive/refs/heads/main.zip"
    corpus_url = os.getenv('CORPUS_URL', corpus_url_default)

    return corpus_url
