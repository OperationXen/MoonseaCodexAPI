from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site


def send_account_confirm_email(user, activation_token):
    """Generate a confirmatin token and send it to the user"""
    subject = "Activate Your MySite Account"
    current_site = get_current_site()
    message = render_to_string(
        "emails/account_activation_email.html",
        {
            "uid": user.pk,
            "domain": current_site.domain,
            "token": activation_token,
        },
    )
    return user.email_user(subject, message)
