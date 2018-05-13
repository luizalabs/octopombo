from octopombo.slackbot.management.commands import commands


class Event:

    def __init__(self, bot):
        self.bot = bot
        self.command = commands.Command()

    def wait_for_event(self):
        events = self.bot.slack_client.rtm_read()

        if events and len(events) > 0:
            for event in events:
                self.parse_event(event)

    def parse_event(self, event):
        if event and 'text' in event and self.bot.bot_id in event['text']:
            self.handle_event(
                event.get('user', ''),
                event['text'].split(self.bot.bot_id)[1].strip().lower(),
                event['channel']
            )

    def get_channel_name(self):
        return self.bot.slack_client.rtm_read()[0].get('subtitle')

    def handle_event(self, user, command, channel):
        try:
            command, *params = command.split(' ')
            params.append(self.get_channel_name())
            if command and channel:
                print(
                    'Received command: ' + command +
                    ' in channel: ' + params[-1] +
                    ' from user: ' + user
                )

                if command == 'show-prs':
                    response = "Pruuuu buscando, aguarde um minuto..."
                    self.bot.slack_client.api_call(
                        'chat.postMessage',
                        channel=channel,
                        text=response,
                        as_user=True
                    )

                response = self.command.handle_command(user, command, params)
                self.bot.slack_client.api_call(
                    'chat.postMessage',
                    channel=channel,
                    text=response,
                    as_user=True
                )
        except Exception as e:
            return 'Ocorreu um erro ao executar o comando: {}'.format(e)
