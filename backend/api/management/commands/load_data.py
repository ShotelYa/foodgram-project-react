# from django.core.management.base import BaseCommand

# from recipes.models import Ingredient

# import csv

# class Command(BaseCommand):
#     help = 'Загрузка базы данных'

#     def handle(self, *args, **options):
#         with open('recipes/data/ingredients.csv', encoding='utf-8') as file:
#             file_reader = csv.reader(file)
#             for row in file_reader:
#                 name, unit = row
#                 Ingredient.objects.get_or_create(name=name, unit=unit)

import json
import os

from recipes.models import Ingredient
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

DATA_ROOT = os.path.join(settings.BASE_DIR, "data")


class Command(BaseCommand):
    help = "loading ingredients from data in json"

    def add_arguments(self, parser):
        parser.add_argument(
            "filename", default="ingredients.json", nargs="?", type=str
        )

    def handle(self, *args, **options):
        try:
            with open(
                os.path.join(
                    DATA_ROOT, options["filename"]), "r", encoding="utf-8"
            ) as f:
                data = json.load(f)
                for ingredient in data:
                    try:
                        Ingredient.objects.create(
                            name=ingredient["name"],
                            measurement_unit=ingredient["measurement_unit"],
                        )
                    except IntegrityError:
                        print(
                            f'Ingredient {ingredient["name"]} '
                            f'{ingredient["measurement_unit"]} '
                            f"already in data base"
                        )
        except FileNotFoundError:
            raise CommandError("the file is missing data")
