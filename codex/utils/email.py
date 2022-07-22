from django.template.loader import render_to_string
from core.settings import DOMAIN


def send_account_confirm_email(request, user, activation_token):
    """Generate a confirmation token and send it to the user"""
    subject = "Welcome to the Moonsea Codex"
    message = render_to_string(
        "emails/account_activation_email.html",
        {
            "user": user,
            "user_id": user.pk,
            "domain": DOMAIN,
            "token": activation_token,
        },
    )
    return user.email_user(subject, message)

def send_password_reset_email(request, user, activation_token):
    """Generate a password reset token and send it to the user"""
    subject = "Moonsea Codex password reset"
    message = render_to_string(
        "emails/password_reset_email.html",
        {
            "domain": DOMAIN,
            "token": activation_token,
            "user_id": user.id,
        },
    )
    return user.email_user(subject, message)
