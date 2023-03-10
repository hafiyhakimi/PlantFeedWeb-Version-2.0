# Generated by Django 4.1.5 on 2023-01-31 14:33

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('member', '0004_alter_person_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='prodProduct',
            fields=[
                ('productid', models.AutoField(primary_key=True, serialize=False)),
                ('productName', models.CharField(blank=True, max_length=255)),
                ('productDesc', models.CharField(blank=True, max_length=1500)),
                ('productCategory', models.CharField(blank=True, max_length=255)),
                ('productPrice', models.DecimalField(decimal_places=2, max_digits=4)),
                ('productStock', models.IntegerField(default=0)),
                ('productPhoto', models.ImageField(null=True, upload_to='images/')),
                ('productRating', models.IntegerField(default=0)),
                ('timePosted', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('Person_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='member.person')),
            ],
            options={
                'db_table': 'prodProduct',
            },
        ),
    ]
