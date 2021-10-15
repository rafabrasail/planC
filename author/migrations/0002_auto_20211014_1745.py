# Generated by Django 3.2.3 on 2021-10-14 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='born',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='club',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='favorite_foot',
            field=models.CharField(choices=[('E', 'Left'), ('D', 'Right'), ('B', 'Both')], default='E', max_length=1),
        ),
    ]
