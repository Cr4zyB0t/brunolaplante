# Generated by Django 3.2.5 on 2021-11-14 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IPLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adresse_IP', models.CharField(max_length=200)),
                ('request', models.TextField(max_length=1024)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
