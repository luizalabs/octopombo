from octopombo.slackbot.management.commands.handler import GithubProject
from octopombo.slackbot.management.commands.models import Project


class Command:

    def __init__(self):
        self.commands = {
            "add-repo" : self.add_repo,
            "remove-repo": self.remove_repo,
            "show-prs": self.show_prs,
            "help" : self.help
        }

    def get_prs(self, params):
        try:
            prs = GithubProject(params[0]).get_pull_requests()
            if prs:
                return prs

            return ["Não existe PR's em aberto! :clap: :tada: :gloria:"]
        except Exception:
            return 'Comando com parametros invalidos, digite `@octopombo show-prs help` para verificar como executar.'

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
            ```@octopombo add-repo repository-name approvals-number```\
            '
        try:
            data = {
                'name': params[0],
                'approvals_count': int(params[1])
            }
            channel = params[2]
            project = Project(channel)

            if project.exists(data):
                return """
                    Pruu esse repositório já foi adicionado antes.
                """

            project.save(data)
            return "Pruu pruu Repositório adicionado com sucesso."
        except Exception:
            return 'Comando com parametros inválidos, digite `@octopombo add-repo help` para verificar como executar.'

    def remove_repo(self, params):
        if 'help' in params:
            return 'Para remover um repositório, chame da seguinte forma:\
            ```@octopombo remove-repo repository-name```\
            '
        try:
            name = params[0]
            channel = params[1]
            project = Project(channel)

            project.delete(name)

            return "Pruu pruu Respositório removido com sucesso."
        except Exception:
            return 'Comando com parametros inválidos, digite `@octopombo remove-repo help` para verificar como executar.'

    def show_prs(self, params):
        if 'help' in params:
            return 'Para listar os prs em aberto chame da seguinte forma:\
            ```@Octopombo show-prs (opcional: resume)```\
            '
        
        if 'resume' in params:
            return self.show_resumed_prs([params[1]])

        prs = self.get_prs(params)
        response = [
            '\n{pr.url} - {pr.title}'.format(
                pr=pr
            ) for pr in prs if pr.approved is False
        ]

        return ''.join(response)

    def show_resumed_prs(self, params):
        prs = self.get_prs(params)

        repos = {}
        for pr in prs:
            if not pr.repository_name in repos and pr.approved is False:
                repos[pr.repository_name] = 1
            elif pr.approved is False:
                repos[pr.repository_name] += 1

        def emoji_translate(prs_quantity):
            if prs_quantity <= 3:
                return ':ok_hand:'
            elif prs_quantity > 3 and prs_quantity <= 6:
                return ':grey_exclamation:'
            
            return ':sos:'  

        response = [
            '\n{key} - open prs: {value} {emoji}'.format(
                key=key.capitalize(),
                value=value,
                emoji=emoji_translate(value)
            ) for key, value in repos.items()
        ]

        return ''.join(response)

    def help(self, *args):
        response = "Comandos suportados no momento:\r\n```"

        for command in self.commands:
            response += command + "\r\n"

        response += '```'
        return response
