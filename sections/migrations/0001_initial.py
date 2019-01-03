# Generated by Django 2.1.4 on 2018-12-23 13:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Undefined Name', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('time_created', models.DateTimeField()),
                ('is_first', models.BooleanField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubForum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Undefined Name', max_length=30)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sections.Forum')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(default='Undefined Theme', max_length=200)),
                ('views', models.PositiveIntegerField(default=0)),
                ('time_created', models.DateTimeField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('subforum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sections.SubForum')),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='subforum',
            field=models.ForeignKey(default=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='sections.Topic'), on_delete=django.db.models.deletion.CASCADE, to='sections.SubForum'),
        ),
        migrations.AddField(
            model_name='message',
            name='topic',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='sections.Topic'),
        ),
    ]
