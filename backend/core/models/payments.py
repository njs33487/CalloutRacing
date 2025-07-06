"""
Payment and Subscription Models

This module contains models for handling payments, subscriptions, and marketplace transactions.
"""

from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class Subscription(models.Model):
    """User subscription model for premium plans."""
    SUBSCRIPTION_STATUS_CHOICES = [
        ('active', 'Active'),
        ('canceled', 'Canceled'),
        ('past_due', 'Past Due'),
        ('unpaid', 'Unpaid'),
        ('trialing', 'Trialing'),
        ('incomplete', 'Incomplete'),
        ('incomplete_expired', 'Incomplete Expired'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    stripe_subscription_id = models.CharField(max_length=255, unique=True, help_text='Stripe subscription ID', null=True, blank=True)
    stripe_customer_id = models.CharField(max_length=255, help_text='Stripe customer ID', null=True, blank=True)
    stripe_price_id = models.CharField(max_length=255, help_text='Stripe price ID', null=True, blank=True)
    status = models.CharField(max_length=20, choices=SUBSCRIPTION_STATUS_CHOICES, default='incomplete')
    current_period_start = models.DateTimeField(null=True, blank=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    cancel_at_period_end = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.status}"


class Payment(models.Model):
    """Payment model for tracking all payments."""
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
        ('canceled', 'Canceled'),
    ]
    
    PAYMENT_TYPE_CHOICES = [
        ('subscription', 'Subscription'),
        ('marketplace', 'Marketplace'),
        ('one_time', 'One Time'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    stripe_payment_intent_id = models.CharField(max_length=255, unique=True, help_text='Stripe payment intent ID', null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text='Amount in dollars')
    currency = models.CharField(max_length=3, default='usd')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - ${self.amount} - {self.status}"


class UserWallet(models.Model):
    """User wallet for managing balances and transactions."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text='Current balance in dollars')
    stripe_account_id = models.CharField(max_length=255, blank=True, null=True, help_text='Stripe Connect account ID for marketplace sellers')
    is_onboarded = models.BooleanField(default=False, help_text='Whether user has completed Stripe Connect onboarding')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - ${self.balance}"


class MarketplaceTransaction(models.Model):
    """Model for tracking marketplace sales and commissions."""
    TRANSACTION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='marketplace_purchases')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='marketplace_sales')
    item = models.ForeignKey('core.MarketplaceListing', on_delete=models.CASCADE, related_name='transactions')
    stripe_payment_intent_id = models.CharField(max_length=255, unique=True, help_text='Stripe payment intent ID')
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text='Total amount in dollars')
    seller_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text='Amount seller receives')
    platform_commission = models.DecimalField(max_digits=10, decimal_places=2, help_text='Platform commission amount')
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.buyer.username} → {self.seller.username} - ${self.amount}" 