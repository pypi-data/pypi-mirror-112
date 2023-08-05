import logging
import re
import time
from collections import namedtuple
from typing import List, NamedTuple, Optional, Union

from ...client import Session
from ...models import Block, BlockFormat, BlockVersion
from .regex import INLINE_CITATION_BLOCK_REGEX
import requests
from collections import namedtuple
from typing import NamedTuple
from ...models import BlockVersion


class LocalMarker(NamedTuple):
    marker: str
    local_path: str
    remote_path: str
    content: Optional[str]


# TODO move to session - easier to mock
def get_model(session, url, model=BlockVersion):
    block = session.get_model(url, model)
    if not block:
        raise ValueError(f"Could not fetch the block {url}")
    return block


def fetch(url: str):
    resp = requests.get(url)
    if resp.status_code >= 400:
        raise ValueError(resp.content)
    return resp.content
