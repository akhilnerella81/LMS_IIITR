# Generated by Django 3.2.12 on 2022-04-01 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth_app', '0014_alter_book_isbn'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
