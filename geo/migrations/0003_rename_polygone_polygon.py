# Generated by Django 5.1.2 on 2024-10-25 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0002_rename_polygone_polygone_polygon'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Polygone',
            new_name='Polygon',
        ),
    ]
