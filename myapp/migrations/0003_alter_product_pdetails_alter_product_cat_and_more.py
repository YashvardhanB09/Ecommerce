# Generated by Django 5.0.4 on 2024-05-05 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_product_cat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Pdetails',
            field=models.CharField(max_length=200, verbose_name='Details'),
        ),
        migrations.AlterField(
            model_name='product',
            name='cat',
            field=models.IntegerField(choices=[(1, 'shoes'), (2, 'mobile'), (3, 'cloths')], verbose_name='Catagory'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Is_Available'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=20, verbose_name='product Name'),
        ),
    ]
