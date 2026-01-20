#!/usr/bin/env python3
#
#  update_labels.py
"""
Update status labels on managed repositories.
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
import sys
from tempfile import TemporaryDirectory

# 3rd party
from github3 import GitHub
from github3.exceptions import NotFoundError
from github3.repos import Repository as GitHubRepository
from repo_helper_github import GitHubManager
from repo_helper_github.exceptions import NoSuchRepository, OrganizationError

# this package
from repo_scripts.utils import clone, get_github_token, iter_my_repos, organizations

__all__ = ["update_labels"]


def update_labels(client: GitHub, github_token: str) -> int:
	"""
	Update status labels on managed repositories.

	:param client:
	:param github_token:
	"""

	retv = 0

	for repo in iter_my_repos(client):
		if repo.archived:
			continue
		if repo.private:
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

			manager = GitHubManager(github_token, target_repo=tmpdir, verbose=False, colour=True)

			try:
				retv |= manager.create_labels(org=repo.owner.login in organizations)
			except NotFoundError:
				print("Error: 'master' branch not found")
				retv |= 1
				continue
			except (NoSuchRepository, OrganizationError) as e:
				print(f"Something went wrong: {e}")
				retv |= 1
				continue

	return retv


if __name__ == "__main__":
	token = get_github_token()

	retv = update_labels(GitHub(token=token), github_token=token)
	sys.exit(retv)
