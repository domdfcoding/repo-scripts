#!/usr/bin/env python3
#
#  protect_master.py
"""
Update branch protection rules for the master branch.
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
import atexit
import sys
from tempfile import TemporaryDirectory

# 3rd party
from domdf_python_tools.paths import PathPlus
from dotenv import dotenv_values
from github3 import GitHub
from github3.exceptions import NotFoundError
from github3.repos import Repository as GitHubRepository
from github3_utils import iter_repos
from repo_helper_bot.updater import clone
from repo_helper_github import GitHubManager
from repo_helper_github.exceptions import NoSuchRepository, OrganizationError

__all__ = ["save_checked_repos"]

config = dotenv_values(".env")

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

data_file = PathPlus("reprotected_repos.json")
if data_file.exists():
	checked_repos = data_file.load_json()
else:
	checked_repos = []


def save_checked_repos():
	data_file.dump_json(checked_repos)


atexit.register(save_checked_repos)

if __name__ == "__main__":
	retv = 0

	token = config["GITHUB_TOKEN"]

	client = GitHub(token=token)
	for repo in iter_repos(client, users, organizations):
		if repo.archived:
			continue
		if repo.private:
			continue
		if f"{repo.owner.login}/{repo.name}" in checked_repos:
			continue

		owner = repo.owner.login
		repository_name = repo.name

		github_repo: GitHubRepository = client.repository(owner, repository_name)

		# Ensure 'repo_helper.yml' exists
		try:
			github_repo.file_contents("repo_helper.yml")
		except NotFoundError:
			print(f"repo_helper.yml not found in the repository {repo.owner.login}/{repo.name}")
			retv |= 1
			continue

		print(repo.full_name)

		with TemporaryDirectory() as tmpdir:

			# Clone to tmpdir
			clone(repo.html_url, tmpdir)

			manager = GitHubManager(token, target_repo=tmpdir, verbose=False, colour=True)

			try:
				retv |= manager.protect_branch("master", org=repo.owner.login in organizations)
			except NotFoundError:
				print("Error: 'master' branch not found")
				retv |= 1
				continue
			except (NoSuchRepository, OrganizationError) as e:
				print(f"Something went wrong: {e}")
				retv |= 1
				continue

			checked_repos.append(f"{repo.owner.login}/{repo.name}")

	sys.exit(retv)
