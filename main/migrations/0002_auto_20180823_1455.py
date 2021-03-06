# Generated by Django 2.1 on 2018-08-23 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dictionary',
            name='language_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='language_from', to='main.Language'),
        ),
        migrations.AlterField(
            model_name='dictionary',
            name='language_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='language_to', to='main.Language'),
        ),
        migrations.AlterField(
            model_name='word',
            name='definition',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='word',
            name='dictionary',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Dictionary'),
        ),
    ]
