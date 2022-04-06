# Generated by Django 2.2.19 on 2022-03-30 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingridient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('measurement_unit', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='posts/')),
                ('text', models.TextField(max_length=100)),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('timing', models.PositiveSmallIntegerField()),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200)),
                ('slug', models.SlugField(null=True, unique=True)),
                ('color', models.CharField(max_length=20, null=True)),
            ],
        ),
    ]