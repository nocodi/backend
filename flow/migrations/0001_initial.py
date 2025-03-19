# Generated by Django 5.1.7 on 2025-03-19 14:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("bot", "0001_initial"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Component",
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
                ("name", models.CharField(max_length=255)),
                ("object_id", models.PositiveIntegerField(blank=True, null=True)),
                ("position_x", models.FloatField()),
                ("position_y", models.FloatField()),
                (
                    "content_type",
                    models.ForeignKey(
                        limit_choices_to={"app_label": "components"},
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "prev_component",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="next_components",
                        to="flow.component",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Flow",
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
                (
                    "bot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bot.bot",
                    ),
                ),
                (
                    "start_component",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="flow.component",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Terminal",
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
                ("name", models.CharField(max_length=255)),
                ("operations", models.JSONField(default=dict)),
                ("fields", models.JSONField(default=dict)),
                (
                    "flow",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="flow.flow",
                    ),
                ),
            ],
        ),
    ]
