from django.db import migrations
from django.utils.text import slugify


def populate_slug_and_is_active(apps, schema_editor):
    """
    Use values() to fetch only the fields we need, avoiding the pre-existing
    migration-state/DB mismatch on the date_of_estashment / date_of_establishment column
    (migration 0017 renamed it via RunSQL without an AlterField, leaving historical
    model state out of sync).
    """
    InstituteProfile = apps.get_model('institute', 'InstituteProfile')
    used_slugs = set()

    for row in InstituteProfile.objects.values('id', 'active', 'name', 'slug'):
        new_is_active = bool(row['active'])
        new_slug = row['slug']

        if not new_slug and row['name']:
            base = slugify(row['name'])[:100] or 'school'
            candidate = base
            n = 1
            while candidate in used_slugs:
                candidate = f'{base}-{n}'
                n += 1
            used_slugs.add(candidate)
            new_slug = candidate
        elif new_slug:
            used_slugs.add(new_slug)

        InstituteProfile.objects.filter(id=row['id']).update(
            is_active=new_is_active,
            slug=new_slug,
        )


def reverse_populate(apps, schema_editor):
    InstituteProfile = apps.get_model('institute', 'InstituteProfile')
    InstituteProfile.objects.all().update(is_active=False, slug=None)


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0018_institute_multitenant'),
    ]

    operations = [
        migrations.RunPython(populate_slug_and_is_active, reverse_populate),
    ]
