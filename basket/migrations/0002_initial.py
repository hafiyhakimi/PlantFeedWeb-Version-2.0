# Generated by Django 4.1.5 on 2023-01-31 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('marketplace', '0001_initial'),
        ('basket', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='productid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.prodproduct'),
        ),
    ]
