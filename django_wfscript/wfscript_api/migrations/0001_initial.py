# Generated by Django 4.0.4 on 2022-05-16 21:14

import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('md5', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('data', models.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('payload', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='response', to='wfscript_api.payload')),
            ],
        ),
    ]
