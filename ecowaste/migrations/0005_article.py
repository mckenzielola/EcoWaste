# Generated by Django 5.1.2 on 2024-12-03 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecowaste', '0004_wasteitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('date_published', models.DateField(auto_now_add=True)),
            ],
        ),
    ]