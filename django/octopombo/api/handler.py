from collections import namedtuple

from django.conf import settings
from github import Github

from octopombo.api.models import Project


class GithubProject:

    def __init__(self, channel, *args, **kwargs):
        self.github = Github(settings.GITHUB_TOKEN)
        self.channel = channel
        self.company_name = settings.COMPANY_NAME

    def get_pull_requests(self):
        repo = namedtuple(
            'Repositorio', ['url', 'title', 'user_name', 'approved']
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
                        approved=self.get_status(pr, repository.name)
                    )
                )

        return pull_requests

    def get_repositories(self):
        projects = self.get_projects()
        github_projects = []

        for project in projects:
            try:
                repository = '/'.join([self.company_name, project.name])
                repo = self.github.search_repositories(repository)
                github_projects.append(repo[0])
            except Exception:
                print(
                    'Repositorio não encontrado, name:{}'.format(project.name)
                )

        return github_projects

    def get_status(self, pr, repository):
        labels = pr.as_issue().labels
        approved_label = self.get_approved_label(repository)

        if labels:
            for label in labels:
                if self.has_request_changes(pr):
                    return False
                if label.name in (approved_label, 'blocked'):
                    return True

        return False

    def has_request_changes(self, pr):
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

        if len(approves) > 2 and len(request_changes) == 0:
            return False
        return True

    def get_approved_label(self, repository):
        return Project.get_approved_label(self.channel, repository)

    def get_projects(self):
        return Project.get_projects_by_channel(self.channel)
