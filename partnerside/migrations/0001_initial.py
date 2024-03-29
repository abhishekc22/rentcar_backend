import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Rentcar",
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
                ("carname", models.CharField(max_length=20)),
                ("location", models.CharField(max_length=100)),
                ("enginetype", models.CharField(max_length=20)),
                (
                    "price",
                    models.PositiveIntegerField(
                        null=True,
                        validators=[django.core.validators.MinValueValidator(1)],
                    ),
                ),
                ("car_type", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "is_blocked",
                    models.BooleanField(blank=True, default=False, null=True),
                ),
                ("document", models.ImageField(blank=True, null=True, upload_to="")),
                ("carimage1", models.ImageField(blank=True, null=True, upload_to="")),
                ("carimage2", models.ImageField(blank=True, null=True, upload_to="")),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "partner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.parnterorofile",
                    ),
                ),
            ],
        ),
    ]
