"""
Payment Models

This module contains models related to payments and financial features:
- Subscription: User subscription plans
- Payment: Payment transactions
- UserWallet: User wallet and balance
- Bet: Betting on races and events
- BettingPool: Betting pools and odds
"""

from django.db import models
from django.conf import settings


class Subscription(models.Model):
    """Subscription model."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    subscription_type = models.CharField(max_length=20, choices=[
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('pro', 'Pro'),
    ], help_text="Subscription type")
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ], default='active', help_text="Subscription status")
    start_date = models.DateTimeField(auto_now_add=True, help_text="Subscription start date")
    end_date = models.DateTimeField(blank=True, null=True, help_text="Subscription end date")
    next_billing_date = models.DateTimeField(blank=True, null=True, help_text="Next billing date")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.subscription_type} ({self.status})"

    class Meta:
        ordering = ['-created_at']


class Payment(models.Model):
    """Payment model."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    payment_type = models.CharField(max_length=20, choices=[
        ('subscription', 'Subscription'),
        ('marketplace', 'Marketplace'),
        ('betting', 'Betting'),
        ('other', 'Other'),
    ], help_text="Payment type")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Payment amount")
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ], default='pending', help_text="Payment status")
    payment_provider = models.CharField(max_length=50, blank=True, help_text="Payment provider")
    transaction_id = models.CharField(max_length=100, blank=True, help_text="Transaction ID")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.payment_type} - ${self.amount}"

    class Meta:
        ordering = ['-created_at']


class UserWallet(models.Model):
    """User wallet model."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Wallet balance")
    is_active = models.BooleanField(default=True, help_text="Whether wallet is active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s wallet - ${self.balance}"

    class Meta:
        ordering = ['-updated_at']


class Bet(models.Model):
    """Bet model."""
    bettor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bets')
    bet_type = models.CharField(max_length=20, choices=[
        ('callout', 'Callout'),
        ('event', 'Event'),
        ('other', 'Other'),
    ], help_text="Bet type")
    bet_amount = models.DecimalField(max_digits=8, decimal_places=2, help_text="Bet amount")
    odds = models.DecimalField(max_digits=5, decimal_places=2, help_text="Betting odds")
    potential_payout = models.DecimalField(max_digits=8, decimal_places=2, help_text="Potential payout")
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('cancelled', 'Cancelled'),
    ], default='pending', help_text="Bet status")
    callout = models.ForeignKey('Callout', on_delete=models.CASCADE, related_name='bets', blank=True, null=True)
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='bets', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bettor.username} - ${self.bet_amount} on {self.bet_type}"

    class Meta:
        ordering = ['-created_at']


class BettingPool(models.Model):
    """Betting pool model."""
    name = models.CharField(max_length=200, help_text="Pool name")
    description = models.TextField(blank=True, help_text="Pool description")
    total_pool = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Total pool amount")
    is_active = models.BooleanField(default=True, help_text="Whether pool is active")
    is_settled = models.BooleanField(default=False, help_text="Whether pool is settled")
    callout = models.ForeignKey('Callout', on_delete=models.CASCADE, related_name='betting_pools', blank=True, null=True)
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='betting_pools', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - ${self.total_pool}"

    class Meta:
        ordering = ['-created_at'] 