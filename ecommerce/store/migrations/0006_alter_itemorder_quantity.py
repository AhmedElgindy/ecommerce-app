# Generated by Django 4.2.2 on 2023-07-20 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_itemorder_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemorder',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
