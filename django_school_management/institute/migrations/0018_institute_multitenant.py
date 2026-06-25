from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0017_fix_schema_mismatches'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instituteprofile',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='instituteprofile',
            name='is_active',
            field=models.BooleanField(
                default=False,
                help_text='Whether this school is currently active on the platform.',
            ),
        ),
        migrations.AddField(
            model_name='instituteprofile',
            name='slug',
            field=models.SlugField(
                blank=True,
                max_length=120,
                null=True,
                unique=True,
                help_text='URL-safe identifier for this school (auto-generated from name).',
            ),
        ),
    ]
