from celery import shared_task
from django.core.mail import EmailMessage, BadHeaderError
from smtplib import SMTPException
import logging
from django.template.loader import render_to_string
from rest_framework import response
from django.conf import settings
from registration.models import Customer
import africastalking
import os
from dotenv import load_dotenv
load_dotenv()
logger = logging.getLogger(__name__)

@shared_task()
def send_email(context, is_customer=None):
        try:
            admin_emails = Customer.objects.filter(role="Admin").values_list('username', flat=True)
            html_content = render_to_string('email_template.html', context)
            order = context.get("order")
            
            email = EmailMessage(
                subject= f"Your new order " if is_customer else f"New Order from {context.get('customer')}",
                body=html_content,
                from_email=settings.EMAIL_HOST_USER,
                to= [context.get('customer')] if is_customer else [email for email in admin_emails]
            )
            email.content_subtype = "html"
            email.send()
        except BadHeaderError:
            logger.error("Email sending failed: Invalid header found.", exc_info=True)
            return False, "Invalid header found in email."
        except SMTPException as e:
            logger.error(f"Email sending failed: SMTP error occurred: {e}", exc_info=True)
            return False, "There was an error sending the email (SMTP error)."
        except Exception as e:
            logger.error(f"Email sending failed: An unexpected error occurred: {e}", exc_info=True)
            return False, "An unexpected error occurred while sending the email."
        return True, "Email sent successfully."
            

africastalking.initialize(
    username=os.getenv("SMS_USERNAME"),
    api_key=os.getenv("SMS_API_KEY")
)

sms = africastalking.SMS

def format_orders_summary(orders):
        total = sum(o.get('total_price', 0) for o in orders)
        items = []
        for o in orders:
            orderproduct = o.get('orderproduct', [])  
            for product_ in orderproduct:
                product_info = product_.get('product', {})
                product_name = product_info.get('name', 'Unknown Product')
                price = product_info.get('price', 0)
                quantity = product_.get('quantity', 0)
                total_price = price * quantity
                items.append(f"{product_name} - {price} x{quantity}: ${total_price:.2f}")
        items_str = "; ".join(items)
        return f"{items_str} | Grand Total: ${total:.2f}"
    
@shared_task()
def send_sms(recipient, message, sender):
        try:
            formatted_message = f"Order from {message.get('customer')}   {format_orders_summary(message.get('orders'))}"
            response = sms.send(formatted_message, [recipient], sender)
            print("SMS Response:", response)
            if not response or (isinstance(response, dict) and response.get('SMSMessageData', {}).get('Recipients', [{}])[0].get('status') != 'Success'):
                send_email(message, is_customer=True)
        except Exception as e:
            print(f"SMS sending failed: {e}")
            send_email(message, is_customer=True)
