# flake8: noqa
# type: ignore

import pkg_resources

from .historical import calc_T0, calc_temp
from .io import load_data_SESL, load_param_file

__version__ = pkg_resources.get_distribution("rhg_compute_tools").version
