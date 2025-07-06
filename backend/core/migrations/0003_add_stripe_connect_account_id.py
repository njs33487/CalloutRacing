# Generated manually to add missing stripe_connect_account_id field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_add_missing_user_fields'),
    ]

    operations = [
        # Add missing stripe_connect_account_id field
        migrations.AddField(
            model_name='user',
            name='stripe_connect_account_id',
            field=models.CharField(
                blank=True,
                help_text='Stripe Connect account ID for marketplace sellers',
                max_length=255,
                null=True
            ),
        ),
    ] 