# Generated by Django 5.0.4 on 2024-05-13 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PaperTrail_App', '0005_document_shared_with'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Annotaions',
            new_name='Annotations',
        ),
        migrations.AlterModelOptions(
            name='annotations',
            options={'verbose_name': 'Annotation', 'verbose_name_plural': 'Annotations'},
        ),
    ]