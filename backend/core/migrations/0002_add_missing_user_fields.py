# Generated manually to add missing User model fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        # Add missing phone_number field
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(
                blank=True,
                help_text="User's phone number",
                max_length=15,
                null=True,
                unique=True
            ),
        ),
        # Add missing phone_verified field
        migrations.AddField(
            model_name='user',
            name='phone_verified',
            field=models.BooleanField(
                default=False,
                help_text='Whether phone number has been verified'
            ),
        ),
        # Add missing stripe_customer_id field
        migrations.AddField(
            model_name='user',
            name='stripe_customer_id',
            field=models.CharField(
                blank=True,
                help_text='Stripe customer ID for subscriptions',
                max_length=255,
                null=True
            ),
        ),
    ] 