from octopombo.aws.s3 import S3Manager


class Project:

    def __init__(self, channel, *args, **kwargs):
        self.s3 = S3Manager()
        self.channel = channel
        self.filename = '.'.join([channel, 'json'])

    def save(self, data):
        try:
            file_data = self.s3.get(self.filename)
            file_data.append(data)
        except Exception:
            file_data = [data]
        self.s3.upload(file_data, self.filename)

    def exists(self, data):
        try:
            file_data = self.s3.get(self.filename)
            for repo in file_data:
                if repo.get('name') == data.get('name'):
                    return True
            return False
        except Exception:
            return False

    def delete(self, project_name):
        try:
            file_data = self.s3.get(self.filename)
            for repo in file_data:
                if repo.get('name') == project_name:
                    file_data.remove(repo)
            self.s3.upload(file_data, self.filename)
        except Exception:
            print('Falha ao remover repositorio')

    def get_approvals_count(self, project_name):
        try:
            file_data = self.s3.get(self.filename)
            for repo in file_data:
                if repo.get('name') == project_name:
                    return repo.get('approvals_count')
        except Exception:
            print("Falha ao recuperar o arquivo")

    def get_projects(self):
        projects = []
        try:
            file_data = self.s3.get(self.filename)
            for repo in file_data:
                projects.append(repo.get('name'))
        except Exception:
            print("Falha ao recuperar o arquivo")

        return projects
