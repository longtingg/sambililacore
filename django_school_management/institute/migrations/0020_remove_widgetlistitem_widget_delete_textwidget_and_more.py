import django.db.models.deletion
import django_countries.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("academics", "0019_subject_subject_template"),
        ("curriculum", "0004_alter_curriculumsubject_unique_together_and_more"),
        ("institute", "0019_institute_populate_slug_is_active"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="widgetlistitem",
            name="widget",
        ),
        migrations.DeleteModel(
            name="TextWidget",
        ),
        migrations.RemoveConstraint(
            model_name="educationboard",
            name="institute_educationboard_country_name_uniq",
        ),
        # The DB column was already renamed from date_of_estashment → date_of_establishment
        # by migration 0017's RunSQL.  We use SeparateDatabaseAndState here to sync
        # Django's migration state (which still knew the old name) with the current model
        # without issuing any DDL — the column already has the correct name in the DB.
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(
                    model_name="instituteprofile",
                    name="date_of_estashment",
                ),
                migrations.AddField(
                    model_name="instituteprofile",
                    name="date_of_establishment",
                    field=models.DateField(blank=True, null=True),
                ),
            ],
            database_operations=[],
        ),
        migrations.AlterField(
            model_name="city",
            name="code",
            field=models.CharField(
                help_text="Short provincial or regional system area locator code",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="city",
            name="country",
            field=django_countries.fields.CountryField(default="ZM", max_length=2),
        ),
        migrations.AlterField(
            model_name="educationboard",
            name="code",
            field=models.CharField(
                blank=True,
                help_text="Short code for display (e.g., ECZ)",
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="educationboard",
            name="country",
            field=django_countries.fields.CountryField(
                db_index=True, default="ZM", max_length=2
            ),
        ),
        migrations.AlterField(
            model_name="instituteprofile",
            name="country",
            field=django_countries.fields.CountryField(default="ZM", max_length=2),
        ),
        migrations.AlterField(
            model_name="instituteprofile",
            name="current_session",
            field=models.ForeignKey(
                blank=True,
                help_text="Active operational academic year configuration.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="institutes_using_as_current",
                to="academics.academicsession",
            ),
        ),
        migrations.AlterField(
            model_name="instituteprofile",
            name="curriculum",
            field=models.ForeignKey(
                blank=True,
                help_text="Zambian Ministry CBC Pathway / general framework assignment tracking.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="institutes",
                to="curriculum.curriculum",
            ),
        ),
        migrations.AlterField(
            model_name="instituteprofile",
            name="district",
            field=models.CharField(
                blank=True,
                help_text="e.g., Lusaka District, Mbala District, Kasama District",
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="instituteprofile",
            name="institute_type",
            field=models.CharField(
                choices=[
                    ("secondary", "Secondary School (Form 1 to 7)"),
                    ("primary", "Primary School (Grade 1 to 7)"),
                    ("combined", "Combined School (Primary & Secondary Tracks)"),
                ],
                default="secondary",
                help_text="Determines structural workflow terminology across system templates.",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="instituteprofile",
            name="name",
            field=models.CharField(help_text="Official school name", max_length=255),
        ),
        migrations.AlterField(
            model_name="instituteprofile",
            name="site_header",
            field=models.CharField(
                default="SCES — Sambilila Cole Educational System",
                help_text="Will be displayed in SuperAdmin Dashboard",
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="instituteprofile",
            name="site_title",
            field=models.CharField(
                default="SCES | Sambilila Cole Educational System",
                help_text="Title of the application/site",
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="instituteprofile",
            name="super_admin_index_title",
            field=models.CharField(
                default="SCES Administration",
                help_text="Will be displayed in SuperAdmin dashboard listing pages",
                max_length=100,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="educationboard",
            unique_together={("country", "name")},
        ),
        migrations.DeleteModel(
            name="ListWidget",
        ),
        migrations.DeleteModel(
            name="WidgetListItem",
        ),
    ]
