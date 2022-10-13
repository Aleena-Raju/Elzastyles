# Generated by Django 4.0.7 on 2022-09-28 11:31

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_alter_category_options_alter_category_cat_image'),
        ('products', '0002_remove_product_image_product_image1_product_image2_and_more'),
        ('extra', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfferProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.IntegerField(default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99)])),
                ('is_active', models.BooleanField(default=True)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='OfferCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.IntegerField(default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99)])),
                ('is_active', models.BooleanField(default=True)),
                ('category', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='category.category')),
            ],
        ),
    ]