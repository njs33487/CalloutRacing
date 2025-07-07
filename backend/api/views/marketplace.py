"""
Marketplace API Views for CalloutRacing Application

This module contains views for managing marketplace listings:
- Vehicle listings
- Parts listings
- Services listings
- Transaction management
"""

from rest_framework import viewsets, status, permissions, serializers
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, Avg
from django.utils import timezone
from datetime import datetime, timedelta
import logging
import stripe
from django.conf import settings

from core.models.marketplace import Marketplace, MarketplaceOrder, MarketplaceReview
from api.serializers import MarketplaceListingSerializer
from core.secret_store import get_stripe_webhook_secret

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

logger = logging.getLogger(__name__)

# Basic serializers for now
class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marketplace
        fields = '__all__'


class ListingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marketplace
        fields = ['title', 'description', 'category', 'price', 'condition', 
                 'location', 'is_negotiable', 'contact_phone', 'contact_email']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketplaceOrder
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketplaceReview
        fields = '__all__'


class ListingViewSet(viewsets.ModelViewSet):
    """ViewSet for managing marketplace listings."""
    queryset = Marketplace.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ListingCreateSerializer
        return ListingSerializer
    
    def get_queryset(self):
        queryset = Marketplace.objects.all()
        
        # Filter by listing type
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
        
        # Filter by location
        location = self.request.query_params.get('location', None)
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        # Filter by negotiable status
        is_negotiable = self.request.query_params.get('is_negotiable', None)
        if is_negotiable is not None:
            is_negotiable = is_negotiable.lower() == 'true'
            queryset = queryset.filter(is_negotiable=is_negotiable)
        
        # Filter by seller
        seller_id = self.request.query_params.get('seller_id', None)
        if seller_id:
            queryset = queryset.filter(seller_id=seller_id)
        
        # Search by title or description
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
    
    @action(detail=True, methods=['post'])
    def contact_seller(self, request, pk=None):
        """Contact the seller about a listing."""
        listing = self.get_object()
        message = request.data.get('message', '')
        
        if not message:
            return Response(
                {'detail': 'Message is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Here you would typically send an email or create a message
        # For now, just return success
        return Response({
            'detail': 'Message sent to seller.',
            'listing_id': listing.id,
            'seller_id': listing.seller.id
        })
    
    @action(detail=True, methods=['post'])
    def make_offer(self, request, pk=None):
        """Make an offer on a listing."""
        listing = self.get_object()
        offer_amount = request.data.get('offer_amount', None)
        message = request.data.get('message', '')
        
        if not offer_amount:
            return Response(
                {'detail': 'Offer amount is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            offer_amount = float(offer_amount)
        except ValueError:
            return Response(
                {'detail': 'Invalid offer amount.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if offer_amount <= 0:
            return Response(
                {'detail': 'Offer amount must be positive.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Here you would typically create an offer record
        # For now, just return success
        return Response({
            'detail': 'Offer submitted successfully.',
            'listing_id': listing.id,
            'offer_amount': offer_amount
        })
    
    @action(detail=False, methods=['get'])
    def my_listings(self, request):
        """Get listings created by the current user."""
        my_listings = Marketplace.objects.filter(seller=request.user).order_by('-created_at')
        serializer = self.get_serializer(my_listings, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def favorites(self, request):
        """Get user's favorite listings."""
        # This would require a favorites model
        # For now, return empty list
        return Response([])
    
    @action(detail=True, methods=['post'])
    def toggle_favorite(self, request, pk=None):
        """Toggle favorite status of a listing."""
        # This would require a favorites model
        # For now, just return success
        return Response({'detail': 'Favorite status toggled.'})


class TransactionViewSet(viewsets.ModelViewSet):
    """ViewSet for managing marketplace transactions."""
    queryset = MarketplaceOrder.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see their own transactions
        return MarketplaceOrder.objects.filter(
            Q(buyer=self.request.user) | Q(seller=self.request.user)
        ).order_by('-created_at')
    
    @action(detail=False, methods=['get'])
    def my_purchases(self, request):
        """Get transactions where user is the buyer."""
        purchases = MarketplaceOrder.objects.filter(buyer=request.user).order_by('-created_at')
        serializer = self.get_serializer(purchases, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_sales(self, request):
        """Get transactions where user is the seller."""
        sales = MarketplaceOrder.objects.filter(seller=request.user).order_by('-created_at')
        serializer = self.get_serializer(sales, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for managing marketplace reviews."""
    queryset = MarketplaceReview.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = MarketplaceReview.objects.all()
        
        # Filter by reviewed user
        reviewed_user_id = self.request.query_params.get('reviewed_user_id', None)
        if reviewed_user_id:
            queryset = queryset.filter(order__seller_id=reviewed_user_id)
        
        # Filter by reviewer
        reviewer_id = self.request.query_params.get('reviewer_id', None)
        if reviewer_id:
            queryset = queryset.filter(reviewer_id=reviewer_id)
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_reviews(self, request):
        """Get reviews written by the current user."""
        my_reviews = MarketplaceReview.objects.filter(reviewer=request.user).order_by('-created_at')
        serializer = self.get_serializer(my_reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def reviews_of_me(self, request):
        """Get reviews of the current user."""
        reviews_of_me = MarketplaceReview.objects.filter(order__seller=request.user).order_by('-created_at')
        serializer = self.get_serializer(reviews_of_me, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_connect_account(request):
    """Create a Stripe Connect account for marketplace sellers"""
    try:
        # Create a connected account for the user
        account = stripe.Account.create(
            controller={
                "stripe_dashboard": {
                    "type": "express",
                },
                "fees": {
                    "payer": "application"
                },
                "losses": {
                    "payments": "application"
                },
            },
            metadata={
                "user_id": str(request.user.id),
                "platform": "calloutracing"
            }
        )
        
        # Store the account ID in user profile
        request.user.stripe_connect_account_id = account.id
        request.user.save()
        
        return Response({
            'account_id': account.id,
            'message': 'Connect account created successfully'
        })
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error in create_connect_account: {str(e)}")
        return Response({
            'error': 'Payment processing error'
        }, status=400)
    except Exception as e:
        logger.error(f"Error in create_connect_account: {str(e)}")
        return Response({
            'error': 'Internal server error'
        }, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_account_link(request):
    """Create an account link for Connect onboarding"""
    try:
        account_id = request.data.get('account_id')
        
        if not account_id:
            return Response({
                'error': 'Account ID is required'
            }, status=400)
        
        # Create account link for onboarding
        account_link = stripe.AccountLink.create(
            account=account_id,
            return_url=f"{settings.FRONTEND_URL}/marketplace/onboarding/return/{account_id}",
            refresh_url=f"{settings.FRONTEND_URL}/marketplace/onboarding/refresh/{account_id}",
            type="account_onboarding",
        )
        
        return Response({
            'url': account_link.url,
        })
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error in create_account_link: {str(e)}")
        return Response({
            'error': 'Payment processing error'
        }, status=400)
    except Exception as e:
        logger.error(f"Error in create_account_link: {str(e)}")
        return Response({
            'error': 'Internal server error'
        }, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_connect_account_status(request):
    """Get the status of user's Connect account"""
    try:
        if not request.user.stripe_connect_account_id:
            return Response({
                'has_account': False,
                'account_id': None
            })
        
        account = stripe.Account.retrieve(request.user.stripe_connect_account_id)
        
        return Response({
            'has_account': True,
            'account_id': account.id,
            'charges_enabled': account.charges_enabled,
            'payouts_enabled': account.payouts_enabled,
            'details_submitted': account.details_submitted,
            'requirements': account.requirements
        })
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error in get_connect_account_status: {str(e)}")
        return Response({
            'error': 'Payment processing error'
        }, status=400)
    except Exception as e:
        logger.error(f"Error in get_connect_account_status: {str(e)}")
        return Response({
            'error': 'Internal server error'
        }, status=500) 