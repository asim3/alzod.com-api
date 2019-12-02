# Generated by Django 2.2.7 on 2019-12-02 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentModel',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('content_type', models.CharField(max_length=1)),
                ('text', models.TextField(blank=True, null=True)),
                ('fk_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='files.FileModel')),
            ],
        ),
    ]
