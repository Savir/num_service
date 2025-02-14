# Generated by Django 5.1.6 on 2025-02-14 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SquaresDiff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(blank=True, db_comment='A unique positive integer representing the primary numeric value our endpoints will calculate "things" for. This is the core of our numeric services.', db_index=True, unique=True)),
                ('occurrences', models.PositiveIntegerField(db_comment='Tracks how many times this number has been used or requested.', default=0)),
                ('last_datetime', models.DateTimeField(auto_now=True, db_comment="Auto-updated timestamp indicating the last time this entry was modified. It will de-facto correspond with the time of the last request, since every time we get a request, the 'occurrences' field gets updated")),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
