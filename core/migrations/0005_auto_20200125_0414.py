# Generated by Django 2.2 on 2020-01-25 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_contactenos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tipo_contacto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_contacto', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='contactenos',
            name='mensaje',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]
