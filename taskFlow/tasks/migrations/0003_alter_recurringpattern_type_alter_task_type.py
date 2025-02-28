# Generated by Django 5.1.6 on 2025-02-28 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_alter_task_urgency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recurringpattern',
            name='type',
            field=models.CharField(choices=[('General', 'General'), ('Fun', 'Fun'), ('Work', 'Work'), ('School', 'School'), ('Chore', 'Chore'), ('Other', 'Other')], default='Other', max_length=20),
        ),
        migrations.AlterField(
            model_name='task',
            name='type',
            field=models.CharField(blank=True, choices=[('General', 'General'), ('Fun', 'Fun'), ('Work', 'Work'), ('School', 'School'), ('Chore', 'Chore'), ('Other', 'Other')], default='General', max_length=20, null=True),
        ),
    ]
