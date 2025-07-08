# Generated manually to ensure SponsoredContent table exists

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_create_otp_with_purpose'),
    ]

    operations = [
        migrations.CreateModel(
            name='SponsoredContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Sponsored content title', max_length=200)),
                ('description', models.TextField(help_text='Sponsored content description')),
                ('image_url', models.URLField(blank=True, help_text='Sponsored content image URL', max_length=500)),
                ('link_url', models.URLField(blank=True, help_text='Sponsored content link URL', max_length=500)),
                ('display_location', models.CharField(choices=[('homepage', 'Homepage'), ('sidebar', 'Sidebar'), ('feed', 'Feed'), ('profile', 'Profile')], default='homepage', help_text='Where to display this sponsored content', max_length=20)),
                ('is_active', models.BooleanField(default=True, help_text='Whether this sponsored content is active')),
                ('start_date', models.DateTimeField(blank=True, help_text='When to start showing this content', null=True)),
                ('end_date', models.DateTimeField(blank=True, help_text='When to stop showing this content', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'verbose_name': 'Sponsored Content',
                'verbose_name_plural': 'Sponsored Content',
            },
        ),
    ] 