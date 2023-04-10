# Generated by Django 4.1 on 2023-03-24 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("researchhub_document", "0050_auto_20221116_2153"),
    ]

    operations = [
        migrations.AddField(
            model_name="researchhubunifieddocument",
            name="is_removed_date",
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name="researchhubunifieddocument",
            name="is_public",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="researchhubunifieddocument",
            name="is_removed",
            field=models.BooleanField(default=False),
        ),
    ]
