import json
import logging
import os
from pathlib import Path

from django.core.management.base import BaseCommand
from django.apps import apps


class Command(BaseCommand):
    help = 'Load fixture data for models'
    logger = logging.getLogger(__name__)

    def handle(self, *args, **options):
        logging.debug('Старт')
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug("Начинаю загрузку фикстур")

        Ingredient = apps.get_model('core', 'Ingredient')

        current_path = Path(os.path.dirname(os.path.realpath(__file__)))
        json_path = os.path.join(current_path, '../../../data/ingredients.json')

        with open(json_path, encoding='utf-8') as f:
            ingredients = json.load(f)

        count_before = Ingredient.objects.count()
        for item in ingredients:
            user, _ = Ingredient.objects.get_or_create(
                name=item.get('name'),
                measurement_unit=item.get('measurement_unit')
            )
        count_after = Ingredient.objects.count() - count_before
        self.logger.debug(f"Успешно загружено - {count_after} объектов!")
