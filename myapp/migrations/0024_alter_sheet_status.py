# Generated by Django 4.2.8 on 2024-11-20 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0023_profile_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sheet',
            name='status',
            field=models.CharField(choices=[('Đúng Giờ', 'Đúng Giờ'), ('Đến Muộn', 'Đến Muộn')], default='Đúng Giờ', max_length=20),
        ),
    ]
