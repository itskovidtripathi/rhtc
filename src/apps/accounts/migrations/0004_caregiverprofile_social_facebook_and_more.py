# Generated by Django 5.2.1 on 2025-06-28 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userrole'),
    ]

    operations = [
        migrations.AddField(
            model_name='caregiverprofile',
            name='social_facebook',
            field=models.URLField(blank=True, null=True, verbose_name='Facebook Profile'),
        ),
        migrations.AddField(
            model_name='caregiverprofile',
            name='social_linked_in',
            field=models.URLField(blank=True, null=True, verbose_name='LinkedIn Profile'),
        ),
        migrations.AddField(
            model_name='caregiverprofile',
            name='social_twitter',
            field=models.URLField(blank=True, null=True, verbose_name='Twitter Profile'),
        ),
    ]
