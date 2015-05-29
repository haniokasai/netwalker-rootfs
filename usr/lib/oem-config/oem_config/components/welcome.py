# -*- coding: UTF-8 -*-

# Copyright (C) 2005 Canonical Ltd.
# Written by Colin Watson <cjwatson@ubuntu.com>.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from oem_config.filteredcommand import FilteredCommand

class Welcome(FilteredCommand):
    def prepare(self, unfiltered=False):
        questions = ['welcome/welcome']
        return (['/usr/lib/oem-config/welcome/welcome'],
                questions)

    def ok_handler(self):
        if self.current_question is not None:
            self.preseed(self.current_question, 'yes')
        FilteredCommand.ok_handler(self)
