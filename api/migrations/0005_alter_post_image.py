# Generated by Django 5.1.3 on 2024-12-08 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='posts/Default.jpg', upload_to='posts/'),
        ),
    ]