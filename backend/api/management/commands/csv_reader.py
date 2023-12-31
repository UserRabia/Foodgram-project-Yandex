from django.core.management.base import BaseCommand
import csv

from recipe.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):

        with open('/app/data/ingredients.csv', encoding='utf-8') as r_file:
            file_reader = csv.reader(r_file, delimiter=",")
            ingredient_list = []
            for row in file_reader:
                ingredient_list.append(
                    Ingredient(name=row[0], measurement_unit=row[1])
                )
            Ingredient.objects.bulk_create(ingredient_list)
