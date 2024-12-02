# Generated by Django 4.2.8 on 2024-10-09 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_profile_address_alter_profile_dob_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='profile',
            name='dob',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='sheet',
            name='checkout',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
