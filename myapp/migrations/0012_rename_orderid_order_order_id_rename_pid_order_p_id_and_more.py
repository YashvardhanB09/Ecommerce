# Generated by Django 5.0.4 on 2024-05-11 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='orderid',
            new_name='order_id',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='pid',
            new_name='p_id',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='userid',
            new_name='user_id',
        ),
    ]
