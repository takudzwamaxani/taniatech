# Generated by Django 5.0.13 on 2025-07-06 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0006_remove_cvprofile_attachments_attachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactinformation',
            name='google_maps_embed_url',
            field=models.URLField(blank=True, help_text='Paste the Google Maps embed URL here.', max_length=1000),
        ),
    ]
