from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_verification_email(user, uidb64, token):
    verification_link = f"http://app.fastprintguys.com/verify-email/{uidb64}/{token}/"  # Frontend URL
    subject = "Email Verification - FastPrintGuys"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [user.email]

    context = {
        "name": user.name,
        "verification_link": verification_link
    }

    html_content = render_to_string("emails/verify_email.html", context)
    text_content = f"Hi {user.name},\n\nPlease verify your email using this link:\n{verification_link}"

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_password_reset_email(user, uidb64, token):
    reset_link = f"http://app.fastprintguys.com/reset-password/{uidb64}/{token}/"  # Frontend URL
    subject = "Reset Your Password - FastPrintGuys"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [user.email]

    context = {
        "name": user.name,
        "reset_link": reset_link
    }

    html_content = render_to_string("emails/reset_password_email.html", context)
    text_content = f"Hi {user.name},\n\nClick the link to reset your password:\n{reset_link}"

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
