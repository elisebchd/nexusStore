import os
from django.conf import settings
from django.core.management.base import BaseCommand
from store.models import ProductImage


class Command(BaseCommand):
    help = 'Update ProductImage records whose stored .svg path has been replaced on disk by a real photo (webp/jpg/jpeg/png).'

    def handle(self, *args, **options):
        updated = 0
        skipped = 0

        for pi in ProductImage.objects.all():
            name = pi.image.name  # e.g. 'products/smartphones_5_view1.svg'
            if not name or not name.lower().endswith('.svg'):
                continue

            base, _ext = os.path.splitext(name)
            found = None
            for candidate_ext in ('webp', 'jpg', 'jpeg', 'png'):
                candidate_name = f'{base}.{candidate_ext}'
                candidate_path = os.path.join(settings.MEDIA_ROOT, candidate_name)
                if os.path.exists(candidate_path):
                    found = candidate_name
                    break

            if found:
                self.stdout.write(f'  Updating {name} -> {found}')
                pi.image.name = found
                pi.save(update_fields=['image'])
                updated += 1
            else:
                skipped += 1

        self.stdout.write(self.style.SUCCESS(f'Done. Updated: {updated}, left as-is (no replacement found): {skipped}'))
