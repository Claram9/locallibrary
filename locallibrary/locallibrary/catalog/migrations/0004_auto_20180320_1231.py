# Generated by Django 2.0.3 on 2018-03-20 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20180319_1358'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='sumary',
            new_name='summary',
        ),
    ]
