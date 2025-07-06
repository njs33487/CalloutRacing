# Generated manually to add missing Subscription model fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_add_stripe_connect_account_id'),
    ]

    operations = [
        # Add missing status field to Subscription
        migrations.AddField(
            model_name='subscription',
            name='status',
            field=models.CharField(
                choices=[
                    ('active', 'Active'),
                    ('canceled', 'Canceled'),
                    ('past_due', 'Past Due'),
                    ('unpaid', 'Unpaid'),
                    ('trialing', 'Trialing'),
                    ('incomplete', 'Incomplete'),
                    ('incomplete_expired', 'Incomplete Expired'),
                ],
                default='incomplete',
                max_length=20
            ),
        ),
        # Add missing current_period_start field
        migrations.AddField(
            model_name='subscription',
            name='current_period_start',
            field=models.DateTimeField(blank=True, null=True),
        ),
        # Add missing current_period_end field
        migrations.AddField(
            model_name='subscription',
            name='current_period_end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        # Add missing cancel_at_period_end field
        migrations.AddField(
            model_name='subscription',
            name='cancel_at_period_end',
            field=models.BooleanField(default=False),
        ),
        # Add missing updated_at field
        migrations.AddField(
            model_name='subscription',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ] 