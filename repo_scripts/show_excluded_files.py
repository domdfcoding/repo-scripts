#!/usr/bin/env python3
#
#  show_excluded_files.py
"""
Show files or sections in ``tox.ini`` excluded from ``repo-helper``.
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
from collections.abc import Mapping
from typing import Any

# 3rd party
from dotenv import dotenv_values
from github3 import GitHub
from github3.exceptions import NotFoundError
from github3.repos.contents import Contents
from ruamel.yaml import YAML

# this package
from repo_scripts.utils import iter_my_repos

config = dotenv_values(".env")

if __name__ == "__main__":

	for repo in iter_my_repos(GitHub(token=config["GITHUB_TOKEN"])):
		if repo.archived:
			continue

		if repo.name == "contributing" or "-stubs" in repo.name:
			continue

		repo_dict = {
				"id": repo.id,
				"name": repo.name,
				"html_url": repo.html_url,
				"owner": {"login": repo.owner.login},
				}
		try:
			c: Contents = repo.file_contents("repo_helper.yml", "master")
		except NotFoundError:
			continue

		raw_config_vars: Mapping[str, Any] = YAML(typ="safe", pure=True).load(c.decoded.decode("UTF-8"))
		exclude_files = raw_config_vars.get("exclude_files", [])
		tox_unmanaged = raw_config_vars.get("tox_unmanaged", [])
		if exclude_files or tox_unmanaged:
			print(repo.full_name)

			if exclude_files:
				print(f"exclude_files = {exclude_files!r}")
			if tox_unmanaged:
				print(f"tox_unmanaged = {tox_unmanaged!r}")

			print()

	# sys.exit(retv)
