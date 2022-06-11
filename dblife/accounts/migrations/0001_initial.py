# Generated by Django 3.2.3 on 2021-05-25 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
                ('useremail', models.EmailField(max_length=64)),
                ('password', models.CharField(max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '커뮤니티 사용자',
                'verbose_name_plural': '커뮤니티 사용자',
                'db_table': 'community_user',
            },
        ),
    ]
