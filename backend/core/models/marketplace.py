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


# Additional marketplace models

class ListingCategory(models.Model):
    """Category for marketplace listings."""
    name = models.CharField(max_length=100, help_text='Category name')
    description = models.TextField(blank=True, help_text='Category description')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, help_text='Parent category')
    
    class Meta:
        verbose_name_plural = 'Listing categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class MarketplaceListing(models.Model):
    """Enhanced marketplace listing model."""
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='marketplace_listings')
    title = models.CharField(max_length=200, help_text='Listing title')
    description = models.TextField(help_text='Listing description')
    category = models.ForeignKey(ListingCategory, on_delete=models.CASCADE, help_text='Listing category')
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Item price')
    condition = models.CharField(max_length=20, choices=[
        ('new', 'New'),
        ('used', 'Used'),
        ('refurbished', 'Refurbished'),
    ], help_text='Item condition')
    location = models.CharField(max_length=200, help_text='Item location')
    is_negotiable = models.BooleanField(default=True, help_text='Whether price is negotiable')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class ListingImage(models.Model):
    """Image for marketplace listings."""
    listing = models.ForeignKey(MarketplaceListing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='marketplace_images/', help_text='Listing image')
    caption = models.CharField(max_length=200, blank=True, help_text='Image caption')
    is_primary = models.BooleanField(default=False, help_text='Whether this is the primary image')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_primary', '-created_at']
    
    def __str__(self):
        return f"Image for {self.listing.title}"


class CarListing(models.Model):
    """Car listing model."""
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='car_listings')
    title = models.CharField(max_length=200, help_text='Car listing title')
    description = models.TextField(help_text='Car description')
    make = models.CharField(max_length=100, help_text='Car make')
    model = models.CharField(max_length=100, help_text='Car model')
    year = models.IntegerField(help_text='Car year')
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Car price')
    mileage = models.IntegerField(help_text='Car mileage')
    condition = models.CharField(max_length=20, choices=[
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ], help_text='Car condition')
    location = models.CharField(max_length=200, help_text='Car location')
    is_negotiable = models.BooleanField(default=True, help_text='Whether price is negotiable')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.year} {self.make} {self.model}"


class Review(models.Model):
    """Review model for marketplace transactions."""
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_given')
    listing = models.ForeignKey(MarketplaceListing, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], help_text='Review rating')
    title = models.CharField(max_length=200, help_text='Review title')
    content = models.TextField(help_text='Review content')
    is_verified_purchase = models.BooleanField(default=False, help_text='Whether this is a verified purchase')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.listing.title}"


class Rating(models.Model):
    """Rating model for sellers."""
    rater = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings_given')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings_received')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], help_text='Rating from 1 to 5')
    comment = models.TextField(blank=True, help_text='Rating comment')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('rater', 'seller')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.rater.username} rates {self.seller.username}: {self.rating}/5"


class PaymentTransaction(models.Model):
    """Payment transaction model."""
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
        ('purchase', 'Purchase'),
        ('refund', 'Refund'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text='Transaction amount')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, help_text='Type of transaction')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', help_text='Transaction status')
    payment_method = models.CharField(max_length=50, blank=True, help_text='Payment method used')
    reference = models.CharField(max_length=100, blank=True, help_text='Transaction reference')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.user.username}"


class Order(models.Model):
    """Order model for marketplace purchases."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text='Total order amount')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', help_text='Order status')
    shipping_address = models.ForeignKey('ShippingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.id} - {self.buyer.username}"


class OrderItem(models.Model):
    """Order item model."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    listing = models.ForeignKey(MarketplaceListing, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, help_text='Item quantity')
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Item price at time of purchase')
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return f"{self.quantity}x {self.listing.title}"


class ShippingAddress(models.Model):
    """Shipping address model."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shipping_addresses')
    street = models.CharField(max_length=200, help_text='Street address')
    city = models.CharField(max_length=100, help_text='City')
    state = models.CharField(max_length=50, help_text='State')
    zip_code = models.CharField(max_length=20, help_text='ZIP code')
    country = models.CharField(max_length=100, default='USA', help_text='Country')
    is_default = models.BooleanField(default=False, help_text='Whether this is the default address')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Shipping addresses'
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        return f"{self.street}, {self.city}, {self.state} {self.zip_code}" 