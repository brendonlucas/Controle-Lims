# Generated by Django 2.2.7 on 2019-12-13 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controle', '0029_delete_emprestimo2'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='quantidade_emprestada',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
