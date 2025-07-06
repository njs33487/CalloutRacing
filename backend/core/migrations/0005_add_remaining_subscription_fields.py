# Generated manually to add remaining missing Subscription model fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_add_missing_subscription_fields'),
    ]

    operations = [
        # Add missing stripe_subscription_id field
        migrations.AddField(
            model_name='subscription',
            name='stripe_subscription_id',
            field=models.CharField(
                blank=True,
                help_text='Stripe subscription ID',
                max_length=255,
                null=True,
                unique=True
            ),
        ),
        # Add missing stripe_customer_id field
        migrations.AddField(
            model_name='subscription',
            name='stripe_customer_id',
            field=models.CharField(
                blank=True,
                help_text='Stripe customer ID',
                max_length=255,
                null=True
            ),
        ),
        # Add missing stripe_price_id field
        migrations.AddField(
            model_name='subscription',
            name='stripe_price_id',
            field=models.CharField(
                blank=True,
                help_text='Stripe price ID',
                max_length=255,
                null=True
            ),
        ),
    ] 