# Generated by Django 4.0 on 2022-04-06 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_alter_stockhistory_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockhistory',
            name='adj_close',
            field=models.FloatField(default=0, help_text='조정 종가', verbose_name='adj_close'),
        ),
        migrations.AlterField(
            model_name='stockhistory',
            name='close',
            field=models.FloatField(default=0, help_text='종가', verbose_name='close'),
        ),
        migrations.AlterField(
            model_name='stockhistory',
            name='high',
            field=models.FloatField(default=0, help_text='고가', verbose_name='high'),
        ),
        migrations.AlterField(
            model_name='stockhistory',
            name='low',
            field=models.FloatField(default=0, help_text='저가', verbose_name='low'),
        ),
        migrations.AlterField(
            model_name='stockhistory',
            name='opens',
            field=models.FloatField(default=0, help_text='시가', verbose_name='opens'),
        ),
        migrations.AlterField(
            model_name='stockhistory',
            name='volume',
            field=models.FloatField(default=0, help_text='거래량', verbose_name='volume'),
        ),
        migrations.AlterField(
            model_name='stockprice',
            name='high',
            field=models.FloatField(default=0, help_text='고가', verbose_name='high'),
        ),
        migrations.AlterField(
            model_name='stockprice',
            name='low',
            field=models.FloatField(default=0, help_text='저가', verbose_name='low'),
        ),
        migrations.AlterField(
            model_name='stockprice',
            name='market',
            field=models.CharField(default='', help_text='상장사', max_length=50, verbose_name='market'),
        ),
        migrations.AlterField(
            model_name='stockprice',
            name='name',
            field=models.CharField(default='', help_text='종목명', max_length=50, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='stockprice',
            name='open',
            field=models.FloatField(default=0, help_text='시가', verbose_name='open'),
        ),
        migrations.AlterField(
            model_name='stockprice',
            name='prevclose',
            field=models.FloatField(default=0, help_text='전일가', verbose_name='prevclose'),
        ),
        migrations.AlterField(
            model_name='stockprice',
            name='price',
            field=models.FloatField(default=0, help_text='주가', verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='stockprice',
            name='volume',
            field=models.FloatField(default=0, help_text='거래량', verbose_name='volume'),
        ),
    ]
