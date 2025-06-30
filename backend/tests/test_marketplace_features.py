from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from core.models import (
    UserProfile, MarketplaceListing, ListingCategory, ListingImage,
    CarListing, CarImage, Review, Rating, PaymentTransaction,
    UserWallet, Order, OrderItem, ShippingAddress
)
from api.serializers import (
    MarketplaceListingSerializer, CarListingSerializer,
    ReviewSerializer, RatingSerializer, PaymentTransactionSerializer,
    UserWalletSerializer, OrderSerializer
)
from django.utils import timezone
from decimal import Decimal
import json

User = get_user_model()


class MarketplaceListingTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username='seller1',
            email='seller1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='buyer1',
            email='buyer1@test.com',
            password='testpass123'
        )
        self.category = ListingCategory.objects.create(
            name='Engine Parts',
            description='Engine components and accessories'
        )
        self.listing = MarketplaceListing.objects.create(
            seller=self.user1,
            title='Turbocharger',
            description='High-performance turbocharger',
            category=self.category,
            price=Decimal('1500.00'),
            condition='used',
            location='Los Angeles, CA',
            is_negotiable=True
        )

    def test_create_marketplace_listing(self):
        """Test creating a marketplace listing."""
        self.client.force_authenticate(user=self.user1)
        data = {
            'title': 'Exhaust System',
            'description': 'Custom exhaust system',
            'category': self.category.id,
            'price': '800.00',
            'condition': 'new',
            'location': 'Miami, FL',
            'is_negotiable': False
        }
        response = self.client.post('/api/marketplace/listings/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(MarketplaceListing.objects.filter(
            title='Exhaust System', seller=self.user1
        ).exists())

    def test_get_marketplace_listings(self):
        """Test getting marketplace listings."""
        response = self.client.get('/api/marketplace/listings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_listings(self):
        """Test searching marketplace listings."""
        response = self.client.get('/api/marketplace/listings/search/?q=turbo')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_listings_by_category(self):
        """Test filtering listings by category."""
        response = self.client.get(f'/api/marketplace/listings/?category={self.category.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_listings_by_price_range(self):
        """Test filtering listings by price range."""
        response = self.client.get('/api/marketplace/listings/?min_price=1000&max_price=2000')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_listing(self):
        """Test updating a marketplace listing."""
        self.client.force_authenticate(user=self.user1)
        data = {'price': '1400.00', 'is_negotiable': False}
        response = self.client.patch(f'/api/marketplace/listings/{self.listing.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.price, Decimal('1400.00'))

    def test_delete_listing(self):
        """Test deleting a marketplace listing."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f'/api/marketplace/listings/{self.listing.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(MarketplaceListing.objects.filter(id=self.listing.id).exists())

    def test_contact_seller(self):
        """Test contacting a seller."""
        self.client.force_authenticate(user=self.user2)
        data = {'message': 'Is this still available?'}
        response = self.client.post(f'/api/marketplace/listings/{self.listing.id}/contact_seller/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CarSalesTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username='seller1',
            email='seller1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='buyer1',
            email='buyer1@test.com',
            password='testpass123'
        )
        self.car_listing = CarListing.objects.create(
            seller=self.user1,
            title='2018 Chevrolet Camaro SS',
            description='Well-maintained Camaro SS',
            make='Chevrolet',
            model='Camaro',
            year=2018,
            price=Decimal('35000.00'),
            mileage=25000,
            condition='excellent',
            location='Los Angeles, CA',
            is_negotiable=True
        )

    def test_create_car_listing(self):
        """Test creating a car listing."""
        self.client.force_authenticate(user=self.user1)
        data = {
            'title': '2019 Ford Mustang GT',
            'description': 'Low mileage Mustang GT',
            'make': 'Ford',
            'model': 'Mustang',
            'year': 2019,
            'price': '42000.00',
            'mileage': 15000,
            'condition': 'excellent',
            'location': 'Miami, FL',
            'is_negotiable': True
        }
        response = self.client.post('/api/marketplace/cars/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CarListing.objects.filter(
            title='2019 Ford Mustang GT', seller=self.user1
        ).exists())

    def test_get_car_listings(self):
        """Test getting car listings."""
        response = self.client.get('/api/marketplace/cars/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_cars_by_make_model(self):
        """Test searching cars by make and model."""
        response = self.client.get('/api/marketplace/cars/search/?make=Chevrolet&model=Camaro')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_cars_by_year_range(self):
        """Test filtering cars by year range."""
        response = self.client.get('/api/marketplace/cars/?min_year=2017&max_year=2019')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_cars_by_price_range(self):
        """Test filtering cars by price range."""
        response = self.client.get('/api/marketplace/cars/?min_price=30000&max_price=40000')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_car_details(self):
        """Test getting detailed car information."""
        response = self.client.get(f'/api/marketplace/cars/{self.car_listing.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], '2018 Chevrolet Camaro SS')

    def test_schedule_test_drive(self):
        """Test scheduling a test drive."""
        self.client.force_authenticate(user=self.user2)
        data = {
            'preferred_date': '2024-01-15',
            'preferred_time': '14:00',
            'message': 'I would like to test drive this car'
        }
        response = self.client.post(f'/api/marketplace/cars/{self.car_listing.id}/schedule_test_drive/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ReviewAndRatingTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username='seller1',
            email='seller1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='buyer1',
            email='buyer1@test.com',
            password='testpass123'
        )
        self.listing = MarketplaceListing.objects.create(
            seller=self.user1,
            title='Test Listing',
            description='Test description',
            price=Decimal('100.00'),
            condition='new'
        )

    def test_create_review(self):
        """Test creating a review for a purchase."""
        self.client.force_authenticate(user=self.user2)
        data = {
            'listing': self.listing.id,
            'rating': 5,
            'title': 'Great product!',
            'content': 'Exactly as described, fast shipping',
            'is_verified_purchase': True
        }
        response = self.client.post('/api/marketplace/reviews/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Review.objects.filter(
            reviewer=self.user2, listing=self.listing
        ).exists())

    def test_get_listing_reviews(self):
        """Test getting reviews for a listing."""
        review = Review.objects.create(
            reviewer=self.user2,
            listing=self.listing,
            rating=5,
            title='Great product!',
            content='Excellent quality',
            is_verified_purchase=True
        )
        response = self.client.get(f'/api/marketplace/listings/{self.listing.id}/reviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_review(self):
        """Test updating a review."""
        review = Review.objects.create(
            reviewer=self.user2,
            listing=self.listing,
            rating=4,
            title='Good product',
            content='Pretty good',
            is_verified_purchase=True
        )
        self.client.force_authenticate(user=self.user2)
        data = {'rating': 5, 'content': 'Actually, excellent quality!'}
        response = self.client.patch(f'/api/marketplace/reviews/{review.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        review.refresh_from_db()
        self.assertEqual(review.rating, 5)

    def test_delete_review(self):
        """Test deleting a review."""
        review = Review.objects.create(
            reviewer=self.user2,
            listing=self.listing,
            rating=3,
            title='Okay product',
            content='Not bad',
            is_verified_purchase=True
        )
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(f'/api/marketplace/reviews/{review.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Review.objects.filter(id=review.id).exists())

    def test_rate_seller(self):
        """Test rating a seller."""
        self.client.force_authenticate(user=self.user2)
        data = {
            'seller': self.user1.id,
            'rating': 5,
            'comment': 'Great seller, fast communication'
        }
        response = self.client.post('/api/marketplace/ratings/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Rating.objects.filter(
            rater=self.user2, seller=self.user1
        ).exists())

    def test_get_seller_rating(self):
        """Test getting a seller's average rating."""
        Rating.objects.create(
            rater=self.user2,
            seller=self.user1,
            rating=5,
            comment='Great seller'
        )
        Rating.objects.create(
            rater=User.objects.create_user(username='user3', email='user3@test.com'),
            seller=self.user1,
            rating=4,
            comment='Good seller'
        )
        response = self.client.get(f'/api/marketplace/sellers/{self.user1.id}/rating/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['average_rating'], 4.5)


class PaymentAndWalletTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='testpass123'
        )
        self.wallet1 = UserWallet.objects.create(
            user=self.user1,
            balance=Decimal('1000.00')
        )
        self.wallet2 = UserWallet.objects.create(
            user=self.user2,
            balance=Decimal('500.00')
        )

    def test_get_wallet_balance(self):
        """Test getting wallet balance."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/marketplace/wallet/balance/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance'], '1000.00')

    def test_add_funds_to_wallet(self):
        """Test adding funds to wallet."""
        self.client.force_authenticate(user=self.user1)
        data = {'amount': '500.00', 'payment_method': 'credit_card'}
        response = self.client.post('/api/marketplace/wallet/add_funds/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.wallet1.refresh_from_db()
        self.assertEqual(self.wallet1.balance, Decimal('1500.00'))

    def test_withdraw_funds_from_wallet(self):
        """Test withdrawing funds from wallet."""
        self.client.force_authenticate(user=self.user1)
        data = {'amount': '200.00', 'withdrawal_method': 'bank_transfer'}
        response = self.client.post('/api/marketplace/wallet/withdraw_funds/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.wallet1.refresh_from_db()
        self.assertEqual(self.wallet1.balance, Decimal('800.00'))

    def test_transfer_funds_between_users(self):
        """Test transferring funds between users."""
        self.client.force_authenticate(user=self.user1)
        data = {'recipient': self.user2.id, 'amount': '100.00'}
        response = self.client.post('/api/marketplace/wallet/transfer/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.wallet1.refresh_from_db()
        self.wallet2.refresh_from_db()
        self.assertEqual(self.wallet1.balance, Decimal('900.00'))
        self.assertEqual(self.wallet2.balance, Decimal('600.00'))

    def test_get_transaction_history(self):
        """Test getting transaction history."""
        PaymentTransaction.objects.create(
            user=self.user1,
            amount=Decimal('100.00'),
            transaction_type='deposit',
            status='completed'
        )
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/marketplace/wallet/transactions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class OrderAndCheckoutTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username='buyer1',
            email='buyer1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='seller1',
            email='seller1@test.com',
            password='testpass123'
        )
        self.listing = MarketplaceListing.objects.create(
            seller=self.user2,
            title='Test Product',
            description='Test description',
            price=Decimal('100.00'),
            condition='new'
        )
        self.wallet = UserWallet.objects.create(
            user=self.user1,
            balance=Decimal('1000.00')
        )

    def test_create_order(self):
        """Test creating an order."""
        self.client.force_authenticate(user=self.user1)
        data = {
            'items': [
                {
                    'listing': self.listing.id,
                    'quantity': 1
                }
            ],
            'shipping_address': {
                'street': '123 Main St',
                'city': 'Los Angeles',
                'state': 'CA',
                'zip_code': '90210',
                'country': 'USA'
            },
            'payment_method': 'wallet'
        }
        response = self.client.post('/api/marketplace/orders/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Order.objects.filter(buyer=self.user1).exists())

    def test_get_user_orders(self):
        """Test getting user's order history."""
        order = Order.objects.create(
            buyer=self.user1,
            total_amount=Decimal('100.00'),
            status='pending'
        )
        OrderItem.objects.create(
            order=order,
            listing=self.listing,
            quantity=1,
            price=Decimal('100.00')
        )
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/marketplace/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_seller_orders(self):
        """Test getting seller's order history."""
        order = Order.objects.create(
            buyer=self.user1,
            total_amount=Decimal('100.00'),
            status='pending'
        )
        OrderItem.objects.create(
            order=order,
            listing=self.listing,
            quantity=1,
            price=Decimal('100.00')
        )
        self.client.force_authenticate(user=self.user2)
        response = self.client.get('/api/marketplace/seller/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_order_status(self):
        """Test updating order status."""
        order = Order.objects.create(
            buyer=self.user1,
            total_amount=Decimal('100.00'),
            status='pending'
        )
        self.client.force_authenticate(user=self.user2)
        data = {'status': 'shipped'}
        response = self.client.patch(f'/api/marketplace/orders/{order.id}/status/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.status, 'shipped')

    def test_cancel_order(self):
        """Test canceling an order."""
        order = Order.objects.create(
            buyer=self.user1,
            total_amount=Decimal('100.00'),
            status='pending'
        )
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(f'/api/marketplace/orders/{order.id}/cancel/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.status, 'cancelled')


class MarketplaceIntegrationTests(APITestCase):
    """Integration tests for marketplace features working together."""
    
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username='seller1',
            email='seller1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='buyer1',
            email='buyer1@test.com',
            password='testpass123'
        )
        self.category = ListingCategory.objects.create(
            name='Engine Parts',
            description='Engine components'
        )
        self.wallet1 = UserWallet.objects.create(
            user=self.user1,
            balance=Decimal('0.00')
        )
        self.wallet2 = UserWallet.objects.create(
            user=self.user2,
            balance=Decimal('1000.00')
        )

    def test_complete_marketplace_workflow(self):
        """Test a complete marketplace workflow: listing, purchase, review."""
        # 1. Create listing
        self.client.force_authenticate(user=self.user1)
        data = {
            'title': 'Turbocharger',
            'description': 'High-performance turbo',
            'category': self.category.id,
            'price': '500.00',
            'condition': 'used'
        }
        response = self.client.post('/api/marketplace/listings/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        listing = MarketplaceListing.objects.get(title='Turbocharger')
        
        # 2. Purchase item
        self.client.force_authenticate(user=self.user2)
        order_data = {
            'items': [{'listing': listing.id, 'quantity': 1}],
            'shipping_address': {
                'street': '123 Main St',
                'city': 'Los Angeles',
                'state': 'CA',
                'zip_code': '90210',
                'country': 'USA'
            },
            'payment_method': 'wallet'
        }
        response = self.client.post('/api/marketplace/orders/', order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 3. Seller ships item
        order = Order.objects.get(buyer=self.user2)
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(f'/api/marketplace/orders/{order.id}/status/', {'status': 'shipped'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 4. Buyer receives and reviews
        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(f'/api/marketplace/orders/{order.id}/status/', {'status': 'delivered'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        review_data = {
            'listing': listing.id,
            'rating': 5,
            'title': 'Great turbo!',
            'content': 'Excellent performance',
            'is_verified_purchase': True
        }
        response = self.client.post('/api/marketplace/reviews/', review_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify all steps worked
        self.assertTrue(Order.objects.filter(buyer=self.user2, status='delivered').exists())
        self.assertTrue(Review.objects.filter(
            reviewer=self.user2, listing=listing, is_verified_purchase=True
        ).exists())
        self.wallet1.refresh_from_db()
        self.wallet2.refresh_from_db()
        self.assertEqual(self.wallet1.balance, Decimal('500.00'))  # Seller received payment
        self.assertEqual(self.wallet2.balance, Decimal('500.00'))  # Buyer paid 