from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def email_sender(subject, template_name, receivers, context, sender=settings.EMAIL_HOST_USER):
    msg_html = render_to_string(template_name, context)
    msg = EmailMessage(subject=subject, body=msg_html, from_email=sender, bcc=receivers)
    msg.content_subtype = "html"
    return msg.send()


def send_review_email(url, receiver):
    subject = "Vurder det siste oppholdet"
    context = {
        'url': url
    }
    email_sender(subject,'email/review-email.html', [receiver], context)



