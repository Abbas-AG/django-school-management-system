# Generated by Django 3.0.5 on 2025-03-12 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0012_lesson'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('class_name', models.CharField(choices=[('one', 'الصف الأول متوسط'), ('two', 'الصف الثاني متوسط'), ('three', 'الصف الثالث متوسط'), ('four', 'الصف الرابع إعدادي'), ('five', 'الصف الخامس إعدادي'), ('six', 'الصف السادس إعدادي')], max_length=10)),
            ],
        ),
    ]
