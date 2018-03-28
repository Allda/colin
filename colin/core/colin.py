# -*- coding: utf-8 -*-
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
#

from .check_runner import go_through_checks
from .config.config import Config
from .target import Target


def run(name_of_target, group=None, severity=None, tags=None, config_name=None, config_file=None):
    """
    Runs the sanity checks for the target.

    :param name_of_target: str (name of the container or image, dockerfile will be added in the future)
    :param group: str (name of the folder with group of checks, if None, all of them will be checked.)
    :param severity: str (if not None, only those checks will be run -- optional x required x warn ...)
    :param tags: list of str (if not None, the checks will be filtered by tags.)
    :param config_name: str (e.g. fedora; if None, default would be used)
    :param config_file: str (path)
    :return: Results instance
    """
    target = Target(name=name_of_target)
    config = Config(config_name=config_name,
                    config_file=config_file)
    checks_to_run = config.get_checks(group=group,
                                      severity=severity,
                                      tags=tags,
                                      target_type=target.target_type)
    result = go_through_checks(target=target,
                               checks=checks_to_run)
    return result
