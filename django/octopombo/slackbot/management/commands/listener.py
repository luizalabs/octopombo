from django.core.management.base import BaseCommand

from octopombo.slackbot.management.commands import bot


class Command(BaseCommand):
    help = 'Starts the bot for the first'

    def handle(self, *args, **options):
        bot.Bot()
