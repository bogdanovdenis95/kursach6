# Generated by Django 4.2 on 2024-07-27 18:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="email_verification_expiry",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="email_verification_token",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]