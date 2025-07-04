# Generated by Django 5.2.1 on 2025-06-21 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('rol', models.CharField(max_length=20)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'empleado',
            },
        ),
    ]
