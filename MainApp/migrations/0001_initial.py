# Generated by Django 5.0.1 on 2024-02-06 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Userinfor',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=16)),
                ('user_account', models.CharField(max_length=16)),
                ('user_pwd', models.CharField(max_length=12)),
                ('create_date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]