# Generated by Django 3.2.3 on 2021-05-27 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_wish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('M', 'Mobile'), ('L', 'Laptop'), ('TW', 'Top Wear'), ('BW', 'Bottom Wear'), ('FW', 'Foot Wear'), ('D', 'Deal'), ('C', 'Corona')], max_length=3),
        ),
    ]
