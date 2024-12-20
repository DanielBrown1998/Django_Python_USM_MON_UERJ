# Generated by Django 5.0.7 on 2024-11-07 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_alter_matriculas_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matriculas',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='monitorias',
            name='status',
            field=models.CharField(choices=[('AUSENTE', 'Ausente'), ('PRESENTE', 'Presente'), ('CANCELADA', 'Cancelada')], default='MARCADA', max_length=15),
        ),
    ]
