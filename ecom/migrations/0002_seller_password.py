# Generated by Django 3.2.6 on 2021-11-14 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='password',
            field=models.CharField(default=0, max_length=200),
        ),
    ]