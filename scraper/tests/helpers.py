"""
Module containing some useful functions and resources for testing

Functions:
    create_processed_items(n_items=10)
    make_response_object(fname, callback=None, method='GET', meta=None)
"""
from datetime import datetime, timedelta
import os
import random

from scrapy.http import Request, HtmlResponse

from scraper.scraper.utils import convert_to_datetime


def create_processed_items(n_items=10):
    """Generates fake processed items."""
    now = datetime.now()
    td = timedelta(minutes=3)
    return [{
        'time_of_quake': convert_to_datetime((now - td * i).isoformat()),
        'url': f'https://www.eqx.com/{i + 1:03d}.html',
        'latitude': random.randint(0, 90),
        'longitude': random.randint(-180, 180),
        'depth': random.randint(1, 200),
        'magnitude': random.randint(1, 10),
        'location': f'Location {i + 1}'
    } for i in range(n_items)]


def make_response_object(fname, callback=None, method='GET', meta=None):
    """Creates a Scrapy Response object from a local HTML file.

    Args:
        fname (str): filename of local HTML file; the file must be 
            located inside `scraper/tests/html`
        callback (callable): the function that will be called
        method (str): HTTP method of request that generates response
        meta (dict): the initial values for the Request.meta attribute

    Returns:
        HtmlResponse object
    """
    base_test_dir = os.path.dirname(os.path.abspath(__file__))
    fpath = os.path.join(base_test_dir, 'html', fname)

    # Read HTML file
    file_content = None
    with open(fpath, 'r', encoding='utf-8') as f:
        file_content = f.read()

    # Make a Request object
    request = Request(
        url=f'file:///{fpath}',
        callback=callback,
        method=method,
        meta=meta
    )

    return HtmlResponse(
        url=request.url,
        request=request,
        body=file_content.encode('utf-8')
    )
