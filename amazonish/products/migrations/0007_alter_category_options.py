# Generated by Django 3.2.22 on 2023-10-22 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20231008_1231'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name', 'parent_category', 'slug', 'tags', 'description', 'created_at', 'updated_at')},
        ),
    ]
