# Generated by Django 5.1 on 2024-08-29 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("notes", "0004_alter_notes_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notes",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
