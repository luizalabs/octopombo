from collections import namedtuple

from django.conf import settings
from github import Github

from octopombo.slackbot.management.commands.models import Project


class GithubProject:

    def __init__(self, channel, *args, **kwargs):
        self.github = Github(settings.GITHUB_TOKEN)
        self.channel = channel
        self.company_name = settings.COMPANY_NAME
        self.project = Project(self.channel)

    def get_pull_requests(self):
        repo = namedtuple(
            'Repositorio', ['url', 'title', 'user_name', 'approved', 'repository_name']
        )
        repositories = self.get_repositories()
        pull_requests = []

        for repository in repositories:
            for pr in repository.get_pulls():
                pull_requests.append(
                    repo(
                        url=pr.html_url,
                        title=pr.title,
                        user_name=pr.user.login,
                        approved=self.get_status(pr, repository.name),
                        repository_name=repository.name
                    )
                )

        return pull_requests

    def get_repositories(self):
        projects = self.get_projects()
        github_projects = []

        for project in projects:
            try:
                repository = '/'.join([self.company_name, project])
                repo = self.github.search_repositories(repository)
                github_projects.append(repo[0])
            except Exception:
                print(
                    'Repositorio não encontrado, name:{}'.format(project)
                )

        return github_projects

    def get_status(self, pr, repository):
        labels = pr.as_issue().labels
        approvals_count = self.get_approvals_count(repository)

        if labels:
            for label in labels:
                if self.has_request_changes(pr, approvals_count):
                    return False
                if label.name in ('approved', 'blocked'):
                    return True

        return False

    def has_request_changes(self, pr, approvals_count):
        approves = []
        request_changes = []
        for review in pr.get_reviews():
            if review.state == 'CHANGES_REQUESTED':
                request_changes.append(review.user.login)
                if review.user.login in approves:
                    approves.remove(review.user.login)
            else:
                approves.append(review.user.login)
                if review.user.login in request_changes:
                    request_changes.remove(review.user.login)

            approves = list(set(approves))
            request_changes = list(set(request_changes))

        if len(approves) >= int(approvals_count) and len(request_changes) == 0:
            return False
        return True

    def get_approvals_count(self, repository):
        return self.project.get_approvals_count(repository)

    def get_projects(self):
        return self.project.get_projects()
