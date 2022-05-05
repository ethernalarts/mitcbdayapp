
import csv
import re

from django.core.management.base import BaseCommand, CommandError
from sendmail.models import staffDetails


class Command(BaseCommand):
    help = 'Load staff data from a CSV file.'

    def add_arguments(self, parser):
        parser.add_argument('--csv', type = str)

    @staticmethod
    def row_to_dict(row, header):
        if len(row) < len(header):
            row += [''] * (len(header) - len(row))
        return dict([(header[i], row[i]) for i, head in enumerate(header) if head])

    def handle(self, *args, **options):
        m = re.compile(r'content:(\w+)')
        header = None
        models = dict()
        try:
            with open(options['csv']) as csvfile:
                model_data = csv.reader(csvfile)
                for i, row in enumerate(model_data):
                    if max([len(cell.strip()) for cell in row[1:] + ['']]) == 0 and m.match(row[0]):
                        model_name = m.match(row[0]).groups()[0]
                        models[model_name] = []
                        header = None
                        continue

                    if header is None:
                        header = row
                        continue

                    row_dict = self.row_to_dict(row, header)
                    if set(row_dict.values()) == {''}:
                        continue
                    models[model_name].append(row_dict)

        except FileNotFoundError:
            raise CommandError('File "{}" does not exist'.format(options['csv']))

        for data_dict in models.get('staffDetails', []):
            s, created = staffDetails.objects.get_or_create(first_name = data_dict['staff_first_name'], defaults = {
                'middle_name': data_dict['staff_middle_name'].strip(),
                'last_name': data_dict['staff_last_name'].strip(),
                'phone_number': data_dict['staff_mobile_number'],
                'email': data_dict['staff_official_email'].strip(),
                'birth_month': data_dict['staff_birth_month'],
                'birth_day': data_dict['staff_birth_day']
            })

            if created:
                print('Created Staff Details "{}"'.format(s.first_name))                              
        
        print("Import complete")
