# Generated by Django 3.0.4 on 2020-03-18 03:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emprestimo', '0007_emprestimo_visualisado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emprestimo',
            name='estado',
        ),
        migrations.RemoveField(
            model_name='emprestimo',
            name='mensagem_rejeitado',
        ),
    ]
