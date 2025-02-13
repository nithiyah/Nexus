# Generated by Django 5.1.5 on 2025-02-13 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_volunteerevent_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.CharField(choices=[('Education', 'Education'), ('Social Development', 'Social Development'), ('Senior Citizen', 'Senior Citizen')], default='Education', max_length=50),
        ),
        migrations.AlterField(
            model_name='volunteerevent',
            name='status',
            field=models.CharField(choices=[('Registered', 'Registered'), ('Waiting List', 'Waiting List')], default='Registered', max_length=20),
        ),
    ]
