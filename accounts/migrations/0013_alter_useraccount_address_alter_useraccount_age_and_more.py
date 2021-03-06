# Generated by Django 4.0.3 on 2022-03-19 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_useraccount_relative_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='address',
            field=models.CharField(default='', max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='age',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='city',
            field=models.CharField(default='', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='country',
            field=models.CharField(default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='pin',
            field=models.CharField(default='', max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='profilePic',
            field=models.FileField(default='anonymous.png', upload_to='accounts'),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='relative_email',
            field=models.CharField(default='', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='relative_email_second',
            field=models.CharField(default='', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='state',
            field=models.CharField(default='', max_length=30, null=True),
        ),
    ]
