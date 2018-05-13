from octopombo.slackbot.management.commands import bot

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Starts the bot for the first'


    def handle(self, *args, **options):
        bot.Bot()
