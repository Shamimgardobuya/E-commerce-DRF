from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

class SendEmail:
    def __init__(self, context):
        self.context = context
        
    def send_email(self):

        html_content = render_to_string('email_template.html', self.context)
        order = self.context.get("order")
        email = EmailMessage(
            subject=f"New Order from {self.context.get('customer')}",
            body=html_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[email for _, email in settings.ADMINS]
        )

        email.content_subtype = "html"
        email.send()
