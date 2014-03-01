#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Glances - An eye on your system
#
# Copyright (C) 2014 Nicolargo <nicolas@nicolargo.com>
#
# Glances is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Glances is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# Glances informations
__appname__ = 'glances'
__version__ = "2.0_Alpha"
__author__ = "Nicolas Hennion <nicolas@nicolargo.com>"
__license__ = "LGPL"

# Import system libs
import sys
import os
import gettext
import locale

# Import PsUtil
try:
    from psutil import __version__ as __psutil_version__
except ImportError:
    print('PsUtil module not found. Glances cannot start.')
    sys.exit(1)

# PSutil version
psutil_version = tuple([int(num) for num in __psutil_version__.split('.')])

# Check PsUtil version
# !!! Move this check outside the globals script
# !!! PsUtil is not necessary on client side
# Note: this is not a mistake: psutil 0.5.1 is detected as 0.5.0
if psutil_version < (0, 5, 0):
    print('PsUtil version %s detected.' % '.'.join(psutil_version))
    print('PsUtil 0.5.1 or higher is needed. Glances cannot start.')
    sys.exit(1)  

# Path definitions
work_path = os.path.realpath(os.path.dirname(__file__))
appname_path = os.path.split(sys.argv[0])[0]
sys_prefix = os.path.realpath(os.path.dirname(appname_path))

# Operating system flag
# Note: Somes libs depends of OS
is_BSD = sys.platform.find('bsd') != -1
is_Linux = sys.platform.startswith('linux')
is_Mac = sys.platform.startswith('darwin')
is_Windows = sys.platform.startswith('win')

# i18n
locale.setlocale(locale.LC_ALL, '')
gettext_domain = 'glances'
# get locale directory
i18n_path = os.path.realpath(os.path.join(work_path, '..', 'i18n'))
sys_i18n_path = os.path.join(sys_prefix, 'share', 'locale')
if os.path.exists(i18n_path):
    locale_dir = i18n_path
elif os.path.exists(sys_i18n_path):
    locale_dir = sys_i18n_path
else:
    locale_dir = None
gettext.install(gettext_domain, locale_dir)

# Import Glances libs
from ..core.glances_config import Config as glancesConfig
from ..core.glances_logs import glancesLogs
from ..core.glances_monitor_list import monitorList as glancesMonitorList

# Instances shared between all scripts
# The global instance for the configuration file
glances_config = glancesConfig()
# The global instance for the logs
glances_logs = glancesLogs()
# The global instance for the monitored list
glances_monitors = glancesMonitorList(glances_config)