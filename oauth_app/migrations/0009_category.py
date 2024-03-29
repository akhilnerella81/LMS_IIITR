# Generated by Django 3.2.12 on 2022-03-30 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth_app', '0008_profile_totalfine'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryname', models.CharField(max_length=50)),
                ('categoryaddr', models.ManyToManyField(related_name='categories', to='oauth_app.Book')),
            ],
        ),
    ]
