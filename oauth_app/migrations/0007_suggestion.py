# Generated by Django 3.2.12 on 2022-03-13 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth_app', '0006_fineperday'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BookTitle', models.CharField(max_length=200)),
                ('Category', models.CharField(max_length=50)),
                ('ISBN', models.CharField(max_length=50)),
            ],
        ),
    ]