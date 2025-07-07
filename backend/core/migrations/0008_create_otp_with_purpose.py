# Generated manually to fix OTP table creation issue

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_userpost_announcement_priority_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp_type', models.CharField(choices=[('phone', 'Phone'), ('email', 'Email')], help_text='Type of OTP (phone or email)', max_length=10)),
                ('identifier', models.CharField(help_text='Phone number or email address', max_length=255)),
                ('code', models.CharField(help_text='6-digit OTP code', max_length=6)),
                ('purpose', models.CharField(choices=[('login', 'Login'), ('signup', 'Signup'), ('password_reset', 'Password Reset'), ('email_verification', 'Email Verification'), ('phone_verification', 'Phone Verification')], default='login', help_text='Purpose of the OTP', max_length=20)),
                ('is_used', models.BooleanField(default=False, help_text='Whether OTP has been used')),
                ('expires_at', models.DateTimeField(help_text='When OTP expires')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='otps', to='core.user')),
            ],
            options={
                'ordering': ['-created_at'],
                'indexes': [
                    models.Index(fields=['identifier', 'code', 'is_used'], name='core_otp_identif_21718b_idx'),
                    models.Index(fields=['expires_at'], name='core_otp_expires_288351_idx'),
                    models.Index(fields=['purpose'], name='core_otp_purpose_b49549_idx'),
                ],
            },
        ),
    ] 