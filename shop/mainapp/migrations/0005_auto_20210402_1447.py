# Generated by Django 3.1.5 on 2021-04-02 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20210402_1240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartproduct',
            name='cart',
        ),
        migrations.AddField(
            model_name='cart',
            name='cart_product',
            field=models.ManyToManyField(to='mainapp.CartProduct'),
        ),
    ]
