# Generated by Django 4.0.5 on 2022-08-03 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_oderitems_image_oderitems_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='oderitems',
            name='image',
        ),
        migrations.RemoveField(
            model_name='oderitems',
            name='total',
        ),
        migrations.AlterField(
            model_name='oderitems',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.product'),
        ),
    ]
