# Generated by Django 5.1.5 on 2025-02-13 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_contact_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='full_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='personnel_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
