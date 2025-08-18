import africastalking
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
    def __init__(self, recipient, message, sender):
        self.recipient = recipient
        self.message = message
        self.sender = sender
        
    def format_orders_summary(self, orders):
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

    def send(self):
        try:
            formatted_message = f"Order from {self.message.get('customer')}   {self.format_orders_summary(self.message.get('orders'))}"
            response = sms.send(formatted_message, [self.recipient], self.sender)
            print("SMS Response:", response)
            if not response or (isinstance(response, dict) and response.get('SMSMessageData', {}).get('Recipients', [{}])[0].get('status') != 'Success'):
                SendEmail(self.message)
        except Exception as e:
            print(f"SMS sending failed: {e}")
            SendEmail(self.message)
