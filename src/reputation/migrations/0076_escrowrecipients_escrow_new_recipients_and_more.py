# Generated by Django 4.1 on 2023-04-03 22:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def migrate_recipients(apps, schema_editor):
    Escrow = apps.get_model('reputation', 'Escrow')

    for escrow in Escrow.objects.all().iterator():
        for recipient in escrow.recipients.all().iterator():
            escrow.new_recipients.add(recipient, through_defaults={"amount": escrow.amount_paid})


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("user", "0091_action_is_removed"),
        ("reputation", "0075_merge_20230331_1914"),
    ]

    operations = [
        migrations.CreateModel(
            name="EscrowRecipients",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("updated_date", models.DateTimeField(auto_now=True)),
                (
                    "amount",
                    models.DecimalField(decimal_places=10, default=0, max_digits=19),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="escrow",
            name="new_recipients",
            field=models.ManyToManyField(
                blank=True,
                related_name="target_escrows_new",
                through="reputation.EscrowRecipients",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="escrowrecipients",
            name="escrow",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="reputation.escrow"
            ),
        ),
        migrations.AddField(
            model_name="escrowrecipients",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.RunPython(migrate_recipients),
        migrations.RemoveField(
            model_name="escrow",
            name="new_recipients",
        ),
        migrations.RemoveField(
            model_name="escrow",
            name="recipients",
        ),
        migrations.AddField(
            model_name="escrow",
            name="recipients",
            field=models.ManyToManyField(
                blank=True,
                related_name="target_escrows",
                through="reputation.EscrowRecipients",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
