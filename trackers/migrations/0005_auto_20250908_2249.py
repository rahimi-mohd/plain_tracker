# trackers/migrations/0005_auto_20250908_2249.py
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trackers", "0004_alter_tracker_tracker_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="TrackerImage",
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
                ("image", models.ImageField(upload_to="tracker_images/")),
                ("upload_at", models.DateTimeField(auto_now_add=True)),
                (
                    "tracker",
                    models.ForeignKey(
                        on_delete=models.CASCADE,
                        related_name="images",
                        to="trackers.tracker",
                    ),
                ),
            ],
        ),
    ]
