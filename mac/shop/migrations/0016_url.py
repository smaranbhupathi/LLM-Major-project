# Generated by Django 4.1.2 on 2024-04-23 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='url',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('user', models.IntegerField()),
                ('url', models.URLField()),
                ('session', models.IntegerField()),
            ],
        ),
    ]
