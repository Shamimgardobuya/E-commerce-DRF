import africastalking
from django.conf import settings
from orders.email_orders import SendEmail
import os
from dotenv import load_dotenv
load_dotenv()
africastalking.initialize(
    
    username=os.getenv("SMS_USERNAME"),
    api_key=os.getenv("SMS_API_KEY")
)

sms = africastalking.SMS

class SendMessage:
    def __init__(self,recipient, message, sender):
        self.recipient = recipient 
        self.message = message 
        self.sender = sender 
        
    def format_orders_summary(orders):
        total = sum(o.total_price for o in orders)
        ids = ", ".join([f"#{o.id}:${o.total_price:.2f}" for o in orders])
        return f"{ids} | Grand Total:${total:.2f}"
        
    def send(self):
        try:
            formatted_message = f"Order from {self.message.get('customer')}   {self.format_orders_summary(self.message.get('orders'))}"
            response = sms.send(formatted_message, [self.recipient], self.sender)
            print(response)
        except Exception as e:
            SendEmail(self.message)
