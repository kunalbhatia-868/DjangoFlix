# Generated by Django 3.2.9 on 2021-11-24 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='value',
            field=models.IntegerField(blank=True, choices=[(None, 'Unknown'), (1, 'Onw'), (2, 'Two'), (3, 'Three'), (4, 'Four'), (5, 'Five')], null=True),
        ),
    ]
