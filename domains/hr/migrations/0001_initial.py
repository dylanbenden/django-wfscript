# Generated by Django 4.0.4 on 2022-05-18 05:17

from django.db import migrations, models
import django.db.models.deletion
import wfscript.materials.mixin


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(max_length=50, unique=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('internal_email', models.CharField(max_length=50, unique=True)),
                ('external_email', models.CharField(max_length=50, unique=True)),
            ],
            bases=(models.Model, wfscript.materials.mixin.WorkflowMaterial),
        ),
        migrations.CreateModel(
            name='EmergencyContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_name', models.CharField(max_length=50)),
                ('contact_info', models.CharField(max_length=50)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emergency_contacts', to='hr.staff')),
            ],
        ),
    ]
