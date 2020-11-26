
# -*- coding: utf-8 -*-
from pkg_resources import get_distribution, DistributionNotFound

from py_raiden_proxy.exceptions.base import (
    RaidenAPIException,
    RaidenAPIConflictException,
    InvalidAPIResponse,
)

raise RaidenAPIException


try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "py-raiden-proxy"
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound

