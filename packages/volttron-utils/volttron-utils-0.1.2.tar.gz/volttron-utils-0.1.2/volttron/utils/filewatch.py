# -*- coding: utf-8 -*- {{{
# vim: set fenc=utf-8 ft=python sw=4 ts=4 sts=4 et:
#
# Copyright 2020, Battelle Memorial Institute.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This material was prepared as an account of work sponsored by an agency of
# the United States Government. Neither the United States Government nor the
# United States Department of Energy, nor Battelle, nor any of their
# employees, nor any jurisdiction or organization that has cooperated in the
# development of these materials, makes any warranty, express or
# implied, or assumes any legal liability or responsibility for the accuracy,
# completeness, or usefulness or any information, apparatus, product,
# software, or process disclosed, or represents that its use would not infringe
# privately owned rights. Reference herein to any specific commercial product,
# process, or service by trade name, trademark, manufacturer, or otherwise
# does not necessarily constitute or imply its endorsement, recommendation, or
# favoring by the United States Government or any agency thereof, or
# Battelle Memorial Institute. The views and opinions of authors expressed
# herein do not necessarily state or reflect those of the
# United States Government or any agency thereof.
#
# PACIFIC NORTHWEST NATIONAL LABORATORY operated by
# BATTELLE for the UNITED STATES DEPARTMENT OF ENERGY
# under Contract DE-AC05-76RL01830
# }}}

__all__ = ['VolttronHomeFileReloader', 'AbsolutePathFileReloader']

import logging

from watchdog.events import PatternMatchingEventHandler

_log = logging.getLogger(__name__)


class VolttronHomeFileReloader(PatternMatchingEventHandler):
    """
    Extends PatternMatchingEvent handler to watch changes to a singlefile/file pattern within volttron home.
    filetowatch should be path relative to volttron home.
    For example filetowatch auth.json with watch file <volttron_home>/auth.json.
    filetowatch *.json will watch all json files in <volttron_home>
    """
    def __init__(self, filetowatch, callback):
        # Protect from circular reference for file
        from volttron.platform import get_home

        super(VolttronHomeFileReloader, self).__init__([get_home() + '/' + filetowatch])
        _log.debug("patterns is {}".format([get_home() + '/' + filetowatch]))
        self._callback = callback

    def on_any_event(self, event):
        _log.debug("Calling callback on event {}. Calling {}".format(event, self._callback))
        try:
            self._callback()
        except BaseException as e:
            _log.error("Exception in callback: {}".format(e))
        _log.debug("After callback on event {}".format(event))


class AbsolutePathFileReloader(PatternMatchingEventHandler):
    """
    Extends PatternMatchingEvent handler to watch changes to a singlefile/file pattern within volttron home.
    filetowatch should be path relative to volttron home.
    For example filetowatch auth.json with watch file <volttron_home>/auth.json.
    filetowatch *.json will watch all json files in <volttron_home>
    """
    def __init__(self, filetowatch, callback):
        super(AbsolutePathFileReloader, self).__init__([filetowatch])
        self._callback = callback
        self._filetowatch = filetowatch

    @property
    def watchfile(self):
        return self._filetowatch

    def on_any_event(self, event):
        _log.debug("Calling callback on event {}. Calling {}".format(event, self._callback))
        try:
            self._callback(self._filetowatch)
        except BaseException as e:
            _log.error("Exception in callback: {}".format(e))
        _log.debug("After callback on event {}".format(event))