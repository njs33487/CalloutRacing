"""
Marketplace Models

This module contains models related to marketplace functionality:
- Marketplace: Marketplace listings
- MarketplaceImage: Images for marketplace items
- MarketplaceOrder: Orders and transactions
- MarketplaceReview: Reviews for marketplace transactions
- ContactSubmission: Contact form submissions
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class Marketplace(models.Model):
    """Marketplace listing model."""
    title = models.CharField(max_length=200, help_text="Listing title")
    description = models.TextField(help_text="Listing description")
    category = models.CharField(max_length=50, choices=[
        ('car', 'Car'),
        ('parts', 'Parts'),
        ('wheels', 'Wheels & Tires'),
        ('electronics', 'Electronics'),
        ('tools', 'Tools'),
        ('other', 'Other'),
    ], help_text="Listing category")
    condition = models.CharField(max_length=20, choices=[
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ], help_text="Item condition")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Item price")
    is_negotiable = models.BooleanField(default=True, help_text="Whether price is negotiable")
    trade_offered = models.BooleanField(default=False, help_text="Whether trade is offered")
    trade_description = models.TextField(blank=True, help_text="Trade description")
    location = models.CharField(max_length=200, help_text="Item location")
    contact_phone = models.CharField(max_length=20, blank=True, help_text="Contact phone")
    contact_email = models.EmailField(blank=True, help_text="Contact email")
    is_active = models.BooleanField(default=True, help_text="Whether listing is active")
    views = models.IntegerField(default=0, help_text="Number of views")
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='marketplace_items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class MarketplaceImage(models.Model):
    """Marketplace image model."""
    marketplace_item = models.ForeignKey(Marketplace, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='marketplace_images/', help_text="Item image")
    caption = models.CharField(max_length=200, blank=True, help_text="Image caption")
    is_primary = models.BooleanField(default=False, help_text="Whether this is the primary image")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.marketplace_item.title}"

    class Meta:
        ordering = ['-is_primary', '-created_at']


class MarketplaceOrder(models.Model):
    """Marketplace order model."""
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='purchases')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sales')
    item = models.ForeignKey(Marketplace, on_delete=models.CASCADE, related_name='orders')
    quantity = models.IntegerField(default=1, help_text="Order quantity")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total order amount")
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ], default='pending', help_text="Order status")
    shipping_address = models.TextField(blank=True, help_text="Shipping address")
    tracking_number = models.CharField(max_length=100, blank=True, help_text="Tracking number")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.item.title}"

    class Meta:
        ordering = ['-created_at']


class MarketplaceReview(models.Model):
    """Marketplace review model."""
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='marketplace_reviews')
    order = models.OneToOneField(MarketplaceOrder, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], help_text="Review rating")
    title = models.CharField(max_length=200, help_text="Review title")
    comment = models.TextField(help_text="Review comment")
    is_verified_purchase = models.BooleanField(default=True, help_text="Whether this is a verified purchase")
    helpful_votes = models.IntegerField(default=0, help_text="Number of helpful votes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.order.item.title}"

    class Meta:
        ordering = ['-created_at']


class ContactSubmission(models.Model):
    """Contact form submission model."""
    name = models.CharField(max_length=100, help_text="Contact person's name")
    email = models.EmailField(help_text="Contact person's email")
    subject = models.CharField(max_length=200, help_text="Subject of the inquiry")
    message = models.TextField(help_text="Contact message content")
    is_reviewed = models.BooleanField(default=False, help_text="Whether admin has reviewed this submission")
    is_responded = models.BooleanField(default=False, help_text="Whether admin has responded to this submission")
    admin_notes = models.TextField(blank=True, help_text="Admin notes about this submission")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the submission was received")
    reviewed_at = models.DateTimeField(blank=True, null=True, help_text="When admin reviewed this submission")
    responded_at = models.DateTimeField(blank=True, null=True, help_text="When admin responded to this submission")

    def __str__(self):
        return f"Contact from {self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at'] 