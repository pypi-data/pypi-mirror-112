# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division

import os

from six.moves import configparser

registered_configs = {}


def register_config(section, function):
    """Registers a configuration section.

    Arguments:
        section(str): Named configuration section
        function(callable): Function invoked with a dictionary of
            ``{option: value}`` for the entries in the section.
    """
    registered_configs[section] = function


def initialize():
    """Read the configuration files."""
    from blackdogosint.osint.log import getLogger
    log = getLogger(__name__)

    xdg_config_home = (
        os.environ.get('XDG_CONFIG_HOME') or
        os.path.expanduser('~/.config')
    )

    c = configparser.ConfigParser()
    c.read([
        '/etc/pwn.conf',
        os.path.join(xdg_config_home, 'pwn.conf'),
        os.path.expanduser('~/.pwn.conf'),
    ])

    for section in c.sections():
        if section not in registered_configs:
            log.warn('Unknown configuration section %r' % section)
            continue
        settings = dict(c.items(section))
        registered_configs[section](settings)
