# Generated by Django 4.1 on 2023-06-28 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_recieving_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dealer',
            name='slug',
            field=models.SlugField(),
        ),
        migrations.AlterField(
            model_name='recieving',
            name='type',
            field=models.CharField(choices=[('BORROW', 'B'), ('PAID', 'P')], max_length=6),
        ),
    ]
