# Generated by Django 5.0 on 2024-02-13 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resqroute', '0004_alter_functionsbrigade_function'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map',
            name='img',
            field=models.ImageField(upload_to=''),
        ),
    ]
