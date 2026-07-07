import os

from django.conf import settings
from django.db import migrations


def fix_svg_to_webp(apps, schema_editor):
    ProductImage = apps.get_model('store', 'ProductImage')

    for pi in ProductImage.objects.all():
        name = pi.image.name if pi.image else ''
        if not name or not name.lower().endswith('.svg'):
            continue

        base, _ext = os.path.splitext(name)
        for candidate_ext in ('webp', 'jpg', 'jpeg', 'png'):
            candidate_name = f'{base}.{candidate_ext}'
            candidate_path = os.path.join(settings.MEDIA_ROOT, candidate_name)
            if os.path.exists(candidate_path):
                pi.image.name = candidate_name
                pi.save(update_fields=['image'])
                break


def noop_reverse(apps, schema_editor):
    # Not reversible: we don't know which rows were originally svg vs webp.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(fix_svg_to_webp, noop_reverse),
    ]
