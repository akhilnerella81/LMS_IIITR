# Generated by Django 3.2.12 on 2022-03-13 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth_app', '0003_issuebook_fine'),
    ]

    operations = [
        migrations.CreateModel(
            name='RenewDays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NumOfDays', models.PositiveIntegerField(default=10)),
            ],
        ),
        migrations.AddField(
            model_name='issuebook',
            name='times_renew',
            field=models.PositiveIntegerField(default=0),
        ),
    ]