# Generated by Django 4.1 on 2023-09-27 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("prediction_market", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="predictionmarketvote",
            name="bet_amount",
            field=models.DecimalField(
                blank=True, decimal_places=10, max_digits=19, null=True
            ),
        ),
    ]
