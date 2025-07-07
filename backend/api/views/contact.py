"""
Contact form API view for CalloutRacing Application
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from core.models.marketplace import ContactSubmission


@api_view(['POST'])
@permission_classes([AllowAny])
def contact_form(request):
    """
    Handle contact form submissions and send email notifications.
    
    This endpoint allows anyone to submit a contact form. It sends an email
    to the admin and a confirmation email to the user.
    
    Args:
        request: HTTP request object containing name, email, subject, and message
        
    Returns:
        Response with success/error message
    """
    try:
        name = request.data.get('name')
        email = request.data.get('email')
        subject = request.data.get('subject')
        message = request.data.get('message')
        
        # Validate required fields
        if not all([name, email, subject, message]):
            return Response({
                'error': 'All fields are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if email is configured
        email_configured = (
            settings.EMAIL_HOST_USER and 
            settings.EMAIL_HOST_PASSWORD and 
            settings.DEFAULT_FROM_EMAIL
        )
        
        if email_configured:
            try:
                # Prepare email content for admin notification
                email_subject = f"CalloutRacing Contact: {subject}"
                email_body = f"""
New contact form submission from CalloutRacing:

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}

---
This message was sent from the CalloutRacing contact form.
                """
                
                # Send email to admin
                send_mail(
                    subject=email_subject,
                    message=email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['digibin@digitalbinarysolutionsllc.com'],
                    fail_silently=True,  # Don't fail if email sending fails
                )
                
                # Prepare confirmation email for user
                confirmation_subject = "Thank you for contacting CalloutRacing"
                confirmation_body = f"""
Dear {name},

Thank you for reaching out to CalloutRacing! We have received your message and will get back to you within 24 hours.

Your message:
Subject: {subject}
Message: {message}

Best regards,
The CalloutRacing Team
                """
                
                # Send confirmation email to user
                send_mail(
                    subject=confirmation_subject,
                    message=confirmation_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=True,  # Don't fail if email sending fails
                )
                
            except Exception as email_error:
                # Log email error but don't fail the request
                print(f"Email sending failed: {email_error}")
        
        # Store contact form submission in database for admin review
        try:
            ContactSubmission.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
        except Exception as db_error:
            # Log database error but don't fail the request
            print(f"Database storage failed: {db_error}")
        
        return Response({
            'message': 'Thank you for your message! We\'ll get back to you soon.'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Contact form error: {e}")
        return Response({
            'error': 'There was an error sending your message. Please try again.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 