from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0016_instituteprofile_curriculum'),
    ]

    operations = [
        # Rename the typo column to the correct name
        migrations.RunSQL(
            sql='ALTER TABLE institute_instituteprofile RENAME COLUMN date_of_estashment TO date_of_establishment',
            reverse_sql='ALTER TABLE institute_instituteprofile RENAME COLUMN date_of_establishment TO date_of_estashment',
        ),
        # Add missing columns
        migrations.AddField(
            model_name='instituteprofile',
            name='province',
            field=models.CharField(
                choices=[
                    ('central', 'Central Province'),
                    ('copperbelt', 'Copperbelt Province'),
                    ('eastern', 'Eastern Province'),
                    ('luapula', 'Luapula Province'),
                    ('lusaka', 'Lusaka Province'),
                    ('muchinga', 'Muchinga Province'),
                    ('northern', 'Northern Province'),
                    ('north_western', 'North-Western Province'),
                    ('southern', 'Southern Province'),
                    ('western', 'Western Province'),
                ],
                default='lusaka',
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name='instituteprofile',
            name='district',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='instituteprofile',
            name='exam_board',
            field=models.CharField(
                choices=[
                    ('ECZ', 'Examinations Council of Zambia (ECZ)'),
                    ('CAMBRIDGE', 'Cambridge Assessment International Education'),
                    ('COMBINED', 'Combined ECZ and Cambridge Syllabus'),
                ],
                default='ECZ',
                max_length=20,
            ),
        ),
    ]
