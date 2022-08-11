# Generated by Django 4.0.5 on 2022-07-30 04:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0010_wishlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='OderPlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=100)),
                ('lname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('mobile', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('country', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('zipcode', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('payment_mode', models.CharField(max_length=100)),
                ('grand_total', models.IntegerField()),
                ('payment_id', models.CharField(max_length=100, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('On the way', 'On the way'), ('completed', 'completed')], default='Pending', max_length=100)),
                ('message', models.TextField(null=True)),
                ('tracking_id', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]