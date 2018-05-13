from octopombo.api.models import Project
from octopombo.api.handler import GithubProject


class Command:

    def __init__(self):
        self.commands = {
            "add-repo" : self.add_repo,
            "remove-repo": self.remove_repo,
            "show-prs": self.show_prs,
            "help" : self.help
        }

    def handle_command(self, user, command, params=None):
        if command in self.commands:
            response = self.commands[command](params)
        else:
            if 'has' in command:
                return self.help()
            response = "Pruu errou o comando: " + command + ". " + self.help()

        return response

    def add_repo(self, params):
        if 'help' in params:
            return 'Para adicionar repositorio chame da seguinte forma:\
            ```@octopombo add-repo nome-do-repositorio label-de-aprovado```\
            '
        try:
            project = params[0]
            approved_label = params[1]
            channel = params[2]

            if Project.objects.filter(channel=channel, name=project).exists():
                return """
                    Pruu :pombo-nicolas: esse repositorio já foi adicionado antes.
                """

            Project.objects.create(
                name=project, channel=channel, approved_label=approved_label
            )
            return "Pruu pruu :pombo-nicolas: Respositorio adicionado com sucesso."
        except Exception:
            return 'Comando com parametros invalidos, digite `@octopombo add-repo help` para verificar como executar.'

    def remove_repo(self, params):
        if 'help' in params:
            return 'Para remover um repositorio, chame da seguinte forma:\
            ```@octopombo remove-repo nome-do-repositorio```\
            '
        try:
            project = params[0]
            channel = params[1]

            Project.objects.get(channel=channel, name=project).delete()

            return "Pruu pruu :pombo-nicolas: Respositorio removido com sucesso."
        except Exception:
            return 'Comando com parametros invalidos, digite `@octopombo remove-repo help` para verificar como executar.'

    def show_prs(self, params):
        if 'help' in params:
            return 'Para listar os prs em aberto chame da seguinte forma:\
            ```@Octopombo show-prs```\
            '
        try:
            prs = GithubProject(params[0]).get_pull_requests()

            response = [
                '\n{pr.url} - {pr.title}'.format(
                    pr=pr
                ) for pr in prs if pr.approved is False
            ]

            return ''.join(response)

        except Exception:
            return 'Comando com parametros invalidos, digite `@octopombo show-prs help` para verificar como executar.'

    def help(self, *args):
        response = "Comandos suportados no momento:\r\n```"

        for command in self.commands:
            response += command + "\r\n"

        response += '```'
        return response
