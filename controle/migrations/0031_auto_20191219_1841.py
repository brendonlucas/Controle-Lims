# Generated by Django 2.2.7 on 2019-12-19 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controle', '0030_item_quantidade_emprestada'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='quantidade_descartada',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='item',
            name='quantidade_emprestada',
            field=models.IntegerField(default=0),
        ),
    ]
