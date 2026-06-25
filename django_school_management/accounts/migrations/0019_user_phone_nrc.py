import django_school_management.accounts.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_user_institute'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(
                blank=True,
                null=True,
                max_length=20,
                unique=True,
                validators=[django_school_management.accounts.validators.validate_e164_phone],
                help_text='E.164 format, e.g. +260977123456',
            ),
        ),
        migrations.AddField(
            model_name='user',
            name='nrc_number',
            field=models.CharField(
                blank=True,
                null=True,
                max_length=15,
                unique=True,
                validators=[django_school_management.accounts.validators.validate_zambian_nrc],
                help_text='Zambian NRC format: NNNNNN/NN/N, e.g. 123456/78/9',
            ),
        ),
    ]
