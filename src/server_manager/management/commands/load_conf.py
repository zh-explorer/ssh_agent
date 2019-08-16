from django.core.management.base import BaseCommand, CommandError
import os
from .config_decode import load_conf_file


class Command(BaseCommand):
    help = "load server config json"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--config", required=True)

    def handle(self, *args, **options):
        filename = options["config"]
        if not os.path.exists(filename):
            raise CommandError("config file not find")
        load_conf_file(filename)
