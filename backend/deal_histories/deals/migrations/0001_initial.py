# Generated by Django 3.0 on 2023-07-27 19:52

import core.enums
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Gem', max_length=core.enums.Limits['GEM_NAME_MAX_CHAR'], unique=True, validators=[django.core.validators.RegexValidator(core.enums.Regex['GEM_NAME'])], verbose_name='gem')),
            ],
            options={
                'verbose_name': 'gem',
                'verbose_name_plural': 'gems',
            },
        ),
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.PositiveIntegerField(default=core.enums.Limits['DEAL_TOTAL_DEFAULT_VALUE'], help_text='The total cost of the deal', verbose_name='total')),
                ('quantity', models.PositiveSmallIntegerField(default=core.enums.Limits['DEAL_QUANTITY_DEFAULT_VALUE'], help_text='The number of gems in the deal', verbose_name='quantity')),
                ('date', models.DateTimeField(help_text='deal time', verbose_name='date')),
                ('item', models.ForeignKey(help_text='Deal stone', on_delete=django.db.models.deletion.PROTECT, related_name='deals', to='deals.Gem', verbose_name='item')),
            ],
            options={
                'verbose_name': 'deal',
                'verbose_name_plural': 'deals',
            },
        ),
    ]
