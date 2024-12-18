# Generated by Django 5.1 on 2024-11-07 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_topicletter_alter_profile_cccd_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topicletter',
            old_name='ten',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='letter',
            name='status',
            field=models.CharField(choices=[('Đang xử lý', 'Đang xử lý'), ('Đã xử lý', 'Đã xử lý')], default='Đang xử lý', max_length=30),
        ),
    ]
