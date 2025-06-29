"""
Marketplace API Views for CalloutRacing Application

This module contains views for managing marketplace listings:
- Car listings, parts, and services
- Marketplace transactions
- Reviews and ratings
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, Avg, Count
from django.utils import timezone

from core.models.marketplace import Marketplace, MarketplaceImage, MarketplaceOrder, MarketplaceReview
from core.models.cars import CarProfile
from .serializers import (
    MarketplaceSerializer, MarketplaceCreateSerializer, 
    MarketplaceImageSerializer, MarketplaceOrderSerializer,
    MarketplaceReviewSerializer
)


class MarketplaceViewSet(viewsets.ModelViewSet):
    """ViewSet for managing marketplace listings."""
    queryset = Marketplace.objects.all()
    serializer_class = MarketplaceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return MarketplaceCreateSerializer
        return MarketplaceSerializer
    
    def get_queryset(self):
        queryset = Marketplace.objects.filter(is_active=True)
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price', None)
        if min_price:
            try:
                min_price = float(min_price)
                queryset = queryset.filter(price__gte=min_price)
            except ValueError:
                pass
        
        max_price = self.request.query_params.get('max_price', None)
        if max_price:
            try:
                max_price = float(max_price)
                queryset = queryset.filter(price__lte=max_price)
            except ValueError:
                pass
        
        # Filter by condition
        condition = self.request.query_params.get('condition', None)
        if condition:
            queryset = queryset.filter(condition=condition)
        
        # Filter by seller
        seller_id = self.request.query_params.get('seller_id', None)
        if seller_id:
            queryset = queryset.filter(seller_id=seller_id)
        
        # Filter by location
        location = self.request.query_params.get('location', None)
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        # Search by title or description
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search) |
                Q(brand__icontains=search) |
                Q(model__icontains=search)
            )
        
        # Sort options
        sort_by = self.request.query_params.get('sort_by', 'created_at')
        if sort_by == 'price_low':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_high':
            queryset = queryset.order_by('-price')
        elif sort_by == 'newest':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'oldest':
            queryset = queryset.order_by('created_at')
        else:
            queryset = queryset.order_by('-created_at')
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
    
    @action(detail=True, methods=['post'])
    def purchase(self, request, pk=None):
        """Purchase a marketplace item."""
        listing = self.get_object()
        buyer = request.user
        
        # Check if user is trying to buy their own item
        if listing.seller == buyer:
            return Response(
                {'detail': 'You cannot purchase your own listing.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if item is still available
        if not listing.is_active:
            return Response(
                {'detail': 'This item is no longer available.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create order
        order = MarketplaceOrder.objects.create(
            listing=listing,
            buyer=buyer,
            seller=listing.seller,
            amount=listing.price,
            status='pending'
        )
        
        # Mark listing as sold
        listing.is_active = False
        listing.save()
        
        serializer = MarketplaceOrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def add_review(self, request, pk=None):
        """Add a review to a marketplace listing."""
        listing = self.get_object()
        user = request.user
        
        # Check if user has purchased this item
        if not MarketplaceOrder.objects.filter(
            listing=listing, 
            buyer=user, 
            status='completed'
        ).exists():
            return Response(
                {'detail': 'You can only review items you have purchased.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if user has already reviewed
        if MarketplaceReview.objects.filter(listing=listing, reviewer=user).exists():
            return Response(
                {'detail': 'You have already reviewed this item.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        rating = request.data.get('rating')
        comment = request.data.get('comment', '')
        
        if not rating or not (1 <= int(rating) <= 5):
            return Response(
                {'detail': 'Rating must be between 1 and 5.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        review = MarketplaceReview.objects.create(
            listing=listing,
            reviewer=user,
            rating=rating,
            comment=comment
        )
        
        serializer = MarketplaceReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get reviews for a marketplace listing."""
        listing = self.get_object()
        reviews = listing.reviews.all().order_by('-created_at')
        serializer = MarketplaceReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_listings(self, request):
        """Get current user's marketplace listings."""
        my_listings = Marketplace.objects.filter(seller=request.user).order_by('-created_at')
        serializer = self.get_serializer(my_listings, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_purchases(self, request):
        """Get current user's marketplace purchases."""
        my_purchases = MarketplaceOrder.objects.filter(buyer=request.user).order_by('-created_at')
        serializer = MarketplaceOrderSerializer(my_purchases, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_sales(self, request):
        """Get current user's marketplace sales."""
        my_sales = MarketplaceOrder.objects.filter(seller=request.user).order_by('-created_at')
        serializer = MarketplaceOrderSerializer(my_sales, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get available marketplace categories."""
        categories = Marketplace.objects.values_list('category', flat=True).distinct()
        return Response(list(categories))
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured marketplace listings."""
        featured_listings = Marketplace.objects.filter(
            is_active=True,
            is_featured=True
        ).order_by('-created_at')[:10]
        
        serializer = self.get_serializer(featured_listings, many=True)
        return Response(serializer.data) 