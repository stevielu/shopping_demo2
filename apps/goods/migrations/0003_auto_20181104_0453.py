# Generated by Django 2.0 on 2018-11-04 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20181104_0443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='name',
            field=models.CharField(default='', max_length=100, null=True, verbose_name='商品名'),
        ),
    ]
