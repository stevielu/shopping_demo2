# Generated by Django 2.0 on 2018-11-04 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='name',
            field=models.CharField(default='', max_length=100, verbose_name='商品名'),
        ),
    ]