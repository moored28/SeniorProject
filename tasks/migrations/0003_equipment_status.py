# Generated by Django 5.0.3 on 2024-03-20 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_remove_equipment_status_alter_crew_crewname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='status',
            field=models.CharField(default='Available', max_length=50),
        ),
    ]
