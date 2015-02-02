# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import configparser
from gns3.qt import QtCore


import logging
log = logging.getLogger(__name__)


class LocalServerConfig:

    """
    Local server configuration.
    """

    def __init__(self):

        self._config = configparser.ConfigParser()
        if sys.platform.startswith("win"):
            filename = "server.ini"
        else:
            filename = "server.conf"
        self._config_file = os.path.join(os.path.dirname(QtCore.QSettings().fileName()), filename)
        try:
            # create the config file if it doesn't exist
            open(self._config_file, 'a').close()
        except OSError as e:
            log.error("Could not create the local server configuration {}: {}".format(self._config_file, e))
        self.readConfig()

    def readConfig(self):
        """
        Read the configuration file.
        """

        try:
            self._config.read(self._config_file)
        except configparser.Error as e:
            log.error("Could not read the local server configuration {}: {}".format(self._config_file, e))

    def writeConfig(self):
        """
        Write the configuration file.
        """

        try:
            with open(self._config_file, 'w') as fp:
                self._config.write(fp)
        except configparser.Error as e:
            log.error("Could not write the local server configuration {}: {}".format(self._config_file, e))

    def loadSettings(self, section, default_settings, types):
        """
        Get all the settings from a given section.

        :param section: section name
        :param default_settings: setting names and default values (dict)
        :param types: setting types (dict)

        :returns: settings (dict)
        """

        if section not in self._config:
            self._config[section] = {}

        settings = {}
        for name, default in default_settings.items():
            if types[name] is int:
                settings[name] = self._config[section].getint(name, default)
            elif types[name] is bool:
                settings[name] = self._config[section].getboolean(name, default)
            elif types[name] is float:
                settings[name] = self._config[section].getfloat(name, default)
            else:
                settings[name] = self._config[section].get(name, default)

        # sync with the config file
        self.saveSettings(section, settings)
        return settings

    def saveSettings(self, section, settings):
        """
        Save all the settings in a given section.

        :param section: section name
        :param settings: settings to save (dict)
        """

        if section not in self._config:
            self._config[section] = {}

        for name, value in settings.items():
            self._config[section][name] = str(value)
        self.writeConfig()

    @staticmethod
    def instance():
        """
        Singleton to return only on instance of LocalServerConfig.

        :returns: instance of Config
        """

        if not hasattr(LocalServerConfig, "_instance"):
            LocalServerConfig._instance = LocalServerConfig()
        return LocalServerConfig._instance
