# Generated by Django 5.0.7 on 2024-08-06 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cloudapp', '0002_document_directory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='directory',
        ),
    ]
