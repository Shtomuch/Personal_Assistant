# Generated by Django 5.1 on 2024-09-02 18:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_customuser_avatar"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="avatar",
        ),
    ]
