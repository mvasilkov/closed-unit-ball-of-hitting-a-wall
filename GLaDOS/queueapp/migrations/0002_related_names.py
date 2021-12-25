# Generated by Django 2.0.3 on 2018-05-07 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('queueapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NopFilter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('is_active', models.BooleanField(default=False)),
                ('from_buffer', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='to_nopfilter', to='queueapp.Buffer')),
                ('queue', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='queueapp.Queue')),
                ('to_buffer', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='from_nopfilter', to='queueapp.Buffer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='log',
            options={'ordering': ('-pk',)},
        ),
        migrations.RemoveField(
            model_name='log',
            name='created',
        ),
        migrations.AddField(
            model_name='log',
            name='count',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='log',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='autofilter',
            name='from_buffer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='to_autofilter', to='queueapp.Buffer'),
        ),
        migrations.AlterField(
            model_name='autofilter',
            name='to_buffer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='from_autofilter', to='queueapp.Buffer'),
        ),
        migrations.AlterField(
            model_name='log',
            name='queue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='logs', to='queueapp.Queue'),
        ),
    ]
