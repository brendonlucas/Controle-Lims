# Generated by Django 3.0.4 on 2020-05-07 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controle', '0035_item_bloqueado'),
    ]

    operations = [
        migrations.CreateModel(
            name='Controle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emprestimo_ativo', models.BooleanField(default=1)),
            ],
        ),
    ]
