# Generated by Django 5.1.4 on 2024-12-10 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_incidents_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incidents',
            name='id',
        ),
        migrations.AddField(
            model_name='incidents',
            name='inc_no',
            field=models.AutoField(default=2, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
