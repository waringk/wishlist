from django.conf import settings
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WishListItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('selected', models.BooleanField(default=False)),
                ('item_url', models.CharField(blank=True, max_length=200, null=True)),
                ('item_description', models.CharField(blank=True, max_length=255, null=True)),
                ('item_photo', models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/images', location='C:\\Users\\dairy\\followish\\media/images/'), upload_to='')),
                ('photo_prefix', models.CharField(blank=True, default='', max_length=10)),
                ('store', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WishListItemTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WishListTagQuantity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extra_tags', models.BooleanField(default=False)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.wishlistitem')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.wishlistitemtag')),
            ],
        ),
        migrations.AddField(
            model_name='wishlistitem',
            name='tags',
            field=models.ManyToManyField(through='home.WishListTagQuantity', to='home.WishListItemTag'),
        ),
        migrations.AddField(
            model_name='wishlistitem',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email')),
                ('username', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
