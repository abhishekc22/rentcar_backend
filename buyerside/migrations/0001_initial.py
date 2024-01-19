# Generated by Django 4.2.2 on 2024-01-19 06:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
        ("partnerside", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Booking",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("pickupdate", models.DateField()),
                ("returndate", models.DateField()),
                ("total_amount", models.FloatField()),
                ("is_cancelled", models.BooleanField(default=False)),
                ("is_is_reserved", models.BooleanField(default=False)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("canceled", "Canceled"),
                            ("reserved", "Reserved"),
                            ("running", "Running"),
                            ("completed", "Completed"),
                        ],
                        default="reserved",
                        max_length=20,
                    ),
                ),
                (
                    "buyer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.buyerprofile",
                    ),
                ),
                (
                    "car",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="partnerside.rentcar",
                    ),
                ),
            ],
        ),
    ]
