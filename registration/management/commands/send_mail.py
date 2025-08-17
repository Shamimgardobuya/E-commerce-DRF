from django.core.mail import send_mail

send_mail(
    subject="Test Email",
    message="This is a plain test email",
    from_email="shamimobuya@gmail.com",
    recipient_list=["obuyashamim21@gmail.com"],
    fail_silently=False,
)