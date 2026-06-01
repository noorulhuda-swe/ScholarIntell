import csv, os
from django.core.management.base import BaseCommand
from django.conf import settings
from scholarships.models import Scholarship

class Command(BaseCommand):
    help = 'Import scholarships from CSV'

    def handle(self, *args, **kwargs):
        csv_path = os.path.join(settings.BASE_DIR, 'data', 'scholarships.csv')
        created_count = 0
        updated_count = 0

        with open(csv_path, encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row = {k.strip(): (v.strip() if v else '') for k, v in row.items()}
                fully_funded = row.get('Fully_Funded?', '').lower() == 'yes'

                obj, created = Scholarship.objects.update_or_create(
                    scholarship_id=row.get('Scholarship_ID', '').strip(),
                    defaults={
                        'name':                  row.get('Scholarship_Name', ''),
                        'description':           row.get('Description', ''),
                        'level':                 row.get('Level', ''),
                        'host_institution':      row.get('Host_Institution', ''),
                        'host_country':          row.get('Host_Country', ''),
                        'field_of_study':        row.get('Feild_Of_Study', ''),
                        'fully_funded':          fully_funded,
                        'what_it_covers':        row.get('What_It_Covers', ''),
                        'special_requirements':  row.get('Special_Requirements', ''),
                        'application_link':      row.get('Application_Link', ''),
                        'open_date':             row.get('Application_Open_Date', ''),
                        'deadline':              row.get('Application_Deadline', ''),
                        'source_website':        row.get('Source_Website', ''),
                        'language_requirements': row.get('Language_Requirements', ''),
                        'notes':                 row.get('Notes', ''),
                        'last_verified':         row.get('Last_Verified_Date', ''),
                    }
                )
                if created: created_count += 1
                else: updated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done! {created_count} created, {updated_count} updated.'
        ))
