# Generated by Django 2.2.1 on 2019-06-12 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controle', '0022_auto_20190611_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='imagem',
            field=models.FileField(default='documents/1111/sem_foto.jpg', upload_to='documents/%Y/%m/%d'),
        ),
    ]