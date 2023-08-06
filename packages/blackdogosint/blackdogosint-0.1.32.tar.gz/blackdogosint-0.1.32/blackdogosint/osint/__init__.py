# -*- coding: utf-8 -*-
# blackdog import
# extra import
from blackdogosint.osint.log import getLogger
import colored_traceback
# Promote useful stuff to toplevel
import platform
from blackdogosint.osint.toplevel import *
from blackdogosint.osint.log import install_default_handler
from blackdogosint.osint import log
from blackdogosint.osint.config import initialize
from blackdogosint.osint.update import check_automatically
install_default_handler()
initialize()


if not platform.architecture()[0].startswith('64'):
    """Determines if the current Python interpreter is supported by blackdogosint."""
    log.warn_once('blackdogosint does not support 32-bit Python.  Use a 64-bit release.')

check_automatically()