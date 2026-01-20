#!/usr/bin/env python3
#
#  utils.py
"""
Shared utilities.
"""
#
#  Copyright © 2026 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
from subprocess import Popen
from typing import Iterator

# 3rd party
from domdf_python_tools.typing import PathLike
from github3 import GitHub
from github3.repos import ShortRepository
from github3_utils import iter_repos
from southwark.repo import Repo

__all__ = ["clone", "iter_my_repos", "users", "organizations"]


def clone(url: str, dest: PathLike) -> Repo:
	"""
	Clones the given URL and returns the :class:`southwark.repo.Repo` object representing it.

	:param url:
	:param dest:
	"""

	process = Popen(["git", "clone", url, dest])
	process.communicate()
	process.wait()

	return Repo(dest)


users = [
		"domdfcoding",
		]

organizations = [
		"sphinx-toolbox",
		"GunShotMatch",
		"potbanksoftware",
		"python-coincidence",
		"python-formate",
		"repo-helper",
		"PyMassSpec",
		]


def iter_my_repos(client: GitHub) -> Iterator[ShortRepository]:

	yield from iter_repos(client, users, organizations)
