# Generated by Django 2.2.19 on 2022-03-31 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recept', '0006_auto_20220331_1400'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='timing',
            new_name='cooking_time',
        ),
    ]
