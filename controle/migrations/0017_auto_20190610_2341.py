# Generated by Django 2.2.1 on 2019-06-11 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controle', '0016_auto_20190610_2340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='imagem',
            field=models.FileField(default='imagens/photo.jpg', upload_to='documents/%y+%m+%d'),
        ),
    ]
