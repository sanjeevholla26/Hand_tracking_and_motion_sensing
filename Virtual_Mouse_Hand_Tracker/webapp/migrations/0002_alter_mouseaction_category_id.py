# Generated by Django 4.1.2 on 2024-01-04 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mouseaction',
            name='category_id',
            field=models.IntegerField(choices=[(1, 'Cursor Movement'), (2, 'Mouse Left Click'), (3, 'Mouse Right Click'), (4, 'ScreenShot'), (5, 'Zoom In and Zoom Out')]),
        ),
    ]
