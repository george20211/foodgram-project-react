# Generated by Django 2.2.19 on 2022-03-31 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recept', '0008_auto_20220331_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', to='recept.Tag'),
        ),
    ]
