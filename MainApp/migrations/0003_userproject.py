# Generated by Django 5.0.1 on 2024-03-05 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0002_remove_userinfor_create_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProject',
            fields=[
                ('project_id', models.AutoField(primary_key=True, serialize=False, verbose_name='项目id')),
                ('project_name', models.CharField(max_length=255, verbose_name='项目名称')),
                ('user_id', models.IntegerField(verbose_name='用户id')),
                ('image_list', models.TextField(verbose_name='图片列表')),
            ],
        ),
    ]
