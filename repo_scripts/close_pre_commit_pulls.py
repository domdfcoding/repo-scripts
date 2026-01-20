#!/usr/bin/env python3
#
#  close_pre_commit_pulls.py
"""
Close pre-commit.ci pull requests on managed repositories.
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

# 3rd party
from github3 import GitHub
from github3.pulls import ShortPullRequest
from github3.repos import Repository as GitHubRepository

# this package
from repo_scripts.utils import get_github_token, iter_my_repos

if __name__ == "__main__":
	retv = 0

	client = GitHub(token=get_github_token())
	for repo in iter_my_repos(client):
		if repo.archived:
			continue
		if repo.private:
			continue

		owner = repo.owner.login
		repository_name = repo.name

		github_repo: GitHubRepository = client.repository(owner, repository_name)

		# TODO: check if managed (has repo-helper.yml)

		pull_requests = list(github_repo.pull_requests(state="open", head="pre-commit-ci-update-config"))
		if not pull_requests:
			continue

		# assert len(pull_requests) == 1, repo.full_name
		pr: ShortPullRequest = pull_requests[0]
		if pr.title != "[pre-commit.ci] pre-commit autoupdate":
			continue
		print(repo.full_name, pr, pr.close())

	sys.exit(retv)
