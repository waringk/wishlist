# Generated by Django 4.0.1 on 2022-02-12 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_wishlistitem_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlistitem',
            name='tags',
            field=models.ManyToManyField(through='home.WishListTagQuantity', to='home.WishListItemTag'),
        ),
    ]