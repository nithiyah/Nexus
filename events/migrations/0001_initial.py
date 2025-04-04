# Generated by Django 5.1.5 on 2025-01-21 09:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('date', models.DateTimeField()),
                ('location', models.CharField(max_length=255)),
                ('volunteers_needed', models.PositiveIntegerField()),
                ('roles_responsibilities', models.TextField()),
                ('category', models.CharField(choices=[('education', 'Education'), ('social', 'Social Development'), ('senior', 'Senior Citizen')], max_length=50)),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
