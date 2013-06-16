#! /usr/bin/python

# Copyright 2013 Martin Pool <mbp@sourcefrog.net>
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

"""Self-test and example for shellliketests."""

import unittest

import shellliketests
from shellliketests import run_script


class TestShellLikeTests(unittest.TestCase):

    def test_echo(self):
        run_script(self, """
            $ echo hello world
            hello world
            """)

    def test_file_manipulation(self):
        run_script(self, """
            $ echo hello > afile
            $ cat afile
            hello
            $ rm afile
            """)


if __name__ == '__main__':
    unittest.main()
