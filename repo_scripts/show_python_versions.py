#!/usr/bin/env python3
#
#  show_python_versions.py
"""
Show supported Python versions for each repository.
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
from packaging.version import Version
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
		python_versions = []
		if "python_versions" in raw_config_vars:
			for v in raw_config_vars["python_versions"]:
				v = str(v)
				if v.startswith("pypy"):
					continue
				python_versions.append(Version(v))

		if python_versions:
			min_version = min(python_versions)
			max_version = max(python_versions)
			if min_version >= Version("3.7") and max_version >= Version("3.12"):
				continue
			print(repo.full_name)
			print(' ', min_version, max_version)
		else:
			print(repo.full_name)
			print("  No python versions set")

		# try:
		# 	retv |= update_repository(repo_dict)
		# except Exception as e:
		# 	traceback.print_exc()
		# 	retv |= 1

	# sys.exit(retv)
