# Generated by Django 5.1.5 on 2025-03-03 11:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_alter_event_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='duration_hours',
            field=models.FloatField(default=0),
        ),
        migrations.CreateModel(
            name='VolunteerParticipation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours_contributed', models.FloatField(default=0)),
                ('date_participated', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participations', to='events.event')),
                ('volunteer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
