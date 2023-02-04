# Generated by Django 4.1.6 on 2023-02-04 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_options_remove_order_address1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='order',
            name='creditnumber',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='order',
            name='cvv',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='order',
            name='expiration',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='order',
            name='name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='order',
            name='namecard',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='order',
            name='transaction_code',
            field=models.CharField(max_length=1000),
        ),
    ]