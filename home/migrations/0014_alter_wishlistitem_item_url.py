# Generated by Django 4.0.1 on 2022-03-09 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_wishlistitem_store'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlistitem',
            name='item_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
