# Generated by Django 4.2.1 on 2023-05-16 15:36

import uuid

import django.db.models.deletion
import django_extensions.db.fields
from django.conf import settings
from django.db import migrations, models

import django_entries.validators


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Entry",
            fields=[
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                (
                    "slug",
                    django_extensions.db.fields.AutoSlugField(
                        blank=True, editable=False, populate_from=["title", "id"]
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Title of entry.",
                        max_length=50,
                        validators=[
                            django_entries.validators.validate_capitalized,
                            django_entries.validators.validate_and_vs_ampersand,
                        ],
                    ),
                ),
                (
                    "excerpt",
                    models.CharField(
                        help_text=(
                            "Short blurb describing entry displayed in list of entries."
                        ),
                        max_length=50,
                        validators=[
                            django_entries.validators.validate_capitalized,
                            django_entries.validators.validate_and_vs_ampersand,
                        ],
                    ),
                ),
                (
                    "content",
                    models.TextField(
                        help_text="Markdown text formatting, e.g. ##, *, 1., -, etc."
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="entries",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Entry",
                "verbose_name_plural": "Entries",
                "ordering": ["-created"],
            },
        ),
    ]